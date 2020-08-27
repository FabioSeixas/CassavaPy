from cassavapy import Output
import pandas as pd
import json


def extract_experiment(json_file, tratmatrix):

    with open(f'{json_file}.json') as f:
        params = json.load(f)

    trat = len(tratmatrix)
    years = 1
    files = len(range(int(params["general"]["first_year"]), 
                      int(params["general"]["last_year"]) + 1))
    modo = "Experimental"

    x = Output(trat=trat, years=years, mode=modo, files=files)
    x.df.to_csv("output.csv")
