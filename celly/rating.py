import copy

def normalize_rating(rating, min=1400, max=1600):
    return ((rating - min) / (max - min))*100

class RatingModel:
    IR = 1500.0
    HF = 0
    SP = 400

    def __init__(self, ids={}, ir=1500.0, hf=0, sp=400, kf=None):
        self.ratings = {}
        for id in ids:
            self.ratings[id] = {
                "rating": ir,
                "gp": 0,
            }
        self.IR = ir
        self.HF = hf
        self.SP = sp
        self.KF = lambda gp: 15 if gp < 10 else 5
        if kf:
            self.KF = kf

    def _expected_scores(self, ra, rb):
        homeexp = 1 / (1 + 10**((rb-ra+self.HF)/self.SP))
        awayexp = 1 - homeexp
        return (homeexp, awayexp)
    
    def _actual_scores(self, homescore, awayscore, period):
        if period == 5:
            return (0.5, 0.5)
        elif period == 4 and homescore > awayscore:
            return (0.6, 0.4)
        elif period == 4 and awayscore > homescore:
            return (0.4, 0.6)
        elif homescore > awayscore:
            return (1.0, 0.0)
        elif awayscore > homescore:
            return (0.0, 1.0)
        else:
            raise Exception("failed to calculate actual score")

    def _update_rating(self, old, act, exp, gp):
        K = self.KF(gp)
        new = old + (K * (act - exp))
        return new

    def calculate_rating(self, home, away, period):
        hid, hscore = home
        aid, ascore = away

        for id in [hid, aid]:
            if id not in self.ratings:
                self.ratings[id] = {
                    "rating": self.IR,
                    "gp": 0,
                }

        hr = self.ratings[hid]["rating"]
        ar = self.ratings[aid]["rating"]
        
        hexp, aexp = self._expected_scores(hr, ar)
        hact, aact = self._actual_scores(hscore, ascore, period)

        hgp = self.ratings[hid]["gp"]
        hnr = self._update_rating(hr, hact, hexp, hgp)
        self.ratings[hid]["rating"] = hnr
        self.ratings[hid]["gp"] += 1

        agp = self.ratings[aid]["gp"]
        anr = self._update_rating(ar, aact, aexp, agp)
        self.ratings[aid]["rating"] = anr
        self.ratings[aid]["gp"] += 1

    def copyratings(self):
        return copy.deepcopy(self.ratings)
