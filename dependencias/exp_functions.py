import numpy as np
import math
from itertools import chain
from datetime import date
from datetime import timedelta as td
from collections import defaultdict as ddic


def format_name(x):

    while len(str(x)) < 3:
        x = "0" + str(x)
    return str(x)


def format_date(x):

    while len(str(x)) < 3:
        x = "0" + str(x)
    return x


def set_irrig_levels_irf(n_irrig, dap_from, dap_by, pdates, trat_list, laminas, design, hdates):

    if "phf" in design:

        return set_irrig_levels_irf_phf(n_irrig, dap_from, dap_by, pdates, trat_list, laminas)

    else:

        return set_irrig_levels_irf_no_phf(n_irrig, dap_from, dap_by, pdates, trat_list, laminas, hdates)


def set_irrig_levels_irf_phf(n_irrig, dap_from, dap_by, pdates, trat_list, laminas):

    irrig_levels = {}
    trat_irrig = {}
    levels_iter = iter(range(len(trat_list) + 1)[1:])

    if trat_list != "NULL":

        for i, date in enumerate(pdates):

            if (i + 1) in trat_list:

                dates = [date + td(days=dap_by) * n for n in range(n_irrig)]
                dates = [date.strftime("%y%j") for date in dates]
                irrig = add_laminas(dates, laminas)
                level = next(levels_iter)
                irrig_levels[level] = irrig
                trat_irrig[level] = i + 1
    else:
        for i, date in enumerate(pdates):

            dates = [date + td(days=dap_by) * n for n in range(n_irrig)]
            dates = [date.strftime("%y%j") for date in dates]
            irrig = add_laminas(dates, laminas)
            level = next(levels_iter)
            irrig_levels[level] = irrig
            trat_irrig[level] = i + 1

    return irrig_levels, trat_irrig


def set_irrig_levels_irf_no_phf(n_irrig, dap_from, dap_by, pdates, trat_list, laminas, hdates):

    irrig_levels = {}
    trat_irrig = ddic(list)
    date_irrig = {}
    levels_iter = iter(range(len(trat_list) + 1)[1:])

    for i, trat in enumerate(trat_list):

        pdate_n = math.ceil(trat / len(hdates))

        if pdate_n not in date_irrig.keys():

            level = next(levels_iter)
            date_irrig[pdate_n] = level

            try:
                date = pdates[pdate_n - 1]
            except:
                raise IndexError(" 'trat_irrig' contém tratamentos além dos definidos. \n ")

            dates = [date + td(days=dap_by) * n for n in range(n_irrig)]
            dates = [date.strftime("%y%j") for date in dates]
            irrig_levels[level] = add_laminas(dates, laminas)

        trat_irrig[date_irrig.get(pdate_n)].append(trat)

    return irrig_levels, trat_irrig


def dates_according_to_planting(DAP_list, inicio):

    date_list = []
    for i, DAP in enumerate(DAP_list):
        date_list.append(inicio + td(days=DAP))

    return [date.strftime("%y%j") for date in date_list]


def set_irrig_levels_irnf(reg, trat_irrig, pdates, design, hdates, laminas):

    irrigated_treatments = []
    for trat in chain.from_iterable(trat_irrig.values()):
        irrigated_treatments.append(trat)

    new_trat_irrig = []

    if "phf" in design:

        irrig_levels, trat_irrig = set_irrig_levels_and_new_trat_irrig(pdates, irrigated_treatments, trat_irrig, reg, laminas)
    else:
        for trat_n in irrigated_treatments:
            pdate = math.ceil(trat_n / len(hdates))
            n_reg = return_irrig(index_trat=trat_n, dicionatio=trat_irrig)
            dates_list = dates_according_to_planting(reg[n_reg], pdates[pdate])
            if dates_list not in new_trat_irrig:
                new_trat_irrig.append(dates_list)

    return irrig_levels, trat_irrig


def set_irrig_levels_and_new_trat_irrig(pdates, irrigated_treatments, trat_irrig, reg, laminas):

    irrig_levels = {}

    for i, pdate in enumerate(pdates):

        # If the irrigation schedule was applied for the plant date:
        if (i + 1) in irrigated_treatments:
            n_reg = return_irrig(index_trat=i + 1, dicionario=trat_irrig)
            dates_list = dates_according_to_planting(reg[n_reg - 1], pdates[i])

            # Put the treatment(w specific plant date) on a new irrigation schedule
            if irrig_levels.__contains__(n_reg):
                irrig_levels[len(trat_irrig) + 1] = add_laminas(dates_list, laminas[n_reg - 1])
                to_update_trat_irrig = {(len(trat_irrig) + 1): [i + 1]}

                for v in trat_irrig.values():

                    if isinstance(v, int):
                        continue
                    if (i + 1) in v:
                        v.remove(i + 1)

                trat_irrig.update(to_update_trat_irrig)

            else:
                irrig_levels[n_reg] = add_laminas(dates_list, laminas[n_reg - 1])

    return irrig_levels, trat_irrig


def fix_PlantHarv(planting, harvest):
    if len(planting) != len(harvest):
        raise ValueError(" Com design 'phf' o número de datas de plantio de colheita devem ser iguais")

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


def check_input_irnf(reg, laminas, trat_irrig, pdates, design, hdates):
    ''' Essa função vai checar os inputs necessários para a irrigação no modo 'irnf'.
    '''

    if "phf" in design:
        if len(hdates) != len(pdates):
            raise ValueError(" Com design 'phf' o número de datas de plantio de colheita devem ser iguais")
        max_n_trat = len(pdates)
    else:
        max_n_trat = len(hdates) * len(pdates)

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

    if not isinstance(trat_irrig, dict):
        raise TypeError("\n\n Com design 'irnf', 'reg_dic' deve ser um dicionário \n")

    for k, v in trat_irrig.items():

        if isinstance(v, int):
            trat_irrig[k] = list([v])

        if k > len(reg):
            raise AssertionError(f' No dicionário há referencia ao planejamento de irrigação nº {k}, no entanto apenas {len(reg)} planejamentos de irrigação foram definidos.')

        for trat in chain(trat_irrig[k]):
            if trat > max_n_trat:
                raise IndexError(f' No dicionário há referencia ao tratamento {trat}, no entanto, só foram definidos {max_n_trat} tratamentos. ')

    return trat_irrig


def add_laminas(irrig_dates, laminas):

    if isinstance(laminas, int) or len(laminas) == 1:

        extended_laminas = np.repeat(laminas, len(irrig_dates))
        return np.column_stack((irrig_dates, extended_laminas)).tolist()

    else:
        try:
            return np.column_stack((irrig_dates, laminas)).tolist()
        except:
            raise ValueError("\n\n ERRO: Comprimento de 'laminas' não é igual a 1. Quantidade de eventos de irrigação e comprimento de 'laminas' diferem.\n")


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
