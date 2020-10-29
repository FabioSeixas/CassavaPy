from cassavapy import write_batch, run_batch
import json

def run_experiment(json_file):
    
    with open(f'{json_file}.json') as f:
        params = json.load(f)

    if params['general']['n_files'] == 'multi':
        files = [f'{params["general"]["file_name"]}{year}' for year 
                in range(int(params["general"]["first_year"]), 
                        int(params["general"]["last_year"]) + 1)]
    
    elif params['general']['n_files'] == 'one':
        files = [f'{params["general"]["file_name"]}{params["general"]["first_year"]}']
    
    else:
        raise ValueError(f"Value '{params['general']['n_files']}' not recognized for 'n_files' parameter.")


    write_batch(files)

    run_batch()
