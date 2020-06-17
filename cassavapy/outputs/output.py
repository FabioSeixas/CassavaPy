from .Seasonal import SeasonalOut
from .Experimental import ExperimentalOut


class Output(object):

    def __init__(self, trat, years=None, mode=None):
        self.trat = trat
        self.years = years
        self.mode = mode
        self.instance = self.output_class(self.trat, self.years, self.mode)
        self.df = self.instance.df

    def output_class(self, trat, years, mode):
        if mode == "Experimental":
            return ExperimentalOut(trat, years)
        elif mode == "Seasonal":
            return SeasonalOut(trat, years)
        raise(ValueError(f'"{mode}" not recognized for "mode" argument. Try "Seasonal" or "Experimental".'))
