from datetime import date
from datetime import timedelta as td
import numpy as np

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

    def set_planting(self, n_plant, p_from, p_by):
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

        self.p_from = date.fromisoformat(p_from)

        dates = []
        for i in range(n_plant):
            dates.append(self.p_from + td(days=p_by * i))

        self._planting = dates

        # Little modification for 'december 31' (subtract one day).
        # Julian convertion sometimes fails and simulation crashes.
        self._planting = [(my_date - td(days=1))
                          if (my_date.month == 12 and my_date.day == 31)
                          else my_date
                          for my_date in self._planting]

        self._planting_julian = [date.strftime("%y%j") for date in self._planting]

    def set_harvest(self, n_harvest, h_from, h_by):
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

        h_from = date.fromisoformat(h_from)

        dates = []
        for i in range(n_harvest):
            dates.append(h_from + td(days=h_by * i))

        self._harvest = [date.strftime("%y%j") for date in dates]

    def set_simulation_start(self, sim_start):
        """
        Method to define simulation start date.

        Parameters
        ----------
            sim_start: str
                Must be a 'dd-mm-yyyy' date ('01-05-2020').
        """

        sim_start = date.fromisoformat(sim_start)
        self._sim_start = sim_start.strftime("%y%j")

    def set_field(self, code_id, soil_id):
        """
        Method to define simulation field.

        Parameters
        ----------
            code_id: str
                DSSAT ID for the weather station (found on .WTH files)

            soil_id: str
                DSSAT ID for the soil (found on .SOIL files)
        """

        self._field = code_id, soil_id

    def set_genotype(self, genotype):
        """
        Method to define the genotype.

        Parameters
        ----------
            genotype: list of two str
                genotype DSSAT code (found on .CUL files)
                The first element is the ecotype code
                The second element is the genotype code
        """

        self._genotype = genotype

    def set_irrigation(self, laminas, n_irrig="NULL", from_irrig="NULL", by_irrig="NULL",
                       reg="NULL", trat_irrig="NULL"):
        """
        Method to define irrigation.
        If "irf" design is setting, parameters 'laminas', 'n_irrig', 'from_irrig' and 'by_irrig'
        are mandatory and a DAP (days after planting) sequence logic is used. If "irnf" design is
        setting, parameters 'laminas', 'reg' and 'trat_irrig' are mandatory and DAP must be setted
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
        After run all necessary 'set_*' functions, this method closes the File preparation setting
        the treatment matrix.

        Parameters
        ----------

            tnames_prefix: str
                An user code for all treatments inside this file. Can be usefull if you run more
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

        self._tratmatrix = exp.set_tratnames(self._tratmatrix, tnames_prefix)
