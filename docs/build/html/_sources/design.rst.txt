
******
Design
******


Each Experimental (or Seasonal) file must have a design. But what is it?

Design was the solution we used to manage combinations of factors. For instance, I want to simulate  cassava production varying the cycle length. That means I have **One Planting Date** and **n Harvest Dates**. That gives us that:

========    =======
Planting    Harvest
========    =======
Plan 1       Harv 1
Plan 1       Harv 2
Plan 1       Harv 3
Plan 1       Harv 4
========    =======

This is called *not fixed planting-harvest*. I will understand why soon. In *not fixed planting-harvest* setting, each planting date is combined with all harvest dates.

Total number of treatments are equal to: **n planting** x **n harvest**.

It is different from *fixed planting-harvest*. If I set three planting dates and three harvest dates, using the *fixed planting-harvest*, I will get:

========    =======
Planting    Harvest
========    =======
Plan 1       Harv 1
Plan 2       Harv 2
Plan 3       Harv 3
========    =======

As you can see, number of planting and harvest dates must match.

Total number of treatments are equal to: **n planting**.

You will have to choose what design you will use when you are creating your instance::

    myInstance = Experimental(filename = "myFile",
                              exp_name = "myExperiment",
                              design = "phf")

In the code above we choosed the *fixed planting-harvest* design. The *not fixed planting-harvest* is the default.

.. note::
    Until now, treatment number by file is limited to 99. If your simulation need more than that, you will have to "break" your treatments in more files. In the run moment, you can run all together.


Irrigation Designs
^^^^^^^^^^^^^^^^^^

Designs are used for planting-harvest combinations, but also for irrigation. If you are using irrigation in your simulations, you will have to choose a design based on what you want.

There is three options for irrigation designs:

#. All rainfed (default)
#. ``irf`` - fixed irrigation
#. ``irnf`` - not fixed irrigation

**Fixed irrigation** means that you will set an "fixed" irrigation schedule and will choose for which treatments it will be applied. For instance:

=========   ========    =======  ==========
Treatment   Planting    Harvest  Irrigation
=========   ========    =======  ==========
 1          Plan 1       Harv 1  Irrig
2           Plan 2       Harv 2  Rainfed
 3          Plan 3       Harv 3  Irrig
=========   ========    =======  ==========

In the design above, treatments **One** and **Three** are receiving the same irrigation management. That means they are receiving the same amount of water in the same DAP's (days after planting) defined by the user.

By the other hand, in the **Not fixed irrigation** setting the user define as many irrigation schedules as he want and combine each with treatments. The following table shows the concept.

=========   ========    =======  ==========
Treatment   Planting    Harvest  Irrigation
=========   ========    =======  ==========
 1          Plan 1       Harv 1  Irrig 1
2           Plan 1       Harv 2  Rainfed
 3          Plan 2       Harv 1  Irrig 2
 4          Plan 2       Harv 2  Irrig 1
=========   ========    =======  ==========

In the design above we defined two irrigation schedules and apply the first to treatments **One** and **Four**, and the second to treatment **Three**. Treatments **One** and **Four** are receiving the same amount of water in the same DAP's (days after planting) defined by the schedule 1 (*Irrig 1*). Treatment **Three**, however, are receiving a different irrigation management.

You may be noted that in the last design (table) we used the *not fixed planting-harvest* setting with **two Planting Dates** and **two Harvest Dates**. We could use the *fixed planting-harvest* instead, with **four Planting Dates** and **four Harvest Dates**.

=========   ========    =======  ==========
Treatment   Planting    Harvest  Irrigation
=========   ========    =======  ==========
 1          Plan 1       Harv 1  Irrig 1
2           Plan 2       Harv 2  Rainfed
 3          Plan 3       Harv 3  Irrig 2
 4          Plan 4       Harv 4  Irrig 1
=========   ========    =======  ==========

To reproduce the design above, write that when you are creating your instance::

    myInstance = Experimental(filename = "myFile",
                              exp_name = "myExperiment",
                              design = ["phf", "irnf"])

If you are interested in the *fixed irrigation* with *fixed planting-harvest* design ::

    myInstance = Experimental(filename = "myFile",
                              exp_name = "myExperiment",
                              design = ["phf", "irf"])

Or maybe *fixed irrigation* with *not fixed planting-harvest* design ::

    myInstance = Experimental(filename = "myFile",
                              exp_name = "myExperiment",

                              # not fixed planting-harvest is the default
                              design = "irf")
