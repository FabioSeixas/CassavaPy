from cassavapy import write_batch, run_batch
import json

def run_experiment(json_file):
    
    with open(f'{json_file}.json') as f:
        params = json.load(f)

    files = [f'{params["general"]["file_name"]}{year}' for year 
             in range(int(params["general"]["first_year"]), 
                      int(params["general"]["last_year"]) + 1)]

    write_batch(files)

    run_batch()
