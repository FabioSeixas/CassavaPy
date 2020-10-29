from cassavapy import Output
import pandas as pd
import json


def extract_experiment(json_file, tratmatrix):

    with open(f'{json_file}.json') as f:
        params = json.load(f)

    trat = len(tratmatrix)

    if params['general']['n_files'] == 'multi':
        files = len(range(int(params["general"]["first_year"]), 
                      int(params["general"]["last_year"]) + 1))
        years = 1
    
    elif params['general']['n_files'] == 'one':
        files = [f'{params["general"]["file_name"]}{params["general"]["first_year"]}']
        years = int(params["general"]["last_year"]) - int(params["general"]["first_year"]) + 1
    
    else:
        raise ValueError(f"Value '{params['general']['n_files']}' not recognized for 'n_files' parameter.")

    modo = "Experimental"

    x = Output(trat=trat, years=years, mode=modo, files=files)
    x.df.to_csv(f'{params["general"]["nome_exp"]}.csv')
