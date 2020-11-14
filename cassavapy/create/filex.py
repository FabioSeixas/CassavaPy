from datetime import date
from datetime import timedelta as td
import numpy as np
from itertools import chain

from .soil import Soil
from . import exp_functions as exp


class FileX:
    """
    Parent class for all Files (Experimental and Seasonal)
    """

    def __init__(self, filename, exp_name, design="NULL"):
        """
        Init a Filex instance.

        Parameters
        ----------
            filename: str
                The filename before the extension "".CSX"".
                Usually DSSAT uses four letters followed by four numbers.

            exp_name: str
                Experiment name.

            design: str | list of str
                Control argument for experiment design purpose. For planting-harvest control,
                "phf" (planting-harvest fixed) can be passed. For irrigation control, "irf" or
                "irnf" can be passed (not both). Default is "NULL", meaning rainfed and not fixed
                planting-harvest experiment. For the meaning of each of these, see documentation.

        Returns
        -------
            A FileX instance.
        """

        self._filename = filename
        self._exp_name = exp_name
        self._design = design

        if "irf" in self._design and "irnf" in self._design:
            raise AttributeError("\n\n Não é possível definir 'design' como 'irf' e 'irnf' ao mesmo tempo \n")

    def set_planting(self, n_plant, p_from, p_by, year, p_list=None, method="seq"):
        """
        Method to define planting dates. It uses date sequence logic.

        Parameters
        ----------
            n_plant: int
                number of planting dates

            p_from: str
                The start date of the sequence. Must be a 'dd-mm-yyyy' date ('01-05-2020').

            p_by: int
                Interval between one date and the next of the sequence

        """
        if method == "seq":
            self.p_from_original = date.fromisoformat(p_from)

            self.p_from = self.p_from_original.replace(year = year)

            dates = []
            for i in range(n_plant):
                dates.append(self.p_from + td(days=p_by * i))

            self._planting = dates

            # Workaround for 'december 31' (subtract one day).
            # Julian convertion sometimes fails and simulation crashes.
            self._planting = [(my_date - td(days=1))
                            if (my_date.month == 12 and my_date.day == 31)
                            else my_date
                            for my_date in self._planting]

            self._planting_julian = [date.strftime("%y%j") for date in self._planting]

        elif method == "list":
            
            self.p_from_original = date.fromisoformat(p_list[0])
            self._planting = [date.fromisoformat(item) for item in p_list]

            planting_list_years = [item.year for item in self._planting]
            unique_years = list(set(planting_list_years))

            if len(unique_years) > 1:

                new_unique_years = [year + n for n in range(len(unique_years))]

                # The way It is written, It allows only two years consecutively
                self._planting = [my_date.replace(year = new_unique_years[0])
                                  if my_date.year == unique_years[0]
                                  else my_date.replace(year = new_unique_years[1])
                                  for my_date in self._planting]

            # Workaround for 'december 31' (subtract one day).
            # Julian convertion sometimes fails and simulation crashes.
            self._planting = [(my_date - td(days=1))
                            if (my_date.month == 12 and my_date.day == 31)
                            else my_date
                            for my_date in self._planting]

            self._planting_julian = [date.strftime("%y%j") for date in self._planting]

        else:
            raise AttributeError(f"\n\n Valor '{method}' não reconhecido para o argumento 'method' \n")



    def set_harvest(self, n_harvest, h_from, h_by, year, h_list=None, h_dap=None, method="seq"):
        """
        Method to define harvest dates. It uses date sequence logic.

        Parameters
        ----------
            n_harvest: int
                number of harvest dates

            h_from: str
                The start date of the sequence. Must be a 'dd-mm-yyyy' date ('01-05-2020').

            h_by: int
                Interval between one date and the next of the sequence
        """
        if method == "seq":
            h_from = date.fromisoformat(h_from)

            planting_harvest_difference = h_from.year - self.p_from_original.year

            h_from = h_from.replace(year = year + planting_harvest_difference)

            dates = []
            for i in range(n_harvest):
                dates.append(h_from + td(days=h_by * i))

            self._harvest = [date.strftime("%y%j") for date in dates]
        
        elif method == "list":

            self._harvest = [date.fromisoformat(item) for item in h_list]

            harvest_list_years = [item.year for item in self._harvest]
            original_unique_years = list(set(harvest_list_years))
            current_unique_years = [year + n for n in range(len(original_unique_years))]
            
            planting_harvest_difference = original_unique_years[0] - self.p_from_original.year

            if not ((original_unique_years[0] - current_unique_years[0]) >= planting_harvest_difference):
                dic = {key: value + planting_harvest_difference for key, value 
                       in zip(original_unique_years, current_unique_years)}

                self._harvest = [item.replace(year = dic[item.year]) for item in self._harvest]

            # Workaround for 'december 31' (subtract one day).
            # Julian convertion sometimes fails and simulation crashes.
            self._harvest = [(my_date - td(days=1))
                            if (my_date.month == 12 and my_date.day == 31)
                            else my_date
                            for my_date in self._harvest]

            self._harvest = [date.strftime("%y%j") for date in self._harvest]

        elif method == "dap":
            
            if "phf" not in self._design:
                raise ValueError("havest method 'dap' must be used with 'phf' design.")

            self._harvest = [p_date + td(days=int(h_dap)) for p_date in self._planting]
            self._harvest = [date.strftime("%y%j") for date in self._harvest]

        else:
            raise AttributeError(f"\n\n Valor '{method}' não reconhecido para o argumento 'method' \n")


    def set_controls(self, sim_start, date_start = None, years=1, auto_irrigation=None):
        """
        Method to define simulation start date and soil water available at the simulation beginning.

        Parameters
        ----------
            sim_start: str
                Must be "P" (simulation start on planting) or "S" (simulation start on a specified date). If "S", the "date_start" argument is necessary.

            date_start: str
                Obligatory if "sim_start" is "S". Must be a 'dd-mm-yyyy' date ('01-05-2020').
            

        """
        self._sim_start = sim_start

        if date_start is not None:
            date_start = date.fromisoformat(date_start)
            self._date_start = date_start.strftime("%y%j")

        self.years = years

        if auto_irrigation:
            self.auto_irrig = "A"
            self.auto_irrig_method = auto_irrigation["method"]
            self.auto_irrig_depth = auto_irrigation["management_depth"]
            self.auto_irrig_threshold = auto_irrigation["threshold"]
            self.auto_irrig_endpoint = auto_irrigation["end_point"]
            self.auto_irrig_effic = auto_irrigation["efficiency"]
        else: 
            self.auto_irrig = "R"
            self.auto_irrig_method = "04"
            self.auto_irrig_depth = 60
            self.auto_irrig_threshold = 60
            self.auto_irrig_endpoint = 100
            self.auto_irrig_effic = 0.8


    def set_field(self, code_id, soil_id, water=1):
        """
        Method to define simulation field.

        Parameters
        ----------
            water: int
                Value between 0 and 1 (0% - 100%) meaning percentage of soil water

            code_id: str
                DSSAT ID for the weather station (found on .WTH files)

            soil_id: str
                DSSAT ID for the soil (found on .SOIL files)
        """

        if water < 0 or water > 1:
            raise ValueError(f"value {water} for 'water' parameter invalid")

        self._field = code_id, soil_id
        self.soil_params = Soil(soil_id).params

        self._water_available(water)

    def set_genotype(self, genotype):
        """
        Method to define genotypes. For each genotype inserted the tratment number is doubled.

        Parameters
        ----------
            genotype: list of tuples
                each tuple must have two string elements
                The first element is the ecotype code (ex: 'UC0007')
                The second element is the genotype code ('MCol-1684')
        """

        self._genotype = exp.validate_genotype_input(genotype)

    def set_irrigation(self, laminas, n_irrig="NULL", from_irrig="NULL", by_irrig="NULL",
                       reg="NULL", trat_irrig="NULL"):
        """
        Method to define irrigation.
        If "irf" design is set, parameters 'laminas', 'n_irrig', 'from_irrig' and 'by_irrig'
        are mandatory and a DAP (days after planting) sequence logic is used. If "irnf" design is
        set, parameters 'laminas', 'reg' and 'trat_irrig' are mandatory and DAP must be setted
        manually.

        Parameters
        ----------
            laminas: int | list of int | list of lists

                water depth applied.

                If it is an int, all treatments and application events will receive the same amount
                of water.

                If it is one list, each list element will correspond to an irrigation event.
                A list of nine elements will correspond to a treatment with nine irrigation events.
                By that way each water depth can be manually defined.

                If it is a list of lists, each list element will be one irrigation treatment.
                Example: '[[10, 20, 15], [5, 4, 6, 5]]' correspond to two irrigation treatments, the
                first with three events and the second with four events.

            n_irrig: int
                Total irrigation events.

            from_irrig: int
                The DAP (days after planting) for the first irrigation event.

            by_irrig: int
                Interval between one irrigation event and the next of the sequence.

            reg: list of int | list of lists
                The irrigation schedule. Each value correspond to a DAP. Must be ordered in
                increasing order.

                If it is one list, each list element will correspond to an irrigation event.
                A list of nine elements will correspond to a treatment with nine irrigation events.

                If it is a list of lists, each list element will be one irrigation treatment.
                Example: '[[5, 9, 13], [2, 4, 6, 10]]' correspond to two irrigation treatments, the
                first with three events and the second with four events.

            trat_irrig: dic
                A dictionary linking each irrigation treatment (key) to one or more experiment
                treatment (value). The value can be an int or a list of int.

        """

        self._trat_irrig = trat_irrig

        if "irf" in self._design:

            self._irrig, self._trat_irrig = exp.set_irrig_levels_irf(n_irrig, from_irrig, by_irrig, self._planting, self._trat_irrig, laminas, self._design, self._harvest)

        if "irnf" in self._design:

            self._trat_irrig = exp.check_input_irnf(reg, laminas, self._trat_irrig, self._planting, self._design, self._harvest)

            self._irrig, self._trat_irrig = exp.set_irrig_levels_irnf(reg, self._trat_irrig, self._planting, self._design, self._harvest, laminas)

    def set_tratmatrix(self, tnames_prefix):
        """
        After run all necessary 'set_*' functions, this method closes the File preparation and set
        the treatment matrix.

        Parameters
        ----------

            tnames_prefix: str
                A code for all treatments inside this file. Can be usefull if you run more
                than one file per time.
        """
        if "phf" in self._design:
            self._tratmatrix = exp.fix_PlantHarv(self._planting, self._harvest)
        else:
            self._tratmatrix = exp.not_fix_PlantHarv(self._planting, self._harvest)

        if "irf" in self._design or "irnf" in self._design:
            self._tratmatrix = exp.trat_insert_irrig(self._trat_irrig, self._tratmatrix)
        else:
            self._tratmatrix = exp.insert_all_rainfed(self._tratmatrix)

        # To insert more than one genotype by file
        genotype_list = [[i] * len(self._tratmatrix) for i in range(1, len(self._genotype) + 1)]
        genotype_list = list(chain.from_iterable(genotype_list))

        self._tratmatrix = self._tratmatrix * len(self._genotype)  # reference trap!

        new_tratmatrix = []
        for i, gen_id in enumerate(genotype_list):
            trat = self._tratmatrix[i][:]      # '[:]' get the value instead of reference
            trat.insert(0, gen_id)
            new_tratmatrix.append(trat)

        self._tratmatrix = exp.set_tratnames(new_tratmatrix, tnames_prefix)

    def _water_available(self, water):

        self.soil_params["SH2O"] = [round(w * water + self.soil_params["SLLL"][i], 3)
                                    for i, w in enumerate(self.soil_params["SH2O"])]
