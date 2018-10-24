from functools import reduce


class CogMissingError(Exception):
    pass


class CogArgError(Exception):
    pass


class CogWheel(object):
    def __init__(self):
        self.subs = {}
        self.wait_cogs = {}
        self.initial_cogs = {}
        self.computed_cogs = {}

    def add(self, new_cog):
        # if the new cog has no inputs then it can be run immediately
        # so add it as an initial cog.
        if not new_cog.inputs:
            self.initial_cogs[new_cog.name] = new_cog
            return

        # else subscribe the cog to its inputs
        for argname, cogname in new_cog.inputs.items():
            if cogname not in self.subs:
                self.subs[cogname] = []
            self.subs[cogname].append(new_cog.name)
            self.wait_cogs[new_cog.name] = new_cog

    def _process(self, ready_cogs):
        new_ready_cogs = {}
        for name, cog in ready_cogs.items():
            # substitute the generated cog output for the cog name
            cog_inputs_with_outputs = {
                argname: self.computed_cogs[cogname].out
                for argname, cogname in cog.inputs.items()
            }
            # invoke the cog and store the result in cog.out
            try:
                cog.out = cog(**cog_inputs_with_outputs)
            except TypeError as e:
                cogcls = cog.__class__.__name__
                raise CogArgError(
                    '''Error in {}\n{}. \n'''
                    '''args: {}'''.format(cogcls, e, cog_inputs_with_outputs)
                )

            self.computed_cogs[name] = cog

            for sub in self.subs.get(name, []):
                subcog = self.wait_cogs[sub]
                is_ready = reduce(
                    lambda x, y: x and y,
                    map(
                        lambda x: x in self.computed_cogs,
                        subcog.inputs.values()
                    )
                )

                if is_ready:
                    new_ready_cogs[sub] = subcog

        if new_ready_cogs:
            self._process(new_ready_cogs)

    def _validate_cogs(self, initial_cogs, wait_cogs):
        if not initial_cogs and wait_cogs:
            missing_cogs = [
                cogname for cog in wait_cogs.values()
                for cogname in cog.inputs.values()
            ]
            missing_cogs = ','.join(missing_cogs)
            raise CogMissingError(
                '''No starting point cog found,'''
                '''missing the following cogs: '''
                '''{}'''.format(missing_cogs)
            )
        all_cog_names = set(
            [cogname for cogname in initial_cogs] +
            [cogname for cogname in wait_cogs]
        )
        missing_cogs = [
            cogname for cog in wait_cogs.values()
            for cogname in cog.inputs.values()
            if cogname not in all_cog_names
        ]
        if missing_cogs:
            raise CogMissingError(
                '''Missing the following cogs: '''
                '''{}'''.format(missing_cogs)
            )

    def start(self):
        self._validate_cogs(self.initial_cogs, self.wait_cogs)
        self._process(self.initial_cogs)
