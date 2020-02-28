import numpy as np


def space(x):
    if x < 10:
        return(f" {x}")
    return(x)


def write_head(file, filename, exp_name):
    exp_details = filename + "CS" + " " + exp_name

    file.write(f'*EXP.DETAILS: {exp_details}\n\n@PEOPLE\nFabio\n@ADDRESS\n-99\n@SITE\n-99\n*GENERAL\n@ PAREA  PRNO  PLEN  PLDR  PLSP  PLAY HAREA  HRNO  HLEN  HARM.........\n    -99   -99   -99   -99   -99   -99   -99   -99   -99   -99\n\n*TREATMENTS                        -------------FACTOR LEVELS------------\n@N R O C TNAME.................... CU FL SA IC MP MI MF MR MC MT ME MH SM\n')


def write_treatments(file, tratmatrix):

    if trat <= 9:
        for i, trat in enumerate(tratmatrix):
            file.write(f" {i} 1 1 0 {trat[0]}                      1  1  0  1  {trat[1]}  {trat[3]}  0  0  0  0  0  {trat[2]}  1\n")
    else:
        for i, trat in enumerate(tratmatrix[:9]):
            file.write(f" {i} 1 1 0 {trat[0]}                      1  1  0  1  {trat[1]}  {trat[3]}  0  0  0  0  0  {trat[2]}  1\n")

        for i, trat in enumerate(tratmatrix[9:]):
            file.write(f"{i} 1 1 0 {trat[0]}                      1  1  0  1 {space(trat[1])} {space(trat[3])}  0  0  0  0  0 {space(trat[2])}  1\n")
