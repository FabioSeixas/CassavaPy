import numpy as np
import math
from datetime import date
from datetime import timedelta as td


def format_name(x):

    while len(str(x)) < 3:
        x = "0" + str(x)
    return str(x)


def format_date(x):

    while len(str(x)) < 3:
        x = "0" + str(x)
    return x


def seq_data_irrig(numero, dap_from, dap_by, inicio):

    dates = [inicio + td(days=dap_from), ]
    for i in range(numero - 1):
        dates.append(dates[i] + td(days=dap_by))

    return [date.strftime("%y%j") for date in dates]


def seq_data_irrig_nf(DAP_list, inicio):

    date_list = []
    for i, DAP in enumerate(DAP_list):
        date_list.append(inicio + td(days=DAP))

    return [date.strftime("%y%j") for date in date_list]


def fix_PlantHarv(planting, harvest):
    if len(planting) != len(harvest):
        raise ValueError("\n\n Quantidade de datas de plantio e colheita não correspondem \n")

    tratmatrix = [[i + 1, i + 1] for i, n in enumerate(planting)]

    assert len(tratmatrix) < 100, "Quantidade de tratamentos ultrapassa o valor máximo (99)."

    return tratmatrix


def not_fix_PlantHarv(planting, harvest):

    matrix = []
    for i, plant_date in enumerate(planting):
        for n, harv in enumerate(harvest):
            temp = [i + 1, n + 1]
            matrix.append(temp)

    assert len(matrix) < 100, "Quantidade de tratamentos ultrapassa o valor máximo (99)."

    return matrix


def lamina_irrig(regs, laminas):

    lam_final = regs
    for i, n in enumerate(regs):
        lam_final[i] = [laminas[i], ] * len(n)

    return lam_final


def check_input_irnf(reg, laminas, reg_dict):
    ''' Essa função vai checar os inputs necessários para a irrigação no modo 'irnf'.
    '''

    if len(reg) != len(laminas):
        raise ValueError("\n\n Checagem dos Inputs encontrou um ERRO: Comprimentos de 'regs' e 'laminas' diferem.\n")

    for i, n in enumerate(reg):

        if isinstance(laminas[i], int):
            next

        elif len(laminas[i]) == 1:
            laminas[i] = laminas[i][0]

        else:
            try:
                np.column_stack((n, laminas[i]))
            except:
                raise ValueError(f"\n\n  Checagem dos Inputs encontrou um ERRO: \n  Comprimento do {i + 1}º elemento de 'reg' e 'laminas' não correspondem.\n")

    if not isinstance(reg_dict, dict):
        raise TypeError("\n\n Com design 'irnf', 'reg_dic' deve ser um dicionário \n")

    for k, v in reg_dict.items():
        if k > len(reg):
            raise AssertionError(f' No dicionário há referencia ao planejamento de irrigação nº {k}, no entanto apenas {len(reg)} planejamentos de irrigação foram definidos.')


def add_laminas(reg, laminas):

    if isinstance(laminas, int):
        temp = np.repeat(laminas, len(reg))
        result = np.column_stack((reg, temp))
    else:
        result = np.column_stack((reg, laminas))

    return [result.tolist(), ]


def add_laminas_nf(reg, laminas):

    result = reg
    for i, value in enumerate(reg):
        if isinstance(laminas[i], int):
            result[i] = np.column_stack((value, np.repeat(laminas[i], len(value))))
        else:
            result[i] = np.column_stack((value, laminas[i]))

    return result


def trat_insert_irrig_irf(dicionario, previus_matrix):

    new_matrix = []

    if dicionario == "NULL":

        for i, part in enumerate(previus_matrix):
            part.append(1)
            new_matrix.append(part)

        return new_matrix

    if isinstance(dicionario, dict):
        raise TypeError("\n\n Com design 'irf', 'reg_dic' deve ser uma lista \n")

    else:
        try:
            for i, part in enumerate(previus_matrix):
                if i + 1 in dicionario:
                    part.append(1)
                    new_matrix.append(part)
                else:
                    part.append(0)
                    new_matrix.append(part)
        except:
            raise ValueError("\n\n Erro na inserção da coluna irrigação na matrix de tratamentos a partir do dicionario \n")

        return new_matrix


def return_irrig(index_trat, dicionario):
    for k, v in dicionario.items():
        try:
            if index_trat in v:
                return k
        except:
            if index_trat == v:
                return k
    return 0


def trat_insert_irrig_irnf(dicionario, previus_matrix):

    new_matrix = []

    for i, trat in enumerate(previus_matrix):

        trat.append(return_irrig(i + 1, dicionario))
        new_matrix.append(trat)

    return new_matrix


def insert_all_rainfed(previus_matrix):
    new_matrix = []

    for i, trat in enumerate(previus_matrix):

        trat.append(0)
        new_matrix.append(trat)

    return new_matrix


def set_tratnames(tratmatrix, prefix):
    new_matrix = []

    for i, trat in enumerate(tratmatrix):

        trat.insert(0, prefix + format_name(i + 1))
        new_matrix.append(trat)

    return new_matrix
