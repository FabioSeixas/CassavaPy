
*********************
What CassavaPy can do
*********************

The following explanation assume knowledge about DSSAT.

DSSAT allows the user to change any factor between environment, crop, genotype and management. Here, the focus is on:

#. Cassava crop (and the MANIHOT model)
#. Planting dates
#. Harvest dates
#. Irrigation management

That said, there are two ways for which a factor (gentoype, planting dates etc) can be changed:

#. Inside the ``.EXP`` or ``.SNX`` files. The factor and its variable values are defined within the file. ``Planting Dates``, ``Harvest Dates`` and ``Irrigation management`` are in that category.

#. The variable factor is unique by file. You will have to make as many files as values you need to vary the factor. ``Genotype``, ``Field``, ``Simulation Start Date``, ``Simulation Controls`` and ``Initial Conditions`` are in that category.

Since setting the last factors is straightforward, here you will find how to set the first.

Go to next section to read about ``designs``.
