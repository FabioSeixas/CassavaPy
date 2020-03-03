from pathlib import Path

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
        pass


def n_trat_out_file(file):
    pattern = re.compile("@")
    ind = []
    for i, line in enumerate(open(f"C:/DSSAT47/Cassava/{file}.OUT")):
        for match in re.finditer(pattern, line):
            ind.append(str(i + 1))
    return len(ind)


def extract_outputs():

    # Rodar script R
    files = ["PlantGro", "Weather", "PlantGrf", "PlantGr2", "SoilWat", "ET"]  # Deixar PlantGro no início da lista porque esse output contém uma informação (DAP x DAS) que nem todas possuem.

    for file in files:

        # Número de tratamentos por arquivo
        trat_total = n_trat_out_file()
        # Pegar os índices das tabelas
        index = functions.index_tables(file)
        # Criar tabelas de resultados no R
        functions.run_R(index, file, trat_total)

    # Gerar Gráficos no R
    lista = []

    with os.scandir(dir) as entries:
        for entry in entries:
            if entry.name not in ["auxiliar.csv", "yieldFinal.csv"]:
                lista.append(entry.name)

    functions.plot_R(trat_total, lista)
