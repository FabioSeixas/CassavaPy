import os
import datetime
import pandas as pd
from itertools import chain

from tradssat import DSSATResults, PlantGroOut, SoilWatOut, ETOut


class ExperimentalOut(object):

    def __init__(self, trat, years, files_n):
        self.trat = trat
        self.years = years
        self.files_n = files_n
        self.results = DSSATResults("C:/DSSAT47/Cassava/")
        self.files = {PlantGroOut: ["YEAR", "DOY", "DAS", "DAP", "TMEAN", "L#SD", "LAID", "RWAD", "CWAD", "LWAD", "SWAD", "HWAD", "HIAD", "PARID", "PARUD", "AWAD", "TWAD", "WAVRD", "WUPRD", "WFPD", "WFGD", "TFPD", "TFGD", "SLAD"],
                      SoilWatOut: ["YEAR", "DOY", "DAS", "SWTD", "SWXD", "PREC", "IRRC", "SW1D", "SW2D", "SW3D", "SW4D"],
                      ETOut: ["YEAR", "DOY", "DAS", "SRAA", "EOAA", "EOPA", "ETAA", "EPAA"]}

        self.index = self.make_index(self.trat, self.years, self.files_n)
        self.df = self.get_outputs()

    def get_var(self, name, trt, run):
        return self.results.get_value(name, trt=trt, run=run)

    def make_date(self, year, doy):
        return datetime.datetime(int(year), 1, 1) + datetime.timedelta(int(doy) - 1)

    def make_index(self, trat, years, files_n=None):
        '''
        Work around for 'files' and 'years'
        if 'files' > 1, 'years' must be 1
        if 'years' > 1, files must be 1
        You can't get the two together
        '''

        def correct_runno_files(trat_n, file, trat_total):
            return file * trat_total - (trat_total - trat_n)

        if files_n is not None and years == 1:
            return [(t + 1, correct_runno_files(t + 1, f + 1, trat))
                    for f in range(files_n)
                    for t in range(trat)]

        def correct_runno_years(trat, runno, years):
            return runno + years * (trat - 1)

        return [(n + 1, correct_runno_years(n + 1, i + 1, years))
                for n in range(trat)
                for i in range(years)]

    def get_outputs(self):

        final_df = pd.DataFrame(columns=["TRAT", "RUN", "DATE"])

        for file, variables in self.files.items():

            if self.change_out_file(file):

                print(f' \n Preparing {file.filename} file')

                df_list = [self.read_each_table(trat, run, file, variables)
                           for trat, run in self.index]

                df_list = pd.concat(df_list)

                final_df = pd.merge(final_df, df_list, how="outer", on=["DATE", "TRAT", "RUN"])
                final_df.sort_values(["TRAT", "RUN", "DATE"], axis=0, inplace=True)

        return final_df

    def change_out_file(self, file):

        self.results._outfiles_clases = {f.filename: f for f in [file, ]}  # PlantGroOut, SoilWatOut, SoilNiOut, SoilTempOut, ETOut]}
        self.results._outfiles = {f: None for f in self.results._outfiles_clases}

        # Check if the output file exists
        return os.path.isfile(f'C:/DSSAT47/Cassava/{[*self.results._outfiles.keys()][0]}')

    def handle_columns(self, df, trat, run, file):
        df["TRAT"] = trat
        df["RUN"] = run
        df["DATE"] = [self.make_date(str(x), str(y)) for x, y in zip(df["YEAR"], df["DOY"])]
        df.drop(["YEAR", "DOY"], axis=1, inplace=True)

        if file != SoilWatOut:
            df.drop("DAS", axis=1, inplace=True)

        return df

    def read_each_table(self, trat, run, file, variables):

        df = pd.DataFrame({var: self.get_var(var, trat, run) for var in variables})

        print(f"Treatment {trat} ; Run {run}")

        return self.handle_columns(df, trat, run, file)
