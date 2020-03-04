from pathlib import Path

import subprocess
import re
import shutil
import sys
import os


def get_outputs(dir, mode="exp"):

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


def n_trat_out_file(file, mode):
    pattern = re.compile("@")
    ind = []
    for i, line in enumerate(open(f"C:/DSSAT47/{mode}/{file}")):
        for match in re.finditer(pattern, line):
            ind.append(str(i + 1))
    return len(ind), ind


def extract_outputs(dir, mode):

    dic = {"exp": "Cassava",
           "seas": "Seasonal"}

    # Rodar script R
    files = ["PlantGro.OUT", "Weather.OUT", "PlantGrf.OUT", "PlantGr2.OUT", "SoilWat.OUT", "ET.OUT"]  # Deixar PlantGro no início da lista porque esse output contém uma informação (DAP x DAS) que nem todas possuem.

    for file in files:

        # Número de tratamentos por arquivo e índices das tabelas
        trat_total, index = n_trat_out_file(file, mode=dic[mode])

        # Criar tabelas de resultados no R
        run_R(index, file, trat_total, mode=dic[mode])

    # Gerar Gráficos no R
    lista = []

    with os.scandir(dir) as entries:
        for entry in entries:
            if entry.name not in ["auxiliar.csv", "yieldFinal.csv"]:
                lista.append(entry.name)

    plot_R(trat_total, lista)


def run_R(index, file, trat, mode):

    print(f'\n Processando "{file}".\n')
    # Executável do R:
    r = "C:\\Program Files\\R\\R-3.6.1\\bin\\Rscript.exe"

    # Definir comando cmd
    cmd = [r, "main.R"] + [str(trat), ] + index + [file, ] + [mode]

    # Rodar Script R
    subprocess.run(cmd, shell=True)


def plot_R(trat, lista):

    print(f'\n Criando gráficos das {trat} simulações\n')

    r = "C:\\Program Files\\R\\R-3.6.1\\bin\\Rscript.exe"

    # Definir comando cmd
    cmd = [r, "dependencias/r_plot.R"] + [str(trat), ] + lista

    subprocess.run(cmd, shell=True)