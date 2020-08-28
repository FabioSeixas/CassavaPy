import pandas as pd


def laminas_by_year(data, year):
    unique_dates = data.iloc[:, 0].unique()

    laminas = []
    for unique in unique_dates:
        laminas.append(data[(data.iloc[:, 1] == year) & (data.iloc[:, 0] == unique)].iloc[:, 3].values.tolist())

        if not laminas[-1]:
            laminas[-1] = [0, ]

    return laminas


def dap_by_year(data, year):
    unique_dates = data.iloc[:, 0].unique()

    dap = []
    for unique in unique_dates:
        dap.append(data[(data.iloc[:, 1] == year) & (data.iloc[:, 0] == unique)].iloc[:, 2].values.tolist())

        if not dap[-1]:
            dap[-1] = [0, ]

    return dap
