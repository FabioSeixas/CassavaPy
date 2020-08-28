import pandas as pd


def laminas_by_year(data, year):
    unique_dates = data.PDate_norm.unique()

    laminas = []
    for unique in unique_dates:
        laminas.append(data[(data.Pyear == year) & (data.PDate_norm == unique)]["diff"].values.tolist())

        if not laminas[-1]:
            laminas[-1] = [0, ]

    return laminas


def dap_by_year(data, year):
    unique_dates = data.PDate_norm.unique()

    dap = []
    for unique in unique_dates:
        dap.append(data[(data.Pyear == year) & (data.PDate_norm == unique)]["DAP"].values.tolist())

        if not dap[-1]:
            dap[-1] = [0, ]

    return dap
