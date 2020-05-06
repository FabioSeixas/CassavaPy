
********************
The simplest example
********************

Import modules::

    from cassavapy import Experimental

Create the Experimental instance::

    myInstance = Experimental(filename = "myFile",
                              exp_name = "myExperiment")

Set the necessary experimental information::

    # Planting dates
    myInstance.set_planting(n_plant = 2,
                            p_from = "2010-10-15",
                            p_by = 30)

    # Harvest dates
    myInstance.set_harvest(n_harvest = 2,
                           h_from = "2011-10-15",
                           h_by = 30)

    # Genotype
    myInstance.set_genotype(genotype = ["UC0006",
                                        "MCol-1684"])

    # Field
    myInstance.set_field(code_id = "BACR",
                         soil_id = "IB00000002")

    # Simulation Start Date
    myInstance.set_simulation_start('2010-05-01')

When all is defined, create the treatment matrix just by::

    myInstance.set_tratmatrix(tnames_prefix = "BA")

And write the .EXP file::

    myInstance.write_file()
    >> myFile.CSX file available at C:/DSSAT47/Cassava

