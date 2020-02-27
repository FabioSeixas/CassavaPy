*Documentation*


Irrigation

For irrigation is necessary to define:

    1) The DAP (day after planting) for each irrigation event. The user must define a list of DAP's to pass for 'set_irrigation' method.

    2) The water depth for each irrigation event. Again a list must be defined to be passed for 'laminas' argument of 'set_irrigation' method.

    3) A dictionary with keys and values to combine irrigation schedules with treatments. The absence of some treatment inside the dictionary is interpreted as a rainfed treatment.

Two modes for irrigation are possible:

    1) 'irf': irrigation fixed. Means one irrigation schedule, with fixed intervals ('irrig_by'). The water depth of each irrigation event can be fixed or can be manually defined (must have the same length as 'n_irrig')

    2) 'irnf': irrigation not fixed. Means different irrigation schedule, with intervals defined by the user.

    The user will define the 'mode' for irrigation in 'design' argument on the creation of the File object. Different routines will be called according to what was defined in 'design' argument. Be sure to fit the input requirements for each 'mode'.

    *Fixed Irrigation*
        1) n_irrig (int): number of irrigation events
        2) from_irrig (int): DAP of the first irrigation event
        3) by_irrig (int): fixed interval between two irrigation events
        4) laminas (int or list of int): water depth of each irrigation event. If it is a 'int', the same amount of water will be applied for all irrigation events.

    *Not Fixed Irrigation*
        1) reg (list of lists of int): A big list containing all irrigation schedules. Inside each small list, the user must define the DAP's for each irrigation event. The intervals between two irrigation events can be flexible.
        2) laminas (list of lists of int): A big list containing small lists. Inside each small list, each element is the water depth for the corresponding irrigation event in 'reg'. Can be an integer (what means the same amount of water for all irrigation events) or a list of integers with the same length as the corresponding small list in 'reg'.


