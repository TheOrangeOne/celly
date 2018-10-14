from functools import reduce


class CogWheel(object):
    def __init__(self):
        self.subs = {}
        self.wait_cogs = {}
        self.initial_cogs = {}
        self.ready_cogs = {}

    def add(self, new_cog):
        if not new_cog.inputs:
            self.initial_cogs[new_cog.name] = new_cog
            return

        for cog in new_cog.inputs:
            if cog not in self.subs:
                self.subs[cog] = []
            self.subs[cog].append(new_cog.name)
            self.wait_cogs[new_cog.name] = new_cog

    def _process(self, cogs):
        new_ready_cogs = {}
        for name, cog in cogs.items():
            cog_inputs = [self.ready_cogs[inp].out for inp in cog.inputs]
            cog.out = cog.output(*cog_inputs)
            self.ready_cogs[name] = cog

            if name not in self.subs:
                continue

            for sub in self.subs[name]:
                subcog = self.wait_cogs[sub]
                is_ready = reduce(
                    lambda x, y: x and y,
                    map(
                        lambda x: x in self.ready_cogs,
                        subcog.inputs
                    )
                )

                if is_ready:
                    new_ready_cogs[sub] = subcog

        if new_ready_cogs:
            self._process(new_ready_cogs)

    def start(self):
        self._process(self.initial_cogs)
