from datetime import date
from datetime import timedelta as td
import numpy as np
import re

from dependencias import exp_functions as exp
from dependencias import write_functions as w_file


class FileX:

    def __init__(self, filename, exp_name, design="NULL"):
        self._filename = filename
        self._exp_name = exp_name
        self._design = design

        if "irf" in self._design and "irnf" in self._design:
            raise AttributeError("\n\n Não é possível definir 'design' como 'irf' e 'irnf' ao mesmo tempo \n")

    def set_planting(self, n_plant, p_from, p_by):
        self.p_from = date.fromisoformat(p_from)

        dates = []
        for i in range(n_plant):
            dates.append(self.p_from + td(days=p_by * i))

        self._planting = dates
        #self._planting = [date.strftime("%y%j") for date in dates]

    def set_harvest(self, n_harvest, h_from, h_by):
        h_from = date.fromisoformat(h_from)

        dates = []
        for i in range(n_harvest):
            dates.append(h_from + td(days=h_by * i))

        self._harvest = [date.strftime("%y%j") for date in dates]

    def set_simulation_start(self, sim_start):
        sim_start = date.fromisoformat(sim_start)
        self._sim_start = sim_start.strftime("%y%j")

    def set_field(self, code_id, soil_id):
        self._field = code_id, soil_id

    def set_genotype(self, genotype):
        self._genotype = genotype

    def set_irrigation(self, n_irrig="NULL", from_irrig="NULL", by_irrig="NULL", reg="NULL", laminas="NULL", reg_dict="NULL"):

        self._reg_dict = reg_dict

        if "irf" in self._design:

            self._irrig = exp.seq_data_irrig(n_irrig, from_irrig, by_irrig, self._planting)

            try:
                self._irrig = exp.add_laminas(self._irrig, laminas)
            except:
                raise ValueError("\n\n ERRO: Comprimento de 'laminas' não é igual a 1. Quantidade de eventos de irrigação e comprimento de 'laminas' diferem.\n")

        if "irnf" in self._design:

            exp.check_input_irnf(reg, laminas, self._reg_dict)

            try:
                self._irrig = reg
                for i, DAP_list in enumerate(reg):

                    self._irrig[i] = exp.seq_data_irrig_nf(DAP_list, self.p_from)
            except:
                print("\nERRO: Não foi possível definir irrigação no modo 'irnf'.\n")

            self._irrig = exp.add_laminas_nf(self._irrig, laminas)

    def set_tratmatrix(self, tnames_prefix):

        if "phf" in self._design:

            self._tratmatrix = exp.fix_PlantHarv(self._planting, self._harvest)

        else:
            self._tratmatrix = exp.not_fix_PlantHarv(self._planting, self._harvest)

        if "irf" in self._design:

            self._tratmatrix = exp.trat_insert_irrig_irf(self._reg_dict, self._tratmatrix)

        elif "irnf" in self._design:
            self._tratmatrix = exp.trat_insert_irrig_irnf(self._reg_dict, self._tratmatrix)

        else:
            self._tratmatrix = exp.insert_all_rainfed(self._tratmatrix)

        self._tratmatrix = exp.set_tratnames(self._tratmatrix, tnames_prefix)


class Experimental(FileX):

    def write_file(self):

        with open(f"C:/DSSAT47/Cassava/{self._filename}.CSX", mode="w") as file:

            # Head
            w_file.write_head(file, self._filename, self._exp_name)

            # Treatments
            w_file.write_treatments(file, self._tratmatrix)

            # Cultivar
            w_file.write_cultivars(file, self._genotype)

            # Fields
            w_file.write_field(file, self._field)

            # Initial Conditions
            w_file.write_initial_conditions(file, self._sim_start)

            # Planting
            w_file.write_planting(file, self._planting)

            # Irrigation
            w_file.write_irrigation(file, self._irrig)

            # Harvest
            w_file.write_harvest(file, self._harvest)

            # Controls
            w_file.write_controls(file, self._sim_start)

        print(f'\n Arquivo "{self._filename}.CSX" disponível em C:/DSSAT47/Cassava')


class Seasonal(FileX):

    def write_file(self):

        with open(f"C:/DSSAT47/Seasonal/{self._filename}.SNX", mode="w") as file:

            # Head
            w_file.write_head(file, self._filename, self._exp_name, mode="SN")

            # Treatments
            w_file.write_treatments(file, self._tratmatrix)

            # Cultivar
            w_file.write_cultivars(file, self._genotype)

            # Fields
            w_file.write_field(file, self._field)

            # Initial Conditions
            w_file.write_initial_conditions(file, self._sim_start)

            # Planting
            w_file.write_planting(file, self._planting)

            # Irrigation
            w_file.write_irrigation(file, self._irrig)

            # Harvest
            w_file.write_harvest(file, self._harvest)

            # Controls
            w_file.write_controls(file, self._sim_start, reps=30, mode="seas")

        print(f'\n Arquivo "{self._filename}.SNX" disponível em C:/DSSAT47/Seasonal')
