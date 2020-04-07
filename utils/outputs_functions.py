from pathlib import Path

import numpy as np
import pandas as pd
import subprocess
import shutil
import sys
import os

from . import output_functions_dependencies as dep


def get_outputs(mode = "exp"):

    if mode == "exp":

        files = ["PlantGro.OUT", "Weather.OUT", "PlantGrf.OUT", "PlantGr2.OUT", "SoilWat.OUT", "ET.OUT"]

        all_outputs = pd.DataFrame(columns = ["Date", "Trat_n"])

        for file in files:

            # Índices das tabelas
            index = dep.n_trat_out_file(file)

            # Criar tabelas de resultados
            file_out = extract_by_file(index, file)

            # Merge tables
            all_outputs = pd.merge(all_outputs, file_out, how = "outer",
                                   on = ["Date", "Trat_n"])

        return all_outputs.sort_values(by = ["Trat_n", "Date"])

    elif mode == "seas":

        diretorio = 'C:/DSSAT47/Seasonal'

        return extract_seasonal(diretorio)

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

    heading = ["Year", "DOY", "DAP",
               "GSTD", # Growth Stage
               "PARID", # PAR Interception (%)
               "PARUD", # PAR utilization efficiency (g/MJ)
               "AWAD", # Assimilate Production
               "LAID", # Leaf Area Index
               "TWAD", # Tops + roots + storage wt (kg[dm]/ha)
               "RWAD", # Root Weight (kg[dm]/ha)
               "CWAD", # Tops Weight (kg[dm]/ha)
               "LWAD", # Leaf Weight (kg[dm]/ha)
               "HWAD", # Harvest Product (kg[dm]/ha)
               "HIAD", # Harvest Index (grain/top)
               "RDPD", # Root Depth (m)
               "SWXD", # Extractable Water (mm) -> plant point of view
               "WAVRD", # Water available to demand ratio (#)
               "WUPRD", # Water uptake to demand ratio (#)
               "WFPD", # Water factor for photosynthesis (0-1)
               "WFGD", # Water factor for growth (0-1)
               "TFPD", # Temperature factor for photosynthesis (0-1)
               "TFGD", ] # Temperature factor for growth (0-1)

    colspecs = [(1,5), (6, 9), (18, 21), (28, 33), (40, 45), (46, 51), (53, 57), (58, 63), (76, 81), (89, 93), (94, 99), (100, 105), (112, 117), (117, 123), (160, 165), (166, 171), (172, 177), (178, 183), (185, 189), (191, 195), (215, 219), (221, 225)]

    return dep.from_file_to_dataframe(index, dir, heading, colspecs, "PlantGro")


def Weather(index, dir):

    heading = ["Year", "DOY", "DAS",
               "PRED", # Precipitation depth (mm/d)
               "DAYLD", # Day length sunrise to sunset (hr)
               "SRAD", # Solar Radiation (MJ/m2/d)
               "CLDD", # Relative Cloudiness factor (0-1)
               "TMXD", # Maximum daily temperature (ºC)
               "TMND", # Minimum daily temperature (ºC)
               "TAVD", # Average daily temperature (ºC)
               "TDWD", # Dewpoint Temperature (ºC)
               "WDSD"] # Wind speed (km/d)

    colspecs = [(1,5), (6, 9), (11, 15), (17, 22), (24, 29), (39, 43), (53, 57), (60, 64), (67, 71), (74, 78), (88, 92), (109, 113)]

    return dep.from_file_to_dataframe(index, dir, heading, colspecs, "Weather")


def PlantGrf(index, dir):

    heading = ["Year", "DOY",
               "EOPD"] # Potential Transpiration (mm/d)

    colspecs = [(1,5), (6, 9), (119, 123)]

    return dep.from_file_to_dataframe(index, dir, heading, colspecs, "PlantGrf")

def PlantGr2(index, dir):

    heading = ["Year", "DOY",
               "RL1D", # Root Density, Soil Layer 1 (cm3/cm3)
               "RL2D", # Root Density, Soil Layer 2 (cm3/cm3) and so on...
               "RL3D", "RL4D", "RL5D", "RL6D", "RL7D", "RL8D", "RL9D", "RL10D"]

    colspecs = [(1,5), (6, 9), (93, 99), (100, 105), (106, 111), (112, 117), (118, 123), (124, 129), (130, 135), (136, 141), (142, 147), (148, 153)]

    return dep.from_file_to_dataframe(index, dir, heading, colspecs, "PlantGr2")

def SoilWat(index, dir):

    heading = ["Year", "DOY",
               "SWTD", # Total soil water in profile (mm)
               "SWXDS", # Extractable water (mm) -> soil point of view
               "ROFC", # Cumulative Runoff (mm)
               "DRNC", # Cumulative Drainage
               "PREC", # Cumulative Precipitation (mm)
               "IRRC", # Cumulative Effective Irrigation (mm)
               "SW1D", # Soil Water, Soil Layer 1 (cm3/cm3)
               "SW2D", # Soil Water, Soil Layer 2 (cm3/cm3) and so on...
               "SW3D", "SW4D", "SW5D", "SW6D", "SW7D", "SW8D"]

    colspecs = [(1,5), (6, 9), (16, 21), (22, 27), (29, 34), (36, 41), (43, 48), (56, 60), (96, 101), (104, 109), (112, 117), (120, 125), (128, 133), (136, 141), (144, 149), (152, 157)]

    return dep.from_file_to_dataframe(index, dir, heading, colspecs, "SoilWat")

def ET(index, dir):

    heading = ["Year", "DOY",
               "EOAA", # Average Potential Evapotranspiration (mm/d)
               "ETAA", # Average Evapotranspiration (mm/d)
               "EPAA"] # Average Plant transpiration (mm/d)

    colspecs = [(1,5), (6, 9), (47, 52), (95, 100), (103, 108)]

    return dep.from_file_to_dataframe(index, dir, heading, colspecs, "ET")

def extract_seasonal(dir):

    data = pd.read_fwf(f'{dir}/Summary.OUT',
                           skiprows = 3)

    return dep.set_dates_seasonal(data)

