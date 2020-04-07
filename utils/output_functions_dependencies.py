import numpy as np
import pandas as pd
import datetime
import re

from tqdm import tqdm


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

    with tqdm(iterable = index) as pbar:

        for i, index_value in enumerate(index):

            data = pd.read_fwf(f'{dir}/{out_file}.OUT',
                               skiprows = int(index_value),
                               names = heading,
                               colspecs = colspecs)

            data = custom_remove_na(data)

            data["Date"] = [make_date(x, y) for x, y in zip(data["Year"], data["DOY"])]

            data.drop(columns = ["Year", "DOY"], inplace = True)

            data["Trat_n"] = i + 1      # Note that 'Trat_n' is an simulation index for the entire Batch file.
                                        # That means if you run more than one Batch file, you will end with
                                        # more than one index lists.

            all_treataments = pd.concat([all_treataments, data],
                                        ignore_index = True)

            pbar.update()

    return all_treataments

def set_dates_seasonal(data):

    data["p_year"] = [str(x)[:4] for x in data["PDAT"]]
    data["p_doy"] = [str(x)[4:7] for x in data["PDAT"]]
    data["h_year"] = [str(x)[:4] for x in data["HDAT"]]
    data["h_doy"] = [str(x)[4:7] for x in data["HDAT"]]

    data["PDate"] = [make_date(x, y) for x, y in zip(data["p_year"], data["p_doy"])]
    data["HDate"] = [make_date(x, y) for x, y in zip(data["h_year"], data["h_doy"])]

    return data.drop(columns = ["p_year", "p_doy", "h_year", "h_doy", "@"])
