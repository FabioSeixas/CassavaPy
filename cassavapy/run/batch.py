
import numpy as np
import subprocess
import re


def space(x):
    if int(x) > 99:
        return f"{x}"

    elif int(x) > 9:
        return f" {x}"
    return f"  {x}"


def write_batch(files, mode="exp"):

    if isinstance(files, str):
        files = [files]

    n_trats = []

    for file in files:
        n_trats.append(count_treatments(file, mode=mode))

    final_list = np.column_stack((files, n_trats)).tolist()

    if "exp" in [mode]:
        write_experimental(final_list)

        print("\n Batch file disponível em C:/DSSAT47/Cassava/DSSBatch.v47. \n")

    elif "seas" in [mode]:
        write_seasonal(final_list)

        print("\n Batch file disponível em C:/DSSAT47/Seasonal/DSSBatch.v47. \n")

    else:
        raise ValueError(f" Valor '{mode}' não reconhecido para o argumento 'mode'. ")


def count_treatments(file, mode="exp"):

    dic = {"exp": ["Cassava",
                   "CSX"],
           "seas": ["Seasonal",
                    "SNX"]}

    pattern_trat = re.compile("TREATMENTS")
    pattern_gen = re.compile("CULTIVARS")
    ind = []

    for i, line in enumerate(open(f"C:/DSSAT47/{dic[mode][0]}/{file}.{dic[mode][1]}")):

        for match in re.finditer(pattern_trat, line):
            ind.append(i + 1)

        for match in re.finditer(pattern_gen, line):
            ind.append(i + 1)

    return (ind[1] - ind[0] - 3)


def write_experimental(final_list):
    with open("C:/DSSAT47/Cassava/DSSBatch.v47", mode="w") as file:

        # Head
        file.write("$BATCH(CASSAVA) \n\n")
        file.write("@FILEX                                                                                        TRTNO     RP     SQ     OP     CO \n")

        # Simulations
        for file_name, n_trat in final_list:
            for i in range(int(n_trat)):
                file.write("C:\\DSSAT47\\CASSAVA\\")
                file.write(file_name)
                file.write(".CSX")
                file.write("                                                                 ")
                file.write(space(str(i + 1)))
                file.write("      1      0      1      0\n")


def write_seasonal(final_list):
    with open("C:/DSSAT47/Seasonal/DSSBatch.v47", mode="w") as file:

        # Head
        file.write("$BATCH(SEASONAL) \n\n")
        file.write("@FILEX                                                                                        TRTNO     RP     SQ     OP     CO \n")

        # Simulations
        for file_name, n_trat in final_list:
            for i in range(int(n_trat)):
                file.write("C:\\DSSAT47\\SEASONAL\\")
                file.write(file_name)
                file.write(".SNX")
                file.write("                                                                ")
                file.write(space(str(i + 1)))
                file.write("      1      0      1      0\n")


def run_batch(mode="exp"):

    dic = {"exp": ["Experimental",
                   "Cassava"],
           "seas": ["Seasonal",
                    "Seasonal"]}

    if any(item in [mode] for item in dic):

        print(f"\n Rodando Simulações do DSSAT no modo '{dic[mode][0]}' \n")

        subprocess.run("C:\\DSSAT47\\DSCSM047.EXE CSYCA047 B DSSBatch.v47",
                       shell=True,
                       cwd=f"C:/DSSAT47/{dic[mode][1]}")

    else:
        raise ValueError(f" Valor '{mode}' não reconhecido para o argumento 'mode'. ")
