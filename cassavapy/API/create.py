from cassavapy import Experimental
from .irrigation import laminas_by_year, dap_by_year
from pandas import read_csv
import json
import ast

def set_experiment(json_file, data_irrig = None):
    
    with open(f'{json_file}.json') as f:
        params = json.load(f)
    
    for year in range(int(params["general"]["first_year"]), 
                      int(params["general"]["last_year"]) + 1):
        
        x = Experimental(filename=f'{params["general"]["file_name"]}{year}', 
                         exp_name=params["general"]["nome_exp"], 
                         design=params["general"]["design"])

        x.set_harvest(n_harvest=int(params["harvest"]["n_harvest"]), 
                      h_from=f'{str(year + int(params["harvest"]["harv_plant_year"]))}-{params["harvest"]["h_from"]}', 
                      h_by=int(params["harvest"]["h_by"]))

        x.set_planting(n_plant=int(params["planting"]["n_plant"]),
                       p_from=f'{str(year)}-{params["planting"]["p_from"]}',
                       p_by=int(params["planting"]["p_by"]))
        
        if isinstance(params["genotype"]["genotype_code"], list):
            genotype_input = [(code, name) for code, name in zip(params["genotype"]["genotype_code"], 
                                                                 params["genotype"]["genotype_name"])]
        else:
            genotype_input = (params["genotype"]["genotype_code"], params["genotype"]["genotype_name"])
        
        x.set_genotype(genotype=genotype_input)

        x.set_field(code_id=params["field"]["code_id"], 
                    soil_id=params["field"]["soil_id"], 
                    water=float(params["field"]["water"]))

        x.set_controls(sim_start = params["controls"]["sim_start"],
                       date_start = f'{year + int(params["controls"]["plant_rel_year"])}-{params["controls"]["date_start"]}',
                       years=int(params["controls"]["seas_years"]))
        
        
        irrig_input = irrigation_inputs(params["irrigation"].copy(), year=year, data_irrig=data_irrig)
        
        x.set_irrigation(laminas=irrig_input["laminas"],
                         n_irrig=irrig_input["n_irrig"],
                         from_irrig=irrig_input["from_irrig"],
                         by_irrig=irrig_input["by_irrig"],
                         reg=irrig_input["reg"],
                         trat_irrig=irrig_input["trat_irrig"])

        x.set_tratmatrix("BA")

        x.write_file()
    
    return x._tratmatrix

def irrigation_inputs(params, year, data_irrig = None):

    ext_data = params.pop("ext_data")

    dic = {key: ast.literal_eval(value) if value else "NULL" for key, value 
            in params.items()}
    
    if ext_data == "N":
        return dic

    else: 
        data_irrig = read_csv(data_irrig)
        dic["laminas"] = laminas_by_year(data_irrig, year=year)
        dic["reg"] = dap_by_year(data_irrig, year=year)
    
    return dic

