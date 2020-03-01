
def write_batch(files, mode="exp"):

    if isinstance(files, str):
        files = [files]

    n_trats = []

    for file in files:
        n_trats.append(count_treatments(file))

    return n_trats


def count_treatments(file):

    pattern_trat = re.compile("TREATMENTS")
    pattern_gen = re.compile("CULTIVARS")
    ind = []

    for i, line in enumerate(open(f"C:/DSSAT47/Cassava/{file}.CSX")):

        for match in re.finditer(pattern_trat, line):
            ind.append(i + 1)

        for match in re.finditer(pattern_gen, line):
            ind.append(i + 1)

    return (ind[1] - ind[0] - 3)
