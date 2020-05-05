from .filex import FileX

from . import write_functions as w_file


class Experimental(FileX):
    """
    Class to create Experimental files
    """

    def write_file(self):
        """
        Method to write the Experimental file. Must be executed after all the preparation.
        """

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
            w_file.write_planting(file, self._planting_julian)

            # Irrigation
            try:
                w_file.write_irrigation(file, self._irrig)
            except:
                pass

            # Harvest
            w_file.write_harvest(file, self._harvest)

            # Controls
            w_file.write_controls(file, self._sim_start)

        print(f'\n "{self._filename}.CSX" file available at C:/DSSAT47/Cassava')


class Seasonal(FileX):
    """
    Class to create Seasonal files
    """

    def write_file(self):
        """
        Method to write the Seasonal file. Must be executed after all the preparation.
        """

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
            w_file.write_planting(file, self._planting_julian)

            # Irrigation
            try:
                w_file.write_irrigation(file, self._irrig)
            except:
                pass

            # Harvest
            w_file.write_harvest(file, self._harvest)

            # Controls
            w_file.write_controls(file, self._sim_start, years=31, mode="seas")

        print(f'\n "{self._filename}.SNX" file available at C:/DSSAT47/Seasonal')
