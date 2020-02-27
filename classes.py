from datetime import date
from datetime import timedelta as td
import numpy as np

from dependencias import exp_functions as exp


class FileX:

    def __init__(self, filename, exp_name, design = "NULL"):
        self._filename = filename
        self._exp_name = exp_name
        self._design = design

    def set_planting(self, n_plant, p_from, p_by):
        self.p_from = date.fromisoformat(p_from)

        dates = []
        for i in range(n_plant):
            dates.append(self.p_from + td(days=p_by * i))

        self._planting = [date.strftime("%y%j") for date in dates]

    def set_harvest(self, n_harvest, h_from, h_by):
        h_from = date.fromisoformat(h_from)

        dates = []
        for i in range(n_harvest):
            dates.append(h_from + td(days=h_by * i))

        self._harvest = [date.strftime("%y%j") for date in dates]

    def set_simulation_start(self, sim_start):
        sim_start = date.fromisoformat(sim_start)
        self._sim_start = sim_start.strftime("%y%j")

    def set_field(self, field):
        self._field = field

    def set_genotype(self, genotype):
        self._genotype = genotype

    def set_irrigation(self, n_irrig="NULL", from_irrig="NULL", by_irrig="NULL", reg="NULL", laminas="NULL", reg_dict="NULL"):

        self._reg_dict = reg_dict

        if "irf" in self._design:

            self._irrig = exp.seq_data_irrig(n_irrig, from_irrig, by_irrig, self.p_from)

            try:
                self._irrig = exp.add_laminas(self._irrig, laminas)
            except:
                raise ValueError("\n\n ERRO: Comprimento de 'laminas' não e igual a 1. Quantidade de eventos de irrigação e comprimento de 'laminas' diferem.\n")

        if "irnf" in self._design:

            exp.check_input_irnf(reg, laminas)

            try:
                self._irrig = reg
                for i, DAP_list in enumerate(reg):

                    self._irrig[i] = exp.seq_data_irrig_nf(DAP_list, self.p_from)

            except:
                print("\nERRO: Não foi possível definir irrigação no modo 'irnf'.\n")

            self._irrig = exp.add_laminas_nf(self._irrig, laminas)

    def set_tratmatrix(self):

        if "phf" in self._design:

            self._tratmatrix = exp.fix_PlantHarv(self._planting, self._harvest)

        else:
            self._tratmatrix = exp.not_fix_PlantHarv(self._planting, self._harvest)

        if "irf" in self._design:

            self._tratmatrix = exp.trat_insert_irrig_irf(self._reg_dict, self._tratmatrix)

        if "IRNF" in self._design:
            self._detailsMatrix = np.array((self._detailsMatrix, self._irrig))
