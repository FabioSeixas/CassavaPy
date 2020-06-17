import os
import datetime
import pandas as pd
from tqdm import tqdm

from tradssat import DSSATResults, PlantGroOut, SoilWatOut, ETOut


class ExperimentalOut(object):

    def __init__(self, trat, years):
        self.trat = trat
        self.years = years
        self.results = DSSATResults("C:/DSSAT47/Cassava/")
        self.files = {PlantGroOut: ["YEAR", "DOY", "DAS", "DAP", "L#SD", "LAID", "RWAD", "CWAD", "LWAD", "SWAD", "HWAD", "HIAD", "PARID", "PARUD", "AWAD", "TWAD", "WAVRD", "WUPRD", "WFPD", "WFGD", "TFPD", "TFGD"],
                      SoilWatOut: ["YEAR", "DOY", "DAS", "SWTD", "SWXD", "PREC", "IRRC", "SW1D", "SW2D", "SW3D", "SW4D"],
                      ETOut: ["YEAR", "DOY", "DAS", "SRAA", "EOAA", "EOPA", "ETAA", "EPAA"]}

        self.index = self.make_index(self.trat, self.years)
        self.df = self.get_outputs()

    def get_var(self, name, trt, run):
        return self.results.get_value(name, trt=trt, run=run)

    def make_date(self, year, doy):
        return datetime.datetime(int(year), 1, 1) + datetime.timedelta(int(doy) - 1)

    def make_index(self, trat, years):
        return [(n + 1, self.correct_runno(n + 1, i + 1, years))
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

    def correct_runno(self, trat, runno, years):
        # Talvez aqui dê para usar enumerate
        return runno + years * (trat - 1)

    def read_each_table(self, trat, run, file, variables):

        df = pd.DataFrame({var: self.get_var(var, trat, run) for var in variables})

        print(f'Processing Treatment {trat} and Run {run}')

        return self.handle_columns(df, trat, run, file)
