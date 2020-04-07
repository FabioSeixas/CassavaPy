
def space(x):
    if int(x) < 10:
        return(f" {x}")
    return(x)


def controls_space(x):
    if int(x) < 0:
        return(f"  {x}")
    return(x)


def write_head(file, filename, exp_name, mode="CS"):
    exp_details = filename + mode + " " + exp_name

    file.write(f'*EXP.DETAILS: {exp_details}\n\n@PEOPLE\nFabio\n@ADDRESS\n-99\n@SITE\n-99\n*GENERAL\n@ PAREA  PRNO  PLEN  PLDR  PLSP  PLAY HAREA  HRNO  HLEN  HARM.........\n    -99   -99   -99   -99   -99   -99   -99   -99   -99   -99\n\n*TREATMENTS                        -------------FACTOR LEVELS------------\n@N R O C TNAME.................... CU FL SA IC MP MI MF MR MC MT ME MH SM\n')


def write_treatments(file, tratmatrix):

    if len(tratmatrix) <= 9:
        for i, trat in enumerate(tratmatrix):
            file.write(f" {i + 1} 1 1 0 {trat[0]}                      1  1  0  1  {trat[1]}  {trat[3]}  0  0  0  0  0  {trat[2]}  1\n")
    else:
        for i, trat in enumerate(tratmatrix[:9]):
            file.write(f" {i + 1} 1 1 0 {trat[0]}                      1  1  0  1  {trat[1]}  {trat[3]}  0  0  0  0  0  {trat[2]}  1\n")

        for i, trat in enumerate(tratmatrix[9:]):
            file.write(f"{i + 10} 1 1 0 {trat[0]}                      1  1  0  1 {space(trat[1])} {space(trat[3])}  0  0  0  0  0 {space(trat[2])}  1\n")


def write_cultivars(file, genotype):
    ''' Por enquanto só está implementado para 1 genótipo por arquivo X.
    '''
    file.write("\n*CULTIVARS\n@C CR INGENO CNAME\n")
    file.write(f" 1 CS {genotype[0]} {genotype[1]}\n")


def write_field(file, field):

    file.write(f"\n*FIELDS\n@L ID_FIELD WSTA....  FLSA  FLOB  FLDT  FLDD  FLDS  FLST SLTX  SLDP  ID_SOIL    FLNAME\n 1 00000001 {field[0]}       -99   -99   -99   -99   -99   -99 -99    -99  {field[1]} -99\n@L ...........XCRD ...........YCRD .....ELEV .............AREA .SLEN .FLWR .SLAS FLHST FHDUR\n 1             -99             -99       -99               -99   -99   -99   -99   -99   -99\n")


def write_initial_conditions(file, sim_start):

    # Por enquanto está configurado apenas para 'Medium Silty Clay' - IB00000002
    file.write(f'\n*INITIAL CONDITIONS\n@C   PCR ICDAT  ICRT  ICND  ICRN  ICRE  ICWD ICRES ICREN ICREP ICRIP ICRID ICNAME\n 1    CS {sim_start}   -99   -99     1     1   -99   -99   -99   -99   -99   -99 -99\n@C  ICBL  SH2O  SNH4  SNO3\n')
    file.write(f' 1     5  .244    .1   1.1\n 1    15  .244    .1   1.1\n 1    30  .244    .1   1.1\n 1    45  .265    .1   1.1\n 1    60  .265    .1   1.1\n 1    90  .322    .1   1.1\n 1   120   .22    .1   1.1\n 1   150  .268    .1   1.1\n')


def write_planting(file, planting):
    file.write("\n*PLANTING DETAILS\n@P PDATE EDATE  PPOP  PPOE  PLME  PLDS  PLRS  PLRD  PLDP  PLWT  PAGE  PENV  PLPH  SPRL                        PLNAME\n")

    if len(planting) <= 9:
        for i, pdate in enumerate(planting):
            file.write(f" {i + 1} {pdate}   -99     1   -99     H     R    80     0     5   -99   -99   -99   -99   -99                        {pdate}\n")
    else:
        for i, pdate in enumerate(planting[:9]):
            file.write(f" {i + 1} {pdate}   -99     1   -99     H     R    80     0     5   -99   -99   -99   -99   -99                        {pdate}\n")
        for i, pdate in enumerate(planting[9:]):
            file.write(f"{i + 10} {pdate}   -99     1   -99     H     R    80     0     5   -99   -99   -99   -99   -99                        {pdate}\n")


def write_irrigation(file, irrigation):
    file.write("\n*IRRIGATION AND WATER MANAGEMENT\n")

    # if len(irrigation) <= 9:
    #     for i, irrig_sch in enumerate(irrigation):
    #         file.write(f"@I  EFIR  IDEP  ITHR  IEPT  IOFF  IAME  IAMT IRNAME\n {i + 1}     1    30    50   100 GS000 IR001    10 -99\n@I IDATE  IROP IRVAL\n")
    #         for q, irr_event in enumerate(irrig_sch):
    #             file.write(f" {i + 1} {irr_event[0]} IR005    {space(irr_event[1])} \n")
    # else:
    #     for i, irrig_sch in enumerate(irrigation[:9]):
    #         file.write(f"@I  EFIR  IDEP  ITHR  IEPT  IOFF  IAME  IAMT IRNAME\n {i + 1}     1    30    50   100 GS000 IR001    10 -99\n@I IDATE  IROP IRVAL\n")
    #         for q, irr_event in enumerate(irrig_sch):
    #             file.write(f" {i + 1} {irr_event[0]} IR005    {space(irr_event[1])} \n")
    #     for i, irrig_sch in enumerate(irrigation[9:]):
    #         file.write(f"@I  EFIR  IDEP  ITHR  IEPT  IOFF  IAME  IAMT IRNAME\n{i + 10}     1    30    50   100 GS000 IR001    10 -99\n@I IDATE  IROP IRVAL\n")
    #         for q, irr_event in enumerate(irrig_sch):
    #             file.write(f"{i + 10} {irr_event[0]} IR005    {space(irr_event[1])} \n")
    for i, irrig_sch in irrigation.items():
        file.write(f"@I  EFIR  IDEP  ITHR  IEPT  IOFF  IAME  IAMT IRNAME\n{space(i)}     1    30    50   100 GS000 IR001    10 -99\n@I IDATE  IROP IRVAL\n")

        for date_event, water in irrig_sch:
            file.write(f"{space(i)} {date_event} IR005    {space(water)} \n")


def write_harvest(file, harvest):

    file.write("\n*HARVEST DETAILS\n@H HDATE  HSTG  HCOM HSIZE   HPC  HBPC HNAME\n")

    if len(harvest) <= 9:
        for i, hdate in enumerate(harvest):
            file.write(f" {i + 1} {hdate} GS000   -99   -99   -99   -99 {i + 1}\n")
    else:
        for i, hdate in enumerate(harvest[:9]):
            file.write(f" {i + 1} {hdate} GS000   -99   -99   -99   -99 {i + 1}\n")
        for i, hdate in enumerate(harvest[9:]):
            file.write(f"{i + 10} {hdate} GS000   -99   -99   -99   -99 {i + 10}\n")


def write_controls(file, sim_start, reps=1, mode="exp"):

    dic = {"exp": ["S", sim_start],
           "seas": ["P", "-99"]}

    if any(item in [mode] for item in dic):
        file.write(f"\n*SIMULATION CONTROLS\n@N GENERAL     NYERS NREPS START SDATE RSEED SNAME.................... SMODEL\n 1 GE             {space(reps)}     1     {dic[mode][0]} {controls_space(dic[mode][1])}  2150 DEFAULT SIMULATION CONTR  CSYCA\n@N OPTIONS     WATER NITRO SYMBI PHOSP POTAS DISES  CHEM  TILL   CO2\n 1 OP              Y     N     N     N     N     N     N     N     M\n@N METHODS     WTHER INCON LIGHT EVAPO INFIL PHOTO HYDRO NSWIT MESOM MESEV MESOL\n 1 ME              M     M     E     R     S     L     R     1     G     S     2\n@N MANAGEMENT  PLANT IRRIG FERTI RESID HARVS\n 1 MA              R     R     N     N     R\n@N OUTPUTS     FNAME OVVEW SUMRY FROPT GROUT CAOUT WAOUT NIOUT MIOUT DIOUT VBOSE CHOUT OPOUT FMOPT\n 1 OU              N     Y     Y     1     Y     Y     Y     Y     Y     N     Y     N     Y     A\n\n@  AUTOMATIC MANAGEMENT\n@N PLANTING    PFRST PLAST PH2OL PH2OU PH2OD PSTMX PSTMN\n 1 PL            001   001    40   100    30    40    10\n@N IRRIGATION  IMDEP ITHRL ITHRU IROFF IMETH IRAMT IREFF\n 1 IR             30    80   100 GS000 IR001    10     1\n@N NITROGEN    NMDEP NMTHR NAMNT NCODE NAOFF\n 1 NI             30    50    25 FE001 GS000\n@N RESIDUES    RIPCN RTIME RIDEP\n 1 RE            100     1    20\n@N HARVEST     HFRST HLAST HPCNP HPCNR\n 1 HA              0   001   100     0")
    else:
        raise ValueError(f" Valor '{mode}' não reconhecido para o argumento 'mode'. ")
