import datetime
import pandas as pd

from tradssat import DSSATResults


class SeasonalOut(object):

    def __init__(self, trat, years):
        self.trat = trat
        self.years = years
        self.vars = ["TRNO", "SDAT", "PDAT", "HDAT", "HWAM", "IRCM", "PRCM"]
        self.folder = "C:/DSSAT47/Seasonal/"
        self.results = DSSATResults(self.folder)
        self.index = self.make_index(self.trat, self.years)
        self.df = self.get_summary(self.vars, self.index)

    def make_index(self, trat, years):
        index = [()]
        for n in range(trat):
            for i in range(years):
                runno = self.correct_runno(n + 1, i + 1, years)
                index.append((n + 1, runno))
        return index[1:]

    def correct_runno(self, trat, runno, years):
        return runno + years * (trat - 1)

    def get_var(self, name, trt, runno):
        return self.results.get_final_value(name,
                                            trt=trt,
                                            cond={"RUNNO": runno})

    def make_date(self, year, doy):
        return datetime.datetime(int(year), 1, 1) + datetime.timedelta(int(doy) - 1)

    def make_df(self, variables, index):
        df = pd.DataFrame()
        for var in variables:
            df[var] = pd.Series([1, ] * len(index))
        return df

    def get_summary(self, variables, index):
        df = self.make_df(variables, index)

        for var in variables:
            df[var] = [self.get_var(name=var,
                                    trt=n,
                                    runno=i) for n, i in index]

        df["SDAT"] = [self.make_date(str(x)[:4], str(y)[4:]) for x, y in zip(df["SDAT"], df["SDAT"])]
        df["PDAT"] = [self.make_date(str(x)[:4], str(y)[4:]) for x, y in zip(df["PDAT"], df["PDAT"])]
        df["HDAT"] = [self.make_date(str(x)[:4], str(y)[4:]) for x, y in zip(df["HDAT"], df["HDAT"])]

        return df
