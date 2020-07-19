
def space(x):
    if int(x) < 10:
        return(f" {x}")

    return(x)


def controls_space(x):
    if int(x) < 0:
        return(f"  {x}")
    return(x)


def handle_empty_space(x):
    if int(x) > 99:
        return ""
    return " "


def spaces(x):
    if int(x) > 99:
        return f"{x}"

    elif int(x) > 9:
        return f" {x}"
    return f"  {x}"


def str_spaces(x):
    x = str(x)[1:]

    if len(x) == 4:
        return x
    if len(x) == 3:
        return f' {x}'
    raise ValueError("Checar espaçamento de 'water' nas condições iniciais")


def write_head(file, filename, exp_name, mode="CS"):

    exp_details = filename + mode + " " + exp_name

    file.write(f'*EXP.DETAILS: {exp_details}\n\n@PEOPLE\nFabio\n@ADDRESS\n-99\n@SITE\n-99\n*GENERAL\n@ PAREA  PRNO  PLEN  PLDR  PLSP  PLAY HAREA  HRNO  HLEN  HARM.........\n    -99   -99   -99   -99   -99   -99   -99   -99   -99   -99\n\n*TREATMENTS                        -------------FACTOR LEVELS------------\n@N R O C TNAME.................... CU FL SA IC MP MI MF MR MC MT ME MH SM\n')


def write_treatments(file, tratmatrix):
    for i, trat in enumerate(tratmatrix):
        file.write(f"{space(i + 1)} 1 1 0 {trat[0]}                    {handle_empty_space(i + 1)}{space(trat[1])}  1  0  1 {space(trat[2])} {space(trat[4])}  0  0  0  0  0 {space(trat[3])}  1\n")


def write_cultivars(file, genotypes):

    file.write("\n*CULTIVARS\n@C CR INGENO CNAME\n")
    for i, gen in enumerate(genotypes, start=1):
        file.write(f"{space(i)} CS {gen[0]} {gen[1]}\n")


def write_field(file, field):

    file.write(f"\n*FIELDS\n@L ID_FIELD WSTA....  FLSA  FLOB  FLDT  FLDD  FLDS  FLST SLTX  SLDP  ID_SOIL    FLNAME\n 1 00000001 {field[0]}       -99   -99   -99   -99   -99   -99 -99    -99  {field[1]} -99\n@L ...........XCRD ...........YCRD .....ELEV .............AREA .SLEN .FLWR .SLAS FLHST FHDUR\n 1             -99             -99       -99               -99   -99   -99   -99   -99   -99\n")


def write_initial_conditions(file, sim_start, soil):

    # Por enquanto está configurado apenas para 'Medium Silty Clay' - IB00000002
    file.write(f'\n*INITIAL CONDITIONS\n@C   PCR ICDAT  ICRT  ICND  ICRN  ICRE  ICWD ICRES ICREN ICREP ICRIP ICRID ICNAME\n 1    CS {sim_start}   -99   -99     1     1   -99   -99   -99   -99   -99   -99 -99\n@C  ICBL  SH2O  SNH4  SNO3\n')

    for depth, water in zip(soil["ICBL"], soil["SH2O"]):
        file.write(f' 1   {spaces(depth)}  {str_spaces(water)}    .1   1.1\n')


def write_planting(file, planting):
    file.write("\n*PLANTING DETAILS\n@P PDATE EDATE  PPOP  PPOE  PLME  PLDS  PLRS  PLRD  PLDP  PLWT  PAGE  PENV  PLPH  SPRL                        PLNAME\n")

    if len(planting) <= 9:
        for i, pdate in enumerate(planting):
            file.write(f" {i + 1} {pdate} {int(pdate) + 10}  1.39   -99     H     R    80     0     5   -99   -99   -99     2    30                        {pdate}\n")
    else:
        for i, pdate in enumerate(planting[:9]):
            file.write(f" {i + 1} {pdate}   -99  1.39   -99     H     R    80     0     5   -99   -99   -99   -99    30                        {pdate}\n")
        for i, pdate in enumerate(planting[9:]):
            file.write(f"{i + 10} {pdate}   -99  1.39   -99     H     R    80     0     5   -99   -99   -99   -99    30                        {pdate}\n")


def write_irrigation(file, irrigation):

    def space_irrig(x):
        if len(str(x)) < 2:
            return(f"   {x}")
        elif len(str(x)) == 2:
            return(f"  {x}")
        elif len(str(x)) == 3:
            return(f' {x}')
        elif len(str(x)) == 4:
            return(x)

    file.write("\n*IRRIGATION AND WATER MANAGEMENT\n")

    for i, irrig_sch in irrigation.items():
        file.write(f"@I  EFIR  IDEP  ITHR  IEPT  IOFF  IAME  IAMT IRNAME\n{space(i)}   0.8    30    50   100 GS000 IR004    10 -99\n@I IDATE  IROP IRVAL\n")

        for date_event, water in irrig_sch:
            file.write(f"{space(i)} {date_event} IR005  {space_irrig(water)} \n")


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


def write_controls(file, sim_start, years=1, mode="exp"):

    dic = {"exp": ["P", sim_start],
           "seas": ["P", sim_start]}     # ["P", "-99"] -> to use planting date as the 'sim_start'

    if any(item in [mode] for item in dic):
        file.write(f"\n*SIMULATION CONTROLS\n@N GENERAL     NYERS NREPS START SDATE RSEED SNAME.................... SMODEL\n 1 GE             {space(years)}     1     {dic[mode][0]} {controls_space(dic[mode][1])}  2150 DEFAULT SIMULATION CONTR  CSYCA\n@N OPTIONS     WATER NITRO SYMBI PHOSP POTAS DISES  CHEM  TILL   CO2\n 1 OP              Y     N     N     N     N     N     N     N     M\n@N METHODS     WTHER INCON LIGHT EVAPO INFIL PHOTO HYDRO NSWIT MESOM MESEV MESOL\n 1 ME              M     M     E     R     S     L     R     1     G     S     2\n@N MANAGEMENT  PLANT IRRIG FERTI RESID HARVS\n 1 MA              R     R     N     N     R\n@N OUTPUTS     FNAME OVVEW SUMRY FROPT GROUT CAOUT WAOUT NIOUT MIOUT DIOUT VBOSE CHOUT OPOUT FMOPT\n 1 OU              N     Y     Y     1     Y     Y     Y     Y     Y     N     Y     N     Y     A\n\n@  AUTOMATIC MANAGEMENT\n@N PLANTING    PFRST PLAST PH2OL PH2OU PH2OD PSTMX PSTMN\n 1 PL            001   001    40   100    30    40    10\n@N IRRIGATION  IMDEP ITHRL ITHRU IROFF IMETH IRAMT IREFF\n 1 IR             30    80   100 GS000 IR001    10     1\n@N NITROGEN    NMDEP NMTHR NAMNT NCODE NAOFF\n 1 NI             30    50    25 FE001 GS000\n@N RESIDUES    RIPCN RTIME RIDEP\n 1 RE            100     1    20\n@N HARVEST     HFRST HLAST HPCNP HPCNR\n 1 HA              0   001   100     0")
    else:
        raise ValueError(f" Valor '{mode}' não reconhecido para o argumento 'mode'. ")
