import numpy as np
import pandas as pd
import datetime
import re

def identify_output(file):

    vec = {"Weather": 10,
           "PlantGro": 10,
           "PlantGrf": 11,
           "SoilWat": 12,
           "PlantGr2": 10,
           "ET": 12}

    return vec[file[:-4]]

def custom_remove_na(data):

    try:
        na_threshold = np.where(data.isna())[0][0]

        return data.iloc[0:na_threshold, :]

    except:
        return data

make_date = lambda x, y: datetime.datetime(int(x), 1, 1) + datetime.timedelta(int(y) - 1)


def n_trat_out_file(file):
    pattern = re.compile("@")
    ind = []
    for i, line in enumerate(open(f"C:/DSSAT47/Cassava/{file}")):
        for match in re.finditer(pattern, line):
            ind.append(str(i + 1))
    return ind


def from_file_to_dataframe(index, dir, heading, colspecs, out_file):

    all_treataments = pd.DataFrame()

    for i, index_value in enumerate(index):

        data = pd.read_fwf(f'{dir}/{out_file}.OUT',
                           skiprows = int(index_value),
                           names = heading,
                           colspecs = colspecs)

        data = custom_remove_na(data)

        data["Date"] = [make_date(x, y) for x, y in zip(data["Year"], data["DOY"])]

        data.drop(columns = ["Year", "DOY"], inplace = True)

        data["Trat_n"] = i + 1

        all_treataments = pd.concat([all_treataments, data],
                                    ignore_index = True)

    return all_treataments
