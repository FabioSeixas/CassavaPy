from cassavapy import Experimental
import json

def set_experiment(json_file):
    
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

        irrigation_inputs(params)
        #x.set_irrigation(laminas=irrig.laminas_by_year(dados_irrig, year),
        #                 reg=irrig.dap_by_year(dados_irrig, year),
        #                 trat_irrig=reg_dicionario)

        x.set_tratmatrix("BA")

        x.write_file()
    
    return x._tratmatrix

def irrigation_inputs(params):

    dic = {
        "laminas": "NULL", 
        "n_irrig": "NULL", 
        "from_irrig": "NULL", 
        'by_irrig': "NULL",
        "reg": "NULL", 
        "trat_irrig": "NULL"
    }

    if "irf" in params["general"]["design"]:
        dic = {key: value if value else "NULL" for key, value 
               in params["irrigation"].items()}
        
        print(dic)
