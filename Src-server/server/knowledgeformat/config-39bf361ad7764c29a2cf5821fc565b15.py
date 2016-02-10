import os
from terra.server import configuration as CONFIG
from terra.server.configuration import (
    ONE_WORD_INTEGER,
    TWO_WORD_INTEGER_BIG_ENDIAN,
    TWO_WORD_INTEGER_LITTLE_ENDIAN,
    TWO_WORD_FLOAT_BIG_ENDIAN,
    TWO_WORD_FLOAT_LITTLE_ENDIAN,

    Register,
    MeterModel,
    Meter,
    Gateway,
    Group,
    EnergyBalanceGroup,

    Parameters
)



#
# Config constants
#

CONFIG_ROOT_PATH = os.path.split(__file__)[0]

DATA_PATH = os.path.join(
    CONFIG_ROOT_PATH, "..", "..", "..", "Cilantro-Terra-BIAL"
)

DB_PATH = os.path.join(DATA_PATH, "server.db")
DB_MAX_SIZE = 130 * 1024 * 1024 * 1024

DATA_SERVER_PORT = 8080
UI_SERVER_PORT = 8081


#
# Meter models
#

### Conzerv EM 6400

def em6400() :
    registers = [
        Register (
            parameter = Parameters.FREQ,
            address = 3914,
            format = TWO_WORD_FLOAT_LITTLE_ENDIAN,
            factor = 1.0
            ),
        Register (
            parameter = Parameters.VLN,
            address = 3910,
            format = TWO_WORD_FLOAT_LITTLE_ENDIAN,
            factor = 1.0
            ),
        Register (
            parameter = Parameters.VLL,
            address = 3908,
            format = TWO_WORD_FLOAT_LITTLE_ENDIAN,
            factor = 0.001
            ),
        Register (
            parameter = Parameters.ILL,
            address = 3912,
            format = TWO_WORD_FLOAT_LITTLE_ENDIAN,
            factor = 1.0
            ),
        Register (
            parameter = Parameters.KW,
            address = 3902,
            format = TWO_WORD_FLOAT_LITTLE_ENDIAN,
            factor = 0.001
            ),
        Register (
            parameter = Parameters.KVAR,
            address = 3904,
            format = TWO_WORD_FLOAT_LITTLE_ENDIAN,
            factor = 0.001
            ),
        Register (
            parameter = Parameters.KVA,
            address = 3900,
            format = TWO_WORD_FLOAT_LITTLE_ENDIAN,
            factor = 0.001
            ),
        Register (
            parameter = Parameters.PF,
            address = 3906,
            format = TWO_WORD_FLOAT_LITTLE_ENDIAN,
            factor = 1.0
            ),
        Register (
            parameter = Parameters.KWH,
            address = 3960,
            format = TWO_WORD_FLOAT_LITTLE_ENDIAN,
            factor = 0.001
            ),
        Register (
            parameter = Parameters.RT,
            address = 3994,
            format = TWO_WORD_INTEGER_LITTLE_ENDIAN,
            factor = 1.0/3600
            ),
    ]
    return MeterModel(
        "Conzerv EM 6400",
        registers = registers,
        tags = ["em6400-model"]
    )

### Conzerv EM 6430

def em6430() :
    registers = [
        Register (
            parameter = Parameters.FREQ,
            address = 3914,
            format = TWO_WORD_FLOAT_LITTLE_ENDIAN,
            factor = 1.0
            ),
        Register (
            parameter = Parameters.VLN,
            address = 3910,
            format = TWO_WORD_FLOAT_LITTLE_ENDIAN,
            factor = 1.0
            ),
        Register (
            parameter = Parameters.VLL,
            address = 3908,
            format = TWO_WORD_FLOAT_LITTLE_ENDIAN,
            factor = 0.001
            ),
        Register (
            parameter = Parameters.ILL,
            address = 3912,
            format = TWO_WORD_FLOAT_LITTLE_ENDIAN,
            factor = 1.0
            ),
        Register (
            parameter = Parameters.KW,
            address = 3902,
            format = TWO_WORD_FLOAT_LITTLE_ENDIAN,
            factor = 0.001
            ),
        Register (
            parameter = Parameters.KVA,
            address = 3900,
            format = TWO_WORD_FLOAT_LITTLE_ENDIAN,
            factor = 0.001
            ),
        Register (
            parameter = Parameters.PF,
            address = 3906,
            format = TWO_WORD_FLOAT_LITTLE_ENDIAN,
            factor = 1.0
            ),
        Register (
            parameter = Parameters.KWH,
            address = 3960,
            format = TWO_WORD_FLOAT_LITTLE_ENDIAN,
            factor = 0.001
            ),
    ]    
    return MeterModel(
        "Conzerv EM 6430",
        registers = registers,
        tags = ["em6430-model"]
    )

### Conzerv EM 6433

def em6433() :
    registers = [
        Register (
            parameter = Parameters.ILL,
            address = 3912,
            format = TWO_WORD_FLOAT_LITTLE_ENDIAN,
            factor = 1.0
            ),
        Register (
            parameter = Parameters.KW,
            address = 3902,
            format = TWO_WORD_FLOAT_LITTLE_ENDIAN,
            factor = 0.001
            ),
        Register (
            parameter = Parameters.KVA,
            address = 3900,
            format = TWO_WORD_FLOAT_LITTLE_ENDIAN,
            factor = 0.001
            ),
        Register (
            parameter = Parameters.PF,
            address = 3906,
            format = TWO_WORD_FLOAT_LITTLE_ENDIAN,
            factor = 1.0
            ),
        Register (
            parameter = Parameters.KWH,
            address = 3960,
            format = TWO_WORD_FLOAT_LITTLE_ENDIAN,
            factor = 0.001
            ),
        Register (
            parameter = Parameters.RT,
            address = 3994,
            format = TWO_WORD_INTEGER_LITTLE_ENDIAN,
            factor = 1.0/3600
            ),
    ]
    return MeterModel(
        "Conzerv EM 6433",
        registers = registers,
        tags = ["em6433-model"]
    )

### Conzerv EM 6434

def em6434() :
    registers = [
        Register (
            parameter = Parameters.KW,
            address = 3902,
            format = TWO_WORD_FLOAT_LITTLE_ENDIAN,
            factor = 0.001
            ),
        Register (
            parameter = Parameters.KVAR,
            address = 3904,
            format = TWO_WORD_FLOAT_LITTLE_ENDIAN,
            factor = 0.001
            ),
        Register (
            parameter = Parameters.KVA,
            address = 3900,
            format = TWO_WORD_FLOAT_LITTLE_ENDIAN,
            factor = 0.001
            ),
        Register (
            parameter = Parameters.PF,
            address = 3906,
            format = TWO_WORD_FLOAT_LITTLE_ENDIAN,
            factor = 1.0
            ),
        Register (
            parameter = Parameters.KWH,
            address = 3960,
            format = TWO_WORD_FLOAT_LITTLE_ENDIAN,
            factor = 0.001
            ),
        Register (
            parameter = Parameters.RT,
            address = 3994,
            format = TWO_WORD_INTEGER_LITTLE_ENDIAN,
            factor = 1.0/3600
            ),
    ]
    return MeterModel(
        "Conzerv EM 6434",
        registers = registers,
        tags = ["em6434-model"]
    )

### Conzerv EM 6436

def em6436() :
    registers = [
        Register (
            parameter = Parameters.FREQ,
            address = 3914,
            format = TWO_WORD_FLOAT_LITTLE_ENDIAN,
            factor = 1.0
            ),
        Register (
            parameter = Parameters.VLN,
            address = 3910,
            format = TWO_WORD_FLOAT_LITTLE_ENDIAN,
            factor = 1.0
            ),
        Register (
            parameter = Parameters.VLL,
            address = 3908,
            format = TWO_WORD_FLOAT_LITTLE_ENDIAN,
            factor = 0.001
            ),
        Register (
            parameter = Parameters.ILL,
            address = 3912,
            format = TWO_WORD_FLOAT_LITTLE_ENDIAN,
            factor = 1.0
            ),
        Register (
            parameter = Parameters.KW,
            address = 3902,
            format = TWO_WORD_FLOAT_LITTLE_ENDIAN,
            factor = 0.001
            ),
        Register (
            parameter = Parameters.KVA,
            address = 3900,
            format = TWO_WORD_FLOAT_LITTLE_ENDIAN,
            factor = 0.001
            ),
        Register (
            parameter = Parameters.PF,
            address = 3906,
            format = TWO_WORD_FLOAT_LITTLE_ENDIAN,
            factor = 1.0
            ),
        Register (
            parameter = Parameters.KWH,
            address = 3960,
            format = TWO_WORD_FLOAT_LITTLE_ENDIAN,
            factor = 0.001
            ),
        Register (
            parameter = Parameters.RT,
            address = 3994,
            format = TWO_WORD_INTEGER_LITTLE_ENDIAN,
            factor = 1.0/3600
            ),
    ]
    return MeterModel(
    "Conzerv EM 6436",
    registers = registers,
    tags = ["em6436-model"]
    )

### Conzerv EM 6438

def em6438() :
    registers = [
        Register (
            parameter = Parameters.KW,
            address = 3902,
            format = TWO_WORD_FLOAT_LITTLE_ENDIAN,
            factor = 0.001
            ),
        Register (
            parameter = Parameters.KWH,
            address = 3960,
            format = TWO_WORD_FLOAT_LITTLE_ENDIAN,
            factor = 0.001
            ),
        Register (
            parameter = Parameters.RT,
            address = 3994,
            format = TWO_WORD_INTEGER_LITTLE_ENDIAN,
            factor = 1.0/3600
            ),
    ]
    return MeterModel(
    "Conzerv EM 6438",
    registers = registers,
    tags = ["em6438-model"]
    )

### Conzerv EM 1200

def em1200() :
    registers = [
        Register (
            parameter = Parameters.KW,
            address = 3050,
            format = TWO_WORD_FLOAT_BIG_ENDIAN,
            factor = 0.001
            ),
        Register (
            parameter = Parameters.PF,
            address = 3054,
            format = TWO_WORD_FLOAT_BIG_ENDIAN,
            factor = 1.0
            ),
        Register (
            parameter = Parameters.KWH,
            address = 3202,
            format = TWO_WORD_FLOAT_BIG_ENDIAN,
            factor = 0.001
            ),
        Register (
            parameter = Parameters.RT,
            address = 3264,
            format = TWO_WORD_INTEGER_BIG_ENDIAN,
            factor = 1.0/3600
            ),
    ]
    return MeterModel(
    "Conzerv EM 1200",
    registers = registers,
    tags = ["em1200-model"]
    )


#
# Gateways
#

class Gateways(object) :
#
# MPSS, PHN, NEC
#
    #
    # A
    #
    BIAL_MPSS_01 = Gateway("BIAL_MPSS_01", [
        Meter("MPSS_16 MVA Transformer 3 Outgoing", meter_id=1, model=em6436()),
        Meter("MPSS_GSE_02", meter_id=2,model=em6436()),
        Meter("MPSS_Express Cargo", meter_id=3,model=em6436()),
        Meter("MPSS_Flight Catering - 1", meter_id=4,model=em6436()),
        Meter("MPSS_Hotel Loop - 1", meter_id=5,model=em6438()),
        Meter("MPSS_Flight Catering 2 - 3", meter_id=6,model=em6436()),
        Meter("MPSS_Airline Office - 2 - 3", meter_id=7,model=em6436()),
    ]),
    #
    # B
    #
    BIAL_MPSS_02 = Gateway("BIAL_MPSS_02", [
        Meter("MPSS_West Apron CSS - 1", meter_id=1, model=em6436()),
        Meter("MPSS_16 MVA Transformer - 1 Outgoing", meter_id=2, model=em6436()),
        Meter("MPSS_PHN Outgoing - 1", meter_id=3, model=em6436()),
        Meter("MPSS_Traffic Station - 1", meter_id=4, model=em6436()),
        Meter("MPSS_Auxilliary Transformer - 1", meter_id=5, model=em6436()),
        Meter("MPSS_Auxilliary Transformer - 2", meter_id=6, model=em6433()),
        Meter("MPSS_Traffic Station - 2", meter_id=7, model=em6436()),
        Meter("MPSS_PHN Outgoing - 2", meter_id=8, model=em6436()),
        Meter("MPSS_16 MVA Transformer - 2 Outgoing", meter_id=9, model=em6436()),
        Meter("MPSS_West Apron CSS - 2", meter_id=10, model=em6438()),
        Meter("MPSS_MRO", meter_id=11, model=em6436()),
        Meter("MPSS_Hotel Loop - 1", meter_id=12, model=em6436()),
        Meter("MPSS_16 MVA Transformer - 4 Outgoing", meter_id=13, model=em6436()),
    ]),

    #
    # D
    #

    BIAL_PHN_01 = Gateway("BIAL_PHN_01", [
        Meter("PHN_NEC Outgoing - 1", meter_id=1, model=em6436()),
        Meter("PHN_PHN Incomer - 1", meter_id=2, model=em6436()),
        Meter("PHN_Runway - 09", meter_id=3, model=em6436()),
        Meter("PHN_GSE - 1", meter_id=4, model=em6436()),
        Meter("PHN_EB panel 1500 KVA DG Incomer - 1 ", meter_id=5, model=em6438()),
        Meter("PHN_Auxilliary Transformer - 1", meter_id=6, model=em6436()),
        Meter("PHN_AC plant 2 MVA - 1", meter_id=7, model=em6436()),
        Meter("PHN_AC plant 3-15 MVA - 1", meter_id=8, model=em6436()),
        Meter("PHN_PTB SG - 3", meter_id=9, model=em6436()),
        Meter("PHN_PTB SG - 1", meter_id=10, model=em6436()),
        Meter("PHN_AC plant 3-15 MVA - 2", meter_id=11, model=em6436()),
        Meter("PHN_AC plant 2 MVA - 2", meter_id=12, model=em6436()),
        Meter("PHN_Auxilliary Transformer - 2", meter_id=13, model=em6436()),
        Meter("PHN_EB panel 1500 KVA DG Incomer - 2", meter_id=14, model=em6438()),
        Meter("PHN_Pump House", meter_id=15, model=em6436()),
        Meter("PHN_Run Way - 27", meter_id=16, model=em6436()),
        Meter("PHN_PHN Incomer - 2", meter_id=17, model=em6436()),
        Meter("PHN_NEC Outgoing - 2", meter_id=18, model=em6436()),
    ]),

    #
    # E
    #

    BIAL_NEC_01 = Gateway("BIAL_NEC_01", [
        Meter("NEC_DG Incomer - 1", meter_id=1, model=em6436()),
        Meter("NEC_East Expansion feeder SG - 5", meter_id=2, model=em6436()),
        Meter("NEC_East Pier feeder SG - 6", meter_id=3, model=em6436()),
        Meter("NEC_New Chiller Plant-1 NCP - 1", meter_id=4, model=em6436()),
        Meter("NEC_New Chiller Plant-2 NCP - 2", meter_id=5, model=em6436()),
        Meter("NEC_Passenger Boarding Bridge PBB", meter_id=6, model=em6436()),
        Meter("NEC_West Expansion feeder SG4", meter_id=7, model=em6436()),
        Meter("NEC_DG Incomer - 2", meter_id=8, model=em6433()),
        Meter("NEC_NEC LT Incomer - 1", meter_id=9, model=em6436()),
        Meter("NEC_NEC LT Incomer - 2", meter_id=10, model=em6436()),
    ]),


    #
    # ALL
    #

    ALL = [
          BIAL_MPSS_01,
          BIAL_MPSS_02,
          BIAL_PHN_01,
          BIAL_NEC_01,
        ]


#
# Hierarchy configuration
#

def meters_with_tag(gateway, tag) :
    result = []
    for meter in gateway.meters() :
        if tag in meter.model().tags() :
            result.append(meter)
    assert len(result) > 0
    return result

def meters_with_names(gateway, names) :
    meter_map = {}
    for meter in gateway.meters() :
        assert meter.name() not in meter_map
        meter_map[meter.name()] = meter
    return [meter_map[name] for name in names]

def meter_by_name(gateway, name) :
    result = meters_with_names(gateway, [name])
    assert len(result) == 1
    return result[0]


class Hierarchy(object) :

    #
    # Water Mill
    #

    BIAL = Group(
        "BIAL",
        children = [
            "MPSS",
            "PHN",
            "NEC"
        ]
    )

    MPSS = Group(
        "MPSS", 
        children = [
            "16 MVA Transformer 1",
            "16 MVA Transformer 2",
            "16 MVA Transformer 3",
            "16 MVA Transformer 4",
    ])

    #
    # 16 MVA Tr - 3
    #

    MVA_16_Transformer_3 = Group(
        "16 MVA Transformer 3", 
        children = [
            "MPSS_GSE_02",
            "MPSS_Express Cargo",
            "MPSS_Flight Catering - 1",
            "MPSS_Hotel Loop - 1",
            "MPSS_Flight Catering 2 - 3",
            "MPSS_Airline Office - 2 - 3"
        ])

    #
    # 16 MVA Tr - 1
    #
    MVA_16_Transformer_1 = Group(
        "16 MVA Transformer 1", 
        children = [
            "MPSS_West Apron CSS - 1",
            "MPSS_PHN Outgoing - 1",
            "MPSS_Traffic Station - 1",
            "MPSS_Auxilliary Transformer - 1",
            "MPSS_Auxilliary Transformer - 2",
            "MPSS_Traffic Station - 2",
            "MPSS_PHN Outgoing - 2",
            "MPSS_West Apron CSS - 2",
        ])

    #
    # 16 MVA Tr - 4
    #

    MVA_16_Transformer_4 = Group(
        "16 MVA Transformer 4", 
        children = [
            "MPSS_MRO",
            "MPSS_Hotel Loop - 1",
        ])

    #
    # PHN
    #
    PHN = Group(
        "PHN", 
        children = [
            "PHN Incomer - 1", 
            "PHN_PHN Incomer - 2",
            "PHN_EB panel 1500 KVA DG Incomer - 1",
            "PHN_EB panel 1500 KVA DG Incomer - 2"
        ])

    #
    # MPSS PHN Outgoing - 1
    #

    MPSS_PHN_Outgoing = Group(
        "MPSS_PHN Outgoing - 1", 
        children = [
            "PHN_PHN Incomer - 1"
        ])

    #
    # PHN Incomer - 1: D2, D5, D14, D17
    #

    PHN_Incomer_1 = Group(
        "PHN Incomer - 1", 
        children = [
            "PHN_NEC Outgoing - 1",
            "PHN_Runway - 09",
            "PHN_GSE - 1",
            "PHN_Auxilliary Transformer - 1",
            "PHN_AC plant 2 MVA - 1",
            "PHN_AC plant 3-15 MVA - 1",
            "PHN_PTB SG - 3",
            "PHN_PTB SG - 1",
            "PHN_NEC Outgoing - 2",
            "PHN_AC plant 3-15 MVA - 2",
            "PHN_AC plant 2 MVA - 2",
            "PHN_Auxilliary Transformer - 2",
            "PHN_Pump House",
            "PHN_Run Way - 27"
        ])

    #
    # NEC Outgoing - 1: D1, E1, E8, E9
    #

    NEC = Group(
        "NEC", 
        children = [
            "NEC_DG Incomer - 1",
            "NEC_DG Incomer - 2",
            "PHN_NEC Outgoing - 2",
            "NEC Outgoing - 1"
    ])

    NEC_Outgoing_1 = Group(
        "NEC Outgoing - 1", 
        children = [
            "NEC_East Expansion feeder SG - 5",
            "NEC_East Pier feeder SG - 6",
            "NEC_New Chiller Plant-1 NCP - 1",
            "NEC_New Chiller Plant-2 NCP - 2",
            "NEC_Passenger Boarding Bridge PBB",
            "NEC_West Expansion feeder SG4",
    ])

    #
    # ROOT
    #

    ROOT = BIAL


#
# Energy Balance Groups
#

ENERGY_BALANCE_GROUPS = [
    #
    # Plant
    #

    #
    # 16 MVA Tr - 3
    #
    EnergyBalanceGroup(
        ht_meter = "MPSS_16 MVA Transformer 3 Outgoing",
        lt_meters = [
            "MPSS_GSE_02",
            "MPSS_Express Cargo",
            "MPSS_Flight Catering - 1",
            "MPSS_Hotel Loop - 1",
            "MPSS_Flight Catering 2 - 3",
            "MPSS_Airline Office - 2 - 3"
        ] 
    ),

    #
    # 16 MVA Tr - 1
    #
    EnergyBalanceGroup(
        ht_meter = "MPSS_16 MVA Transformer - 1 Outgoing", 
        lt_meters = [
            "MPSS_West Apron CSS - 1",
            "MPSS_PHN Outgoing - 1",
            "MPSS_Traffic Station - 1",
            "MPSS_Auxilliary Transformer - 1",
            "MPSS_Auxilliary Transformer - 2",
            "MPSS_Traffic Station - 2",
            "MPSS_PHN Outgoing - 2",
            "MPSS_West Apron CSS - 2",
        ]
    ),

    #
    # 16 MVA Tr - 4
    #
    EnergyBalanceGroup(
        ht_meter =  "MPSS_16 MVA Transformer - 4 Outgoing", 
        lt_meters = [
            "MPSS_MRO",
            "MPSS_Hotel Loop - 1",
        ]
    ),

    #
    # MPSS PHN Outgoing - 1
    #
    EnergyBalanceGroup(
        ht_meter =  "MPSS_PHN Outgoing - 1", 
        lt_meters = [
            "PHN_PHN Incomer - 1"
        ]
    ),

    #
    # PHN Incomer - 1: D2, D5, D14, D17
    #
    EnergyBalanceGroup(
        ht_meter =  "PHN_PHN Incomer - 1", 
        lt_meters = [
            "PHN_NEC Outgoing - 1",
            "PHN_Runway - 09",
            "PHN_GSE - 1",
            "PHN_Auxilliary Transformer - 1",
            "PHN_AC plant 2 MVA - 1",
            "PHN_AC plant 3-15 MVA - 1",
            "PHN_PTB SG - 3",
            "PHN_PTB SG - 1",
            "PHN_NEC Outgoing - 2",
            "PHN_AC plant 3-15 MVA - 2",
            "PHN_AC plant 2 MVA - 2",
            "PHN_Auxilliary Transformer - 2",
            "PHN_Pump House",
            "PHN_Run Way - 27"
        ]
    ),

    #
    # NEC Outgoing - 1: D1, E1, E8, E9
    #
    EnergyBalanceGroup(
        ht_meter =  "PHN_NEC Outgoing - 1", 
        lt_meters = [
            "NEC_East Expansion feeder SG - 5",
            "NEC_East Pier feeder SG - 6",
            "NEC_New Chiller Plant-1 NCP - 1",
            "NEC_New Chiller Plant-2 NCP - 2",
            "NEC_Passenger Boarding Bridge PBB",
            "NEC_West Expansion feeder SG4",
        ]
    ),


    #
    # PHN Auxilliary Transformer - 1
    #
    EnergyBalanceGroup(
        ht_meter =  "PHN_Auxilliary Transformer - 1", 
        lt_meters = [
           "NEC_NEC LT Incomer - 1"
        ]
    ),

    #
    # PHN Auxilliary Transformer - 2
    #
    EnergyBalanceGroup(
        ht_meter =  "PHN_Auxilliary Transformer - 2", 
        lt_meters = [
            "NEC_NEC LT Incomer - 2"
        ]
    ),

    #
    # MPSS PHN Outgoing - 2
    #
    EnergyBalanceGroup(
        ht_meter =  "MPSS_PHN Outgoing - 2", 
        lt_meters = [
            "PHN_PHN Incomer - 2"
        ]
    ),
]


#
# data_for_json
#

def data_for_json() :
    return CONFIG.data_for_json(
        Gateways, Hierarchy, ENERGY_BALANCE_GROUPS
    )


#
# generate_script
#

def generate_script() :
    return CONFIG.generate_script(
        Gateways, Hierarchy
    )


if __name__ == "__main__" :
    print generate_script()
