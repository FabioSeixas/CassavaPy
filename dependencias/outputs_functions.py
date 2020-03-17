from pathlib import Path

import numpy as np
import pandas as pd
import subprocess
import shutil
import sys
import os

from . import output_functions_dependencies as dep

def get_outputs(dir, mode="exp", out_files = None, trats = None):

    dir = Path(dir) / 'Outputs'

    # Diretório de Ouputs já existe
    if dir.exists():
        with os.scandir(dir) as entries:
            if any(entries):
                print(f"\n Diretório '{dir}' não vazio. \n Deseja encerrar a função (N) ou deixar que a execução delete os arquivos em {dir} automaticamente (Y) ?")
                x = input()
                if x == "N" or x == "n":
                    print("\n Execução interrompida.")
                    sys.exit()
                elif x == "Y" or x == "y":
                    print(f"\n Arquivos em '{dir}' deletados. \n Executando função.")
                    shutil.rmtree(dir)
                else:
                    print("\n Valor inválido. Escolha 'N' ou 'Y'.")
                    sys.exit()

            else:
                print(f' \n Diretório {dir} vazio e disponível para uso. ')
                shutil.rmtree(dir)

    # Diretório de Ouputs não existe
    else:
        print(f'\n Diretório "{dir}" criado.')

    try:
        os.mkdir(dir)
    except:
        raise ValueError(f"\n Não foi possível criar diretório '{dir}'. ")

    print(f' \n Rodando extração de Outputs \n')
    extract_outputs(dir=dir, mode=mode)

    print(f' \n Processo Finalizado. \n Ouputs em "{dir}".')


def extract_outputs(dir, mode):

    if mode == "exp":

        files = ["PlantGro.OUT", "Weather.OUT", "PlantGrf.OUT", "PlantGr2.OUT", "SoilWat.OUT", "ET.OUT"]

        all_outputs = pd.DataFrame(columns = ["Date", "Trat_n"])

        for file in files:

            # Número de tratamentos por arquivo e índices das tabelas
            index = dep.n_trat_out_file(file)

            # Criar tabelas de resultados
            file_out = extract_by_file(index, file)

            # Merge tables
            all_outputs = pd.merge(all_outputs, file_out, how = "outer",
                                   on = ["Date", "Trat_n"])

        all_outputs.sort_values(by = ["Trat_n", "Date"], inplace = True)
        all_outputs.to_csv("testetodas.csv")

    elif mode == "seas":

        diretorio = 'C:/DSSAT47/Seasonal'

        file_out = extract_seasonal(diretorio)

    else:
        raise ValueError(f' Valor {mode} não reconhecido para o argumento "mode".')


def extract_by_file(index, file):

    print(f'\n Processando "{file}"...\n')

    dir = "C:/DSSAT47/Cassava"

    return {"PlantGro.OUT": lambda: PlantGro(index, dir),
            "Weather.OUT": lambda: Weather(index, dir),
            "PlantGrf.OUT": lambda: PlantGrf(index, dir),
            "PlantGr2.OUT": lambda: PlantGr2(index, dir),
            "SoilWat.OUT": lambda: SoilWat(index, dir),
            "ET.OUT": lambda: ET(index, dir),
            }.get(file)()


def PlantGro(index, dir):

    heading = ["Year", "DOY", "DAP", "GSTD", "PARID", "PARUD", "AWAD", "LAID", "TWAD", "RWAD", "CWAD", "LWAD", "HWAD", "HIAD", "RDPD", "SWXD", "WAVRD", "WUPRD", "WFPD", "WFGD", "TFPD", "TFGD", ]

    colspecs = [(1,5), (6, 9), (18, 21), (28, 33), (40, 45), (46, 51), (53, 57), (58, 63), (76, 81), (89, 93), (94, 99), (100, 105), (112, 117), (117, 123), (160, 165), (166, 171), (172, 177), (178, 183), (185, 189), (191, 195), (215, 219), (221, 225)]

    return dep.from_file_to_dataframe(index, dir, heading, colspecs, "PlantGro")


def Weather(index, dir):

    heading = ["Year", "DOY", "PRED", "DAYLD", "SRAD", "CLDD", "TMXD", "TMND", "TAVD", "TDWD", "WDSD"]

    colspecs = [(1,5), (6, 9), (17, 22), (24, 29), (39, 43), (53, 57), (60, 64), (67, 71), (74, 78), (88, 92), (109, 113)]

    return dep.from_file_to_dataframe(index, dir, heading, colspecs, "Weather")


def PlantGrf(index, dir):

    heading = ["Year", "DOY", "WAVRD", "WUPRD", "EOPD"]

    colspecs = [(1,5), (6, 9), (100, 105), (106, 111), (119, 123)]

    return dep.from_file_to_dataframe(index, dir, heading, colspecs, "PlantGrf")

def PlantGr2(index, dir):

    heading = ["Year", "DOY", "RL1D", "RL2D", "RL3D", "RL4D", "RL5D", "RL6D", "RL7D", "RL8D", "RL9D", "RL10D"]

    colspecs = [(1,5), (6, 9), (93, 99), (100, 105), (106, 111), (112, 117), (118, 123), (124, 129), (130, 135), (136, 141), (142, 147), (148, 153)]

    return dep.from_file_to_dataframe(index, dir, heading, colspecs, "PlantGr2")

def SoilWat(index, dir):

    heading = ["Year", "DOY", "SWTD", "SWXDS", "ROFC", "DRNC", "PREC", "IRRC", "SW1D", "SW2D", "SW3D", "SW4D", "SW5D", "SW6D", "SW7D", "SW8D"]

    colspecs = [(1,5), (6, 9), (16, 21), (22, 27), (29, 34), (36, 41), (43, 48), (56, 60), (96, 101), (104, 109), (112, 117), (120, 125), (128, 133), (136, 141), (144, 149), (152, 157)]

    return dep.from_file_to_dataframe(index, dir, heading, colspecs, "SoilWat")

def ET(index, dir):

    heading = ["Year", "DOY", "EOAA", "ETAA", "EPAA"]

    colspecs = [(1,5), (6, 9), (47, 52), (95, 100), (103, 108)]

    return dep.from_file_to_dataframe(index, dir, heading, colspecs, "ET")

def plot_R(trat, lista):

    print(f'\n Criando gráficos das {trat} simulações\n')

    r = "C:\\Program Files\\R\\R-3.6.1\\bin\\Rscript.exe"

    # Definir comando cmd
    cmd = [r, "dependencias/r_plot.R"] + [str(trat), ] + lista

    subprocess.run(cmd, shell=True)


def run_R(index, file, trat, mode):

    print(f'\n Processando "{file}".\n')
    # Executável do R:
    r = "C:\\Program Files\\R\\R-3.6.1\\bin\\Rscript.exe"

    # Definir comando cmd
    cmd = [r, "main.R"] + [str(trat), ] + index + [file, ] + [mode]

    # Rodar Script R
    subprocess.run(cmd, shell=True)
