from flask import Flask, jsonify, request
import yfinance as yf
import pandas as pd
import numpy as np
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app, origins="*")

# ================================================================
# DATA: Emiten IDX
# ================================================================
IDX_ALL = [
    "AADI","AALI","ABBA","ABDA","ABMM","ACES","ACRO","ACST","ADCP","ADES",
    "ADHI","ADMF","ADMG","ADMR","ADRO","AEGS","AGAR","AGII","AGRO","AGRS",
    "AHAP","AIMS","AISA","AKKU","AKPI","AKRA","AKSI","ALDO","ALII","ALKA",
    "ALMI","ALTO","AMAG","AMAN","AMAR","AMFG","AMIN","AMMN","AMMS","AMOR",
    "AMRT","ANDI","ANJT","ANTM","APEX","APIC","APII","APLI","APLN","ARCI",
    "AREA","ARGO","ARII","ARKA","ARKO","ARMY","ARNA","ARTA","ARTI","ARTO",
    "ASBI","ASDM","ASGR","ASHA","ASII","ASJT","ASLC","ASLI","ASMI","ASPI",
    "ASPR","ASRI","ASRM","ASSA","ATAP","ATIC","ATLA","AUTO","AVIA","AWAN",
    "AXIO","AYAM","AYLS","BABP","BABY","BACA","BAIK","BAJA","BALI","BANK",
    "BAPA","BAPI","BATA","BATR","BAUT","BAYU","BBCA","BBHI","BBKP","BBLD",
    "BBMD","BBNI","BBRI","BBRM","BBSI","BBSS","BBTN","BBYB","BCAP","BCIC",
    "BCIP","BDKR","BDMN","BEBS","BEEF","BEER","BEKS","BELI","BELL","BESS",
    "BEST","BFIN","BGTG","BHAT","BHIT","BIKA","BIKE","BIMA","BINA","BINO",
    "BIPI","BIPP","BIRD","BISI","BJBR","BJTM","BKDP","BKSL","BKSW","BLES",
    "BLOG","BLTA","BLTZ","BLUE","BMAS","BMBL","BMHS","BMRI","BMSR","BMTR",
    "BNBA","BNBR","BNGA","BNII","BNLI","BOAT","BOBA","BOGA","BOLA","BOLT",
    "BOSS","BPFI","BPII","BPTR","BRAM","BREN","BRIS","BRMS","BRNA","BRPT",
    "BRRC","BSBK","BSDE","BSIM","BSML","BSSR","BSWD","BTEK","BTEL","BTON",
    "BTPN","BTPS","BUAH","BUDI","BUKA","BUKK","BULL","BUMI","BUVA","BVIC",
    "BWPT","BYAN","CAKK","CAMP","CANI","CARE","CARS","CASA","CASH","CASS",
    "CBDK","CBMF","CBPE","CBRE","CBUT","CCSI","CDIA","CEKA","CENT","CFIN",
    "CGAS","CHEK","CHEM","CHIP","CINT","CITA","CITY","CLAY","CLEO","CLPI",
    "CMNP","CMNT","CMPP","CMRY","CNKO","CNMA","CNTX","COAL","COCO","COIN",
    "COWL","CPIN","CPRI","CPRO","CRAB","CRSN","CSAP","CSIS","CSMI","CSRA",
    "CTBN","CTRA","CTTH","CUAN","CYBR","DAAZ","DADA","DART","DATA","DAYA",
    "DCII","DEAL","DEFI","DEPO","DEWA","DEWI","DFAM","DGIK","DGNS","DGWG",
    "DIGI","DILD","DIVA","DKFT","DKHH","DLTA","DMAS","DMMX","DMND","DNAR",
    "DNET","DOID","DOOH","DOSS","DPNS","DPUM","DRMA","DSFI","DSNG","DSSA",
    "DUCK","DUTI","DVLA","DWGL","DYAN","EAST","ECII","EDGE","EKAD","ELIT",
    "ELPI","ELSA","ELTY","EMAS","EMDE","EMTK","ENAK","ENRG","ENVY","ENZO",
    "EPAC","EPMT","ERAA","ERAL","ERTX","ESIP","ESSA","ESTA","ESTI","ETWA",
    "EURO","EXCL","FAPA","FAST","FASW","FILM","FIMP","FIRE","FISH","FITT",
    "FLMC","FMII","FOLK","FOOD","FORE","FORU","FPNI","FUJI","FUTR","FWCT",
    "GAMA","GDST","GDYR","GEMA","GEMS","GGRM","GGRP","GHON","GIAA","GJTL",
    "GLOB","GLVA","GMFI","GMTD","GOLD","GOLF","GOLL","GOOD","GOTO","GPRA",
    "GPSO","GRIA","GRPH","GRPM","GSMF","GTBO","GTRA","GTSI","GULA","GUNA",
    "GWSA","GZCO","HADE","HAIS","HAJJ","HALO","HATM","HBAT","HDFA","HDIT",
    "HEAL","HELI","HERO","HEXA","HGII","HILL","HITS","HKMU","HMSP","HOKI",
    "HOME","HOMI","HOPE","HOTL","HRME","HRTA","HRUM","HUMI","HYGN","IATA",
    "IBFN","IBOS","IBST","ICBP","ICON","IDEA","IDPR","IFII","IFSH","IGAR",
    "IIKP","IKAI","IKAN","IKBI","IKPM","IMAS","IMJS","IMPC","INAF","INAI",
    "INCF","INCI","INCO","INDF","INDO","INDR","INDS","INDX","INDY","INET",
    "INKP","INOV","INPC","INPP","INPS","INRU","INTA","INTD","INTP","IOTF",
    "IPAC","IPCC","IPCM","IPOL","IPPE","IPTV","IRRA","IRSX","ISAP","ISAT",
    "ISEA","ISSP","ITIC","ITMA","ITMG","JARR","JAST","JATI","JAWA","JAYA",
    "JECC","JGLE","JIHD","JKON","JMAS","JPFA","JRPT","JSKY","JSMR","JSPT",
    "JTPE","KAEF","KAQI","KARW","KAYU","KBAG","KBLI","KBLM","KBLV","KBRI",
    "KDSI","KDTN","KEEN","KEJU","KETR","KIAS","KICI","KIJA","KING","KINO",
    "KIOS","KJEN","KKES","KKGI","KLAS","KLBF","KLIN","KMDS","KMTR","KOBX",
    "KOCI","KOIN","KOKA","KONI","KOPI","KOTA","KPIG","KRAS","KREN","KRYA",
    "KSIX","KUAS","LABA","LABS","LAJU","LAND","LAPD","LCGP","LCKM","LEAD",
    "LFLO","LIFE","LINK","LION","LIVE","LMAS","LMAX","LMPI","LMSH","LOPI",
    "LPCK","LPGI","LPIN","LPKR","LPLI","LPPF","LPPS","LRNA","LSIP","LTLS",
    "LUCK","LUCY","MABA","MAGP","MAHA","MAIN","MANG","MAPA","MAPB","MAPI",
    "MARI","MARK","MASB","MAXI","MAYA","MBAP","MBMA","MBSS","MBTO","MCAS",
    "MCOL","MCOR","MDIA","MDIY","MDKA","MDKI","MDLA","MDLN","MDRN","MEDC",
    "MEDS","MEGA","MEJA","MENN","MERI","MERK","META","MFMI","MGLV","MGNA",
    "MGRO","MHKI","MICE","MIDI","MIKA","MINA","MINE","MIRA","MITI","MKAP",
    "MKNT","MKPI","MKTR","MLBI","MLIA","MLPL","MLPT","MMIX","MMLP","MNCN",
    "MOLI","MORA","MPIX","MPMX","MPOW","MPPA","MPRO","MPXL","MRAT","MREI",
    "MSIE","MSIN","MSJA","MSKY","MSTI","MTDL","MTEL","MTFN","MTLA","MTMH",
    "MTPS","MTRA","MTSM","MTWI","MUTU","MYOH","MYOR","MYTX","NAIK","NANO",
    "NASA","NASI","NATO","NAYZ","NCKL","NELY","NEST","NETV","NFCX","NICE",
    "NICK","NICL","NIKL","NINE","NIRO","NISP","NOBU","NPGF","NRCA","NSSS",
    "NTBK","NUSA","NZIA","OASA","OBAT","OBMD","OCAP","OILS","OKAS","OLIV",
    "OMED","OMRE","OPMS","PACK","PADA","PADI","PALM","PAMG","PANI","PANR",
    "PANS","PART","PBID","PBRX","PBSA","PCAR","PDES","PDPP","PEGE","PEHA",
    "PEVE","PGAS","PGEO","PGJO","PGLI","PGUN","PICO","PIPA","PJAA","PJHB",
    "PKPK","PLAN","PLAS","PLIN","PMJS","PMMP","PMUI","PNBN","PNBS","PNGO",
    "PNIN","PNLF","PNSE","POLA","POLI","POLL","POLU","POLY","POOL","PORT",
    "POSA","POWR","PPGL","PPRE","PPRI","PPRO","PRAY","PRDA","PRIM","PSAB",
    "PSAT","PSDN","PSGO","PSKT","PSSI","PTBA","PTDU","PTIS","PTMP","PTMR",
    "PTPP","PTPS","PTPW","PTRO","PTSN","PTSP","PUDP","PURA","PURE","PURI",
    "PWON","PYFA","PZZA","RAAM","RAFI","RAJA","RALS","RANC","RATU","RBMS",
    "RCCC","RDTX","REAL","RELF","RELI","RGAS","RICY","RIGS","RIMO","RISE",
    "RLCO","RMKE","RMKO","ROCK","RODA","RONY","ROTI","RSCH","RSGK","RUIS",
    "RUNS","SAFE","SAGE","SAME","SAMF","SAPX","SATU","SBAT","SBMA","SCCO",
    "SCMA","SCNP","SCPI","SDMU","SDPC","SDRA","SEMA","SFAN","SGER","SGRO",
    "SHID","SHIP","SICO","SIDO","SILO","SIMA","SIMP","SINI","SIPD","SKBM",
    "SKLT","SKRN","SKYB","SLIS","SMAR","SMBR","SMCB","SMDM","SMDR","SMGA",
    "SMGR","SMIL","SMKL","SMKM","SMLE","SMMA","SMMT","SMRA","SMRU","SMSM",
    "SNLK","SOCI","SOFA","SOHO","SOLA","SONA","SOSS","SOTS","SOUL","SPMA",
    "SPRE","SPTO","SQMI","SRAJ","SRIL","SRSN","SRTG","SSIA","SSMS","SSTM",
    "STAA","STAR","STRK","STTP","SUGI","SULI","SUNI","SUPA","SUPR","SURE",
    "SURI","SWAT","SWID","TALF","TAMA","TAMU","TAPG","TARA","TAXI","TAYS",
    "TBIG","TBLA","TBMS","TCID","TCPI","TDPM","TEBE","TECH","TELE","TFAS",
    "TFCO","TGKA","TGRA","TGUK","TIFA","TINS","TIRA","TIRT","TKIM","TLDN",
    "TLKM","TMAS","TMPO","TNCA","TOBA","TOOL","TOPS","TOSK","TOTL","TOTO",
    "TOWR","TOYS","TPIA","TPMA","TRAM","TRGU","TRIL","TRIM","TRIN","TRIO",
    "TRIS","TRJA","TRON","TRST","TRUE","TRUK","TRUS","TSPC","TUGU","TYRE",
    "UANG","UCID","UDNG","UFOE","ULTJ","UNIC","UNIQ","UNIT","UNSP","UNTD",
    "UNTR","UNVR","URBN","UVCR","VAST","VERN","VICI","VICO","VINS","VISI",
    "VIVA","VKTR","VOKS","VRNA","VTNY","WAPO","WEGE","WEHA","WGSH","WICO",
    "WIDI","WIFI","WIIM","WIKA","WINE","WINR","WINS","WIRG","WMPP","WMUU",
    "WOMF","WOOD","WOWS","WSBP","WSKT","WTON","YELO","YOII","YPAS","YULE",
    "YUPI","ZATA","ZBRA","ZINC","ZONE","ZYRX",
]

SECTORS = {
    "Basic_Materials": [
        "ADMG","AGII","AKPI","ALDO","ALKA","ALMI","AMMN","ANTM","APLI","ARCI",
        "ASPR","AVIA","AYLS","BAJA","BATR","BEBS","BLES","BMSR","BRMS","BRNA",
        "BRPT","BTON","CHEM","CITA","CLPI","CMNT","CTBN","DAAZ","DGWG","DKFT",
        "DPNS","EKAD","EMAS","EPAC","ESIP","ESSA","ETWA","FASW","FPNI","FWCT",
        "GDST","GGRP","HKMU","IFII","IFSH","IGAR","INAI","INCF","INCI","INCO",
        "INKP","INRU","INTD","INTP","IPOL","ISSP","KAYU","KBRI","KDSI","KKES",
        "KMTR","KRAS","LMSH","LTLS","MBMA","MDKA","MDKI","MINE","MOLI","NCKL",
        "NICE","NICL","NIKL","NPGF","OBMD","OKAS","OPMS","PACK","PBID","PDPP",
        "PICO","PPRI","PSAB","PTMR","PURE","SAMF","SBMA","SIMA","SMBR","SMCB",
        "SMGA","SMGR","SMKL","SMLE","SOLA","SPMA","SQMI","SRSN","SULI","SWAT",
        "TALF","TBMS","TDPM","TINS","TIRT","TKIM","TPIA","TRST","UNIC","WSBP",
        "WTON","YPAS","ZINC",
    ],
    "Consumer_Cyclicals": [
        "ABBA","ACES","ACRO","AEGS","AKKU","ARGO","ARTA","ASLC","AUTO","BABY",
        "BAIK","BATA","BAUT","BAYU","BELL","BIKE","BIMA","BLTZ","BMBL","BMTR",
        "BOGA","BOLA","BOLT","BRAM","BUVA","CARS","CBMF","CINT","CLAY","CNMA",
        "CNTX","CSAP","CSMI","DEPO","DFAM","DIGI","DOOH","DOSS","DRMA","DUCK",
        "EAST","ECII","ENAK","ERAA","ERAL","ERTX","ESTA","ESTI","FAST","FILM",
        "FITT","FORU","FUTR","GDYR","GEMA","GJTL","GLOB","GOLF","GRPH","GWSA",
        "HAJJ","HOME","HOTL","HRME","HRTA","IDEA","IIKP","IMAS","INDR","INDS",
        "INOV","IPTV","ISAP","JGLE","JIHD","JSPT","KAQI","KDTN","KICI","KLIN",
        "KOTA","KPIG","LFLO","LIVE","LMAX","LMPI","LPIN","LPPF","LUCY","MABA",
        "MAPA","MAPB","MAPI","MARI","MDIA","MDIY","MEJA","MERI","MGLV","MGNA",
        "MICE","MINA","MKNT","MNCN","MPMX","MSIN","MSKY","MYTX","NATO","NETV",
        "NUSA","OLIV","PANR","PART","PBRX","PDES","PGLI","PJAA","PLAN","PMJS",
        "PMUI","PNSE","POLU","POLY","PSKT","PTSP","PZZA","RAAM","RAFI","RALS",
        "RICY","SBAT","SCMA","SCNP","SHID","SLIS","SMSM","SNLK","SOFA","SONA",
        "SOTS","SPRE","SRIL","SSTM","SWID","TELE","TFCO","TMPO","TOOL","TOYS",
        "TRIO","TRIS","TYRE","UFOE","UNIT","UNTD","VERN","VIVA","VKTR","WOOD",
        "YELO","ZATA","ZONE",
    ],
    "Consumer_Non_Cyclicals": [
        "AALI","ADES","AGAR","AISA","ALTO","AMMS","AMRT","ANDI","ANJT","ASHA",
        "AYAM","BEEF","BEER","BISI","BOBA","BRRC","BTEK","BUAH","BUDI","BWPT",
        "CAMP","CBUT","CEKA","CLEO","CMRY","COCO","CPIN","CPRO","CRAB","CSRA",
        "DAYA","DEWI","DLTA","DMND","DPUM","DSFI","DSNG","ENZO","EPMT","EURO",
        "FAPA","FISH","FLMC","FOOD","FORE","GGRM","GOLL","GOOD","GRPM","GULA",
        "GUNA","GZCO","HERO","HMSP","HOKI","IBOS","ICBP","IKAN","INDF","IPPE",
        "ISEA","ITIC","JARR","JAWA","JPFA","KEJU","KINO","KMDS","LAPD","LSIP",
        "MAGP","MAIN","MAXI","MBTO","MGRO","MIDI","MKTR","MLBI","MLPL","MPPA",
        "MRAT","MSJA","MYOR","NANO","NASI","NAYZ","NEST","NSSS","OILS","PCAR",
        "PGUN","PMMP","PNGO","PSDN","PSGO","PTPS","RANC","RLCO","ROTI","SDPC",
        "SGRO","SIMP","SIPD","SKBM","SKLT","SMAR","SOUL","SSMS","STAA","STRK",
        "STTP","TAPG","TAYS","TBLA","TCID","TGKA","TGUK","TLDN","TRGU","UCID",
        "UDNG","ULTJ","UNSP","UNVR","VICI","WAPO","WICO","WIIM","WINE","WMPP",
        "WMUU","YUPI",
    ],
    "Energy": [
        "AADI","ABMM","ADMR","ADRO","AIMS","AKRA","ALII","APEX","ARII","ARTI",
        "ATLA","BBRM","BESS","BIPI","BOAT","BOSS","BSML","BSSR","BULL","BUMI",
        "BYAN","CANI","CBRE","CGAS","CNKO","COAL","CUAN","DEWA","DOID","DSSA",
        "DWGL","ELSA","ENRG","FIRE","GEMS","GTBO","GTSI","HILL","HITS","HRUM",
        "HUMI","IATA","INDY","INPS","ITMA","ITMG","JSKY","KKGI","KOPI","LEAD",
        "MAHA","MBAP","MBSS","MCOL","MEDC","MKAP","MTFN","MYOH","PGAS","PKPK",
        "PSAT","PSSI","PTBA","PTIS","PTRO","RAJA","RATU","RGAS","RIGS","RMKE",
        "RMKO","RUIS","SEMA","SGER","SHIP","SICO","SMMT","SMRU","SOCI","SUGI",
        "SUNI","SURE","TAMU","TCPI","TEBE","TOBA","TPMA","TRAM","UNIQ","WINS",
        "WOWS",
    ],
    "Financials": [
        "ABDA","ADMF","AGRO","AGRS","AHAP","AMAG","AMAR","AMOR","APIC","ARTO",
        "ASBI","ASDM","ASJT","ASMI","ASRM","BABP","BACA","BANK","BBCA","BBHI",
        "BBKP","BBLD","BBMD","BBNI","BBRI","BBSI","BBTN","BBYB","BCAP","BCIC",
        "BDMN","BEKS","BFIN","BGTG","BHAT","BINA","BJBR","BJTM","BKSW","BMAS",
        "BMRI","BNBA","BNGA","BNII","BNLI","BPFI","BPII","BRIS","BSIM","BSWD",
        "BTPN","BTPS","BVIC","CASA","CFIN","COIN","DEFI","DNAR","DNET","FUJI",
        "GSMF","HDFA","INPC","JMAS","LIFE","LPGI","LPPS","MASB","MAYA","MCOR",
        "MEGA","MREI","MTWI","NICK","NISP","NOBU","OCAP","PADI","PALM","PANS",
        "PEGE","PLAS","PNBN","PNBS","PNIN","PNLF","POLA","POOL","RELI","SDRA",
        "SFAN","SMMA","SRTG","STAR","SUPA","TIFA","TRIM","TRUS","TUGU","VICO",
        "VINS","VRNA","VTNY","WOMF","YOII","YULE",
    ],
    "Healthcare": [
        "BMHS","CARE","CHEK","DGNS","DKHH","DVLA","HALO","HEAL","IKPM","INAF",
        "IRRA","KAEF","KLBF","LABS","MDLA","MEDS","MERK","MIKA","MMIX","MTMH",
        "OBAT","OMED","PEHA","PEVE","PRAY","PRDA","PRIM","PYFA","RSCH","RSGK",
        "SAME","SCPI","SIDO","SILO","SOHO","SRAJ","SURI","TSPC",
    ],
    "Industrials": [
        "AMFG","AMIN","APII","ARKA","ARNA","ASGR","ASII","BHIT","BINO","BLUE",
        "BNBR","CAKK","CCSI","CRSN","CTTH","DYAN","FOLK","GPSO","HEXA","HOPE",
        "HYGN","IBFN","ICON","IKAI","IKBI","IMPC","INDX","INTA","JECC","JTPE",
        "KBLI","KBLM","KIAS","KING","KOBX","KOIN","KONI","KUAS","LABA","LION",
        "MARK","MDRN","MFMI","MHKI","MLIA","MUTU","NAIK","NTBK","PADA","PIPA",
        "PTMP","SCCO","SINI","SKRN","SMIL","SOSS","SPTO","TIRA","TOTO","TRIL",
        "UNTR","VISI","VOKS","WIDI","ZBRA",
    ],
    "Infrastructures": [
        "ACST","ADHI","ARKO","ASLI","BALI","BDKR","BREN","BTEL","BUKK","CASS",
        "CDIA","CENT","CMNP","DATA","DGIK","EXCL","FIMP","GHON","GMFI","GOLD",
        "HADE","HGII","IBST","IDPR","INET","IPCC","IPCM","ISAT","JAST","JKON",
        "JSMR","KARW","KBLV","KEEN","KETR","KOKA","KRYA","LCKM","LINK","MANG",
        "META","MORA","MPOW","MTEL","MTPS","MTRA","NRCA","OASA","PBSA","PGEO",
        "PORT","POWR","PPRE","PTDU","PTPP","PTPW","RONY","SMKM","SSIA","SUPR",
        "TAMA","TBIG","TGRA","TLKM","TOPS","TOTL","TOWR","WEGE","WIKA","WSKT",
    ],
    "Properties_Real_Estate": [
        "ADCP","AMAN","APLN","ARMY","ASPI","ASRI","ATAP","BAPA","BAPI","BBSS",
        "BCIP","BEST","BIKA","BIPP","BKDP","BKSL","BSBK","BSDE","CBDK","CBPE",
        "CITY","COWL","CPRI","CSIS","CTRA","DADA","DART","DILD","DMAS","DUTI",
        "ELTY","EMDE","FMII","GAMA","GMTD","GPRA","GRIA","HBAT","HOMI","INDO",
        "INPP","IPAC","JRPT","KBAG","KIJA","KOCI","KSIX","LAND","LCGP","LPCK",
        "LPKR","LPLI","MDLN","MKPI","MMLP","MPRO","MSIE","MTLA","MTSM","NASA",
        "NIRO","NZIA","OMRE","PAMG","PANI","PLIN","POLI","POLL","POSA","PPRO",
        "PUDP","PURI","PWON","RBMS","RDTX","REAL","RELF","RIMO","RISE","ROCK",
        "RODA","SAGE","SATU","SMDM","SMRA","TARA","TRIN","TRUE","UANG","URBN",
        "VAST","WINR",
    ],
    "Technology": [
        "AREA","ATIC","AWAN","AXIO","BELI","BUKA","CASH","CHIP","CYBR","DCII",
        "DIVA","DMMX","EDGE","ELIT","EMTK","ENVY","GLVA","GOTO","HDIT","IOTF",
        "IRSX","JATI","KIOS","KREN","LMAS","LUCK","MCAS","MENN","MLPT","MPIX",
        "MSTI","MTDL","NFCX","NINE","PGJO","PTSN","RUNS","SKYB","TECH","TFAS",
        "TOSK","TRON","UVCR","WGSH","WIFI","WIRG","ZYRX",
    ],
    "Transportation_Logistic": [
        "AKSI","ASSA","BIRD","BLOG","BLTA","BPTR","CMPP","DEAL","ELPI","GIAA",
        "GTRA","HAIS","HATM","HELI","IMJS","JAYA","KJEN","KLAS","LAJU","LOPI",
        "LRNA","MIRA","MITI","MPXL","NELY","PJHB","PPGL","PURA","RCCC","SAFE",
        "SAPX","SDMU","SMDR","TAXI","TMAS","TNCA","TRJA","TRUK","WEHA",
    ],
}
IDX_LQ45 = [
    "ADRO","AKRA","AMRT","ANTM","ASII","BBCA","BBNI","BBRI","BBTN","BMRI",
    "BRPT","BSDE","BUKA","CPIN","CTRA","EMTK","EXCL","GGRM","GOTO","HMSP",
    "HRUM","ICBP","INCO","INDF","INKP","INTP","ISAT","ITMG","JPFA","JSMR",
    "KLBF","LSIP","MAPI","MEDC","MIKA","MNCN","MTEL","MYOR","PGAS","PTBA",
    "PTPP","PWON","SMGR","SMRA","TBIG","TKIM","TLKM","TOWR","TPIA","UNTR",
    "UNVR","WIKA",
]

IDX_IDX30 = [
    "ASII","BBCA","BBNI","BBRI","BMRI","BREN","BUKA","CPIN","EXCL","GOTO",
    "HMSP","ICBP","INCO","INDF","INKP","ISAT","ITMG","KLBF","MAPI","MEDC",
    "MIKA","MTEL","PGAS","PTBA","SMGR","TBIG","TKIM","TLKM","TOWR","UNVR",
]


# ================================================================
# HELPERS
# ================================================================
def fetch_history(ticker_symbol, period, interval, retries=3):
    """Fetch yfinance history dengan retry otomatis jika gagal."""
    for attempt in range(retries):
        try:
            s    = yf.Ticker(ticker_symbol)
            hist = s.history(period=period, interval=interval)
            if not hist.empty:
                return hist
            if attempt < retries - 1:
                time.sleep(0.5)
        except Exception:
            if attempt < retries - 1:
                time.sleep(0.5)
    return pd.DataFrame()

def find_pivots(highs, lows, order=3):
    pivot_highs, pivot_lows = [], []
    n = len(highs)
    for i in range(order, n - order):
        if all(highs[i] >= highs[i-j] for j in range(1, order+1)) and \
           all(highs[i] >= highs[i+j] for j in range(1, order+1)):
            pivot_highs.append((i, float(highs[i])))
        if all(lows[i] <= lows[i-j] for j in range(1, order+1)) and \
           all(lows[i] <= lows[i+j] for j in range(1, order+1)):
            pivot_lows.append((i, float(lows[i])))
    return pivot_highs, pivot_lows

def cluster_levels(levels, tolerance_pct=0.015):
    if not levels:
        return []
    levels_sorted = sorted(levels)
    clusters, current = [], [levels_sorted[0]]
    for price in levels_sorted[1:]:
        if (price - current[-1]) / current[-1] <= tolerance_pct:
            current.append(price)
        else:
            clusters.append(round(float(np.mean(current)), 2))
            current = [price]
    clusters.append(round(float(np.mean(current)), 2))
    return clusters

def strength_score(level, highs, lows, closes, tolerance_pct=0.015):
    touches = 0
    for h, l, c in zip(highs, lows, closes):
        if abs(level-h)/level <= tolerance_pct or \
           abs(level-l)/level <= tolerance_pct or \
           abs(level-c)/level <= tolerance_pct:
            touches += 1
    return touches

def safe_avg(series, window):
    val = series.rolling(window).mean().iloc[-1]
    if pd.isna(val) or val <= 0:
        val = series.mean()
    return float(val) if not pd.isna(val) else 0.0

def calc_rsi(closes_array, period=14):
    s = pd.Series(closes_array)
    deltas = s.diff().dropna()
    gain = deltas.clip(lower=0).rolling(period).mean().iloc[-1]
    loss = (-deltas.clip(upper=0)).rolling(period).mean().iloc[-1]
    if pd.isna(gain) or pd.isna(loss) or loss == 0:
        return 50.0
    return round(100 - (100 / (1 + gain / loss)), 2)

# ================================================================
# ENDPOINT: Stock Data (Screener)
# ================================================================
@app.route("/stock/<symbol>")
def stock(symbol):
    symbol = symbol.upper().strip()
    ticker = symbol + ".JK"
    try:
        hist = fetch_history(ticker, "30d", "1d")
        if hist.empty:
            return jsonify({"error": f"Emiten {symbol} tidak ditemukan atau data tidak tersedia di Yahoo Finance"}), 404

        close  = float(hist["Close"].iloc[-1])
        open_  = float(hist["Open"].iloc[-1])
        high   = float(hist["High"].iloc[-1])
        low    = float(hist["Low"].iloc[-1])
        volume = int(hist["Volume"].iloc[-1])
        ma5    = safe_avg(hist["Close"], 5)
        ma20   = safe_avg(hist["Close"], 20)
        avg_vol= safe_avg(hist["Volume"], 5)

        prev_close = float(hist["Close"].iloc[-2]) if len(hist) >= 2 else close
        change     = round(close - prev_close, 2)
        change_pct = round((change / prev_close) * 100, 2) if prev_close else 0
        body       = abs(close - open_)
        range_     = high - low
        body_ratio = round(body / range_, 2) if range_ != 0 else 0
        gap        = round((close - open_) / open_ * 100, 2) if open_ != 0 else 0
        rsi        = calc_rsi(hist["Close"].values)

        week52  = fetch_history(ticker, "1y", "1d")
        high52  = round(float(week52["High"].max()), 2) if not week52.empty else high
        low52   = round(float(week52["Low"].min()),  2) if not week52.empty else low

        return jsonify({
            "emiten": symbol, "price": round(close, 2),
            "open": round(open_, 2), "high": round(high, 2),
            "low": round(low, 2), "volume": volume,
            "avg_volume": int(avg_vol), "ma5": round(ma5, 2),
            "ma20": round(ma20, 2), "body_ratio": body_ratio,
            "gap": gap, "change": change, "change_pct": change_pct,
            "rsi": rsi, "high_52w": high52, "low_52w": low52,
        })
    except Exception as e:
        return jsonify({"error": f"Gagal mengambil data {symbol}: {str(e)}"}), 500

# ================================================================
# ENDPOINT: Backtest
# ================================================================
@app.route("/backtest/<symbol>")
def backtest(symbol):
    symbol = symbol.upper().strip()
    ticker = symbol + ".JK"
    try:
        hist = fetch_history(ticker, "120d", "1d")
        if hist.empty:
            return jsonify({"error": f"Emiten {symbol} tidak ditemukan atau data tidak tersedia"}), 404

        wins, total = 0, 0
        for i in range(20, len(hist) - 1):
            today    = hist.iloc[i]
            tomorrow = hist.iloc[i + 1]
            ma5      = hist["Close"].rolling(5).mean().iloc[i]
            avg_vol  = hist["Volume"].rolling(5).mean().iloc[i]
            if pd.isna(ma5) or pd.isna(avg_vol) or avg_vol == 0:
                continue
            trend      = today["Close"] > ma5
            momentum   = (today["High"] - today["Close"]) / today["High"] < 0.02
            vol_score  = today["Volume"] / avg_vol * 100
            body       = abs(today["Close"] - today["Open"])
            range_     = today["High"] - today["Low"]
            body_ratio = body / range_ if range_ != 0 else 0
            gap        = (today["Close"] - today["Open"]) / today["Open"] * 100 if today["Open"] != 0 else 0
            score = 0
            if trend:            score += 30
            if momentum:         score += 30
            if vol_score > 130:  score += 40
            if body_ratio > 0.6: score += 20
            if gap > 1:          score += 20
            if score >= 80:
                total += 1
                gain = (tomorrow["Close"] - today["Close"]) / today["Close"] * 100
                if gain > 2:
                    wins += 1

        winrate = round((wins / total) * 100, 2) if total > 0 else 0
        return jsonify({"symbol": symbol, "signal_count": total, "wins": wins, "winrate": winrate})
    except Exception as e:
        return jsonify({"error": f"Gagal backtest {symbol}: {str(e)}"}), 500

# ================================================================
# ENDPOINT: Support & Resistance
# ================================================================
@app.route("/sr/<symbol>")
def support_resistance(symbol):
    symbol = symbol.upper().strip()
    ticker = symbol + ".JK"
    try:
        hist = fetch_history(ticker, "6mo", "1d")
        if hist.empty:
            return jsonify({"error": f"Emiten {symbol} tidak ditemukan atau data tidak tersedia"}), 404
        if len(hist) < 20:
            return jsonify({"error": f"Data {symbol} tidak cukup (hanya {len(hist)} hari, butuh minimal 20)"}), 404

        highs  = hist["High"].values
        lows   = hist["Low"].values
        closes = hist["Close"].values

        current_price = float(closes[-1])
        current_open  = float(hist["Open"].iloc[-1])
        current_high  = float(highs[-1])
        current_low   = float(lows[-1])

        pivot_highs, pivot_lows = find_pivots(highs, lows, order=3)
        resistance_levels = cluster_levels([p[1] for p in pivot_highs])
        support_levels    = cluster_levels([p[1] for p in pivot_lows])

        def enrich(levels, kind):
            result = []
            for lvl in levels:
                strength = strength_score(lvl, highs, lows, closes)
                dist_pct = round((lvl - current_price) / current_price * 100, 2)
                result.append({"price": lvl, "strength": strength, "dist_pct": dist_pct, "type": kind})
            result.sort(key=lambda x: abs(x["dist_pct"]))
            return result[:6]

        resistances = enrich([l for l in resistance_levels if l > current_price], "resistance")
        supports     = enrich([l for l in support_levels    if l < current_price], "support")

        period_high = float(max(highs))
        period_low  = float(min(lows))
        fib_range   = period_high - period_low
        fib_levels  = {
            "0.0":   round(period_low, 2),
            "0.236": round(period_low + 0.236 * fib_range, 2),
            "0.382": round(period_low + 0.382 * fib_range, 2),
            "0.5":   round(period_low + 0.5   * fib_range, 2),
            "0.618": round(period_low + 0.618 * fib_range, 2),
            "0.786": round(period_low + 0.786 * fib_range, 2),
            "1.0":   round(period_high, 2),
        }

        nearest_res = resistances[0]["price"] if resistances else None
        nearest_sup = supports[0]["price"]    if supports    else None
        price_bins  = np.histogram(closes, bins=20)
        max_bin_idx = int(np.argmax(price_bins[0]))
        consolidation_low  = round(float(price_bins[1][max_bin_idx]), 2)
        consolidation_high = round(float(price_bins[1][max_bin_idx + 1]), 2)
        rsi = calc_rsi(closes)

        if nearest_sup and nearest_res:
            range_sr     = nearest_res - nearest_sup
            pos_in_range = (current_price - nearest_sup) / range_sr if range_sr != 0 else 0.5
            if pos_in_range < 0.3:
                signal, signal_type = "DEKAT SUPPORT — Potensi Pantul", "bullish"
            elif pos_in_range > 0.7:
                signal, signal_type = "DEKAT RESISTANCE — Waspadai Penolakan", "bearish"
            else:
                signal, signal_type = "DI TENGAH RANGE — Tunggu Konfirmasi", "neutral"
        else:
            signal, signal_type = "—", "neutral"

        candles = []
        for idx, row in hist.tail(60).iterrows():
            candles.append({
                "date":   str(idx.date()),
                "open":   round(float(row["Open"]),  2),
                "high":   round(float(row["High"]),  2),
                "low":    round(float(row["Low"]),   2),
                "close":  round(float(row["Close"]), 2),
                "volume": int(row["Volume"]),
            })

        return jsonify({
            "symbol": symbol, "price": round(current_price, 2),
            "open": round(current_open, 2), "high": round(current_high, 2),
            "low": round(current_low, 2), "rsi": rsi,
            "resistances": resistances, "supports": supports,
            "fibonacci": fib_levels, "period_high": round(period_high, 2),
            "period_low": round(period_low, 2), "nearest_res": nearest_res,
            "nearest_sup": nearest_sup,
            "consolidation": {"low": consolidation_low, "high": consolidation_high},
            "signal": signal, "signal_type": signal_type,
            "candles": candles, "data_period": "6 Bulan",
        })
    except Exception as e:
        return jsonify({"error": f"Gagal mengambil data SR {symbol}: {str(e)}"}), 500

# ================================================================
# ENDPOINT: Volume Single
# ================================================================
@app.route("/volume/<symbol>")
def volume_single(symbol):
    symbol = symbol.upper().strip()
    ticker = symbol + ".JK"
    try:
        hist = fetch_history(ticker, "3mo", "1d")
        if hist.empty:
            return jsonify({"error": f"Emiten {symbol} tidak ditemukan atau data tidak tersedia"}), 404
        if len(hist) < 10:
            return jsonify({"error": f"Data {symbol} tidak cukup (hanya {len(hist)} hari)"}), 404

        closes  = hist["Close"].values
        volumes = hist["Volume"].values
        dates   = [str(d.date()) for d in hist.index]

        avg_vol_20 = safe_avg(hist["Volume"], 20)
        avg_vol_5  = safe_avg(hist["Volume"], 5)
        cur_vol    = int(volumes[-1])
        cur_price  = float(closes[-1])
        prev_price = float(closes[-2]) if len(closes) > 1 else cur_price
        change_pct = round((cur_price - prev_price) / prev_price * 100, 2)
        ratio_20   = round(cur_vol / avg_vol_20, 2) if avg_vol_20 > 0 else 0
        ratio_5    = round(cur_vol / avg_vol_5,  2) if avg_vol_5  > 0 else 0

        if ratio_20 >= 3.0:   alert, alert_type = "EXTREME", "extreme"
        elif ratio_20 >= 2.0: alert, alert_type = "HIGH",    "high"
        elif ratio_20 >= 1.3: alert, alert_type = "MODERATE","moderate"
        else:                  alert, alert_type = "NORMAL",  "normal"

        price_up = change_pct > 0
        if alert_type in ("extreme","high") and price_up:
            interpretation, interp_type = "Akumulasi — Volume besar disertai kenaikan harga", "bullish"
        elif alert_type in ("extreme","high") and not price_up:
            interpretation, interp_type = "Distribusi — Volume besar disertai penurunan harga", "bearish"
        elif alert_type == "moderate":
            interpretation, interp_type = "Perhatikan — Volume mulai meningkat di atas rata-rata", "neutral"
        else:
            interpretation, interp_type = "Normal — Tidak ada anomali volume signifikan", "normal"

        avg_arr = hist["Volume"].rolling(20).mean().values
        spikes  = []
        for i in range(20, len(volumes)):
            if not pd.isna(avg_arr[i]) and avg_arr[i] > 0 and volumes[i] / avg_arr[i] >= 1.5:
                spikes.append({
                    "date":    dates[i],
                    "volume":  int(volumes[i]),
                    "ratio":   round(float(volumes[i] / avg_arr[i]), 2),
                    "price":   round(float(closes[i]), 2),
                    "change":  round(float((closes[i]-closes[i-1])/closes[i-1]*100), 2),
                })
        spikes = sorted(spikes, key=lambda x: x["ratio"], reverse=True)[:10]

        chart     = []
        avg20_arr = hist["Volume"].rolling(20).mean().values
        for i in range(len(dates)):
            chart.append({
                "date":   dates[i],
                "volume": int(volumes[i]),
                "avg20":  round(float(avg20_arr[i]), 0) if not np.isnan(avg20_arr[i]) else 0,
                "close":  round(float(closes[i]), 2),
                "change": round(float((closes[i]-closes[i-1])/closes[i-1]*100), 2) if i > 0 else 0,
            })

        rsi = calc_rsi(closes)
        return jsonify({
            "symbol": symbol, "price": round(cur_price, 2),
            "change_pct": change_pct, "volume": cur_vol,
            "avg_vol_20": round(avg_vol_20, 0), "avg_vol_5": round(avg_vol_5, 0),
            "ratio_20": ratio_20, "ratio_5": ratio_5,
            "alert": alert, "alert_type": alert_type,
            "interpretation": interpretation, "interp_type": interp_type,
            "rsi": rsi, "spike_history": spikes, "chart": chart[-60:],
        })
    except Exception as e:
        return jsonify({"error": f"Gagal mengambil data volume {symbol}: {str(e)}"}), 500

# ================================================================
# ENDPOINT: Volume Scan per Sektor
# ================================================================
@app.route("/scan/<sector>")
def volume_scan(sector):
    sector  = sector.strip()
    symbols = SECTORS.get(sector, [])
    if not symbols:
        return jsonify({"error": f"Sektor '{sector}' tidak ditemukan. Tersedia: {list(SECTORS.keys())}"}), 404

    results = []
    errors  = []
    for sym in symbols:
        try:
            ticker = sym + ".JK"
            hist   = fetch_history(ticker, "3mo", "1d")
            if hist.empty or len(hist) < 22:
                errors.append(f"{sym}: data tidak cukup")
                continue
            avg20      = safe_avg(hist["Volume"], 20)
            cur_vol    = int(hist["Volume"].iloc[-1])
            cur_price  = float(hist["Close"].iloc[-1])
            prev_price = float(hist["Close"].iloc[-2])
            change     = round((cur_price - prev_price) / prev_price * 100, 2)
            ratio      = round(cur_vol / avg20, 2) if avg20 > 0 else 0
            if ratio >= 3.0:   alert, atype = "EXTREME",  "extreme"
            elif ratio >= 2.0: alert, atype = "HIGH",     "high"
            elif ratio >= 1.3: alert, atype = "MODERATE", "moderate"
            else:               alert, atype = "NORMAL",   "normal"
            results.append({
                "symbol": sym, "price": round(cur_price, 2),
                "change_pct": change, "volume": cur_vol,
                "avg_vol": round(avg20, 0), "ratio": ratio,
                "alert": alert, "alert_type": atype,
            })
        except Exception as e:
            errors.append(f"{sym}: {str(e)}")
            continue

    results.sort(key=lambda x: x["ratio"], reverse=True)
    return jsonify({"sector": sector, "results": results, "total": len(results), "errors": errors})

# ================================================================
# ENDPOINT: Daftar Sektor
# ================================================================
@app.route("/sectors")
def sectors():
    return jsonify({"sectors": list(SECTORS.keys())})

# ================================================================
# ENDPOINT: Market Scanner — Batch per chunk (Vercel compatible)
# Cara kerja: frontend kirim ?universe=all&chunk=0&size=20
# Backend scan 20 saham sekaligus, return JSON
# Frontend polling chunk berikutnya sampai selesai
# CATATAN: size max 10 di Vercel untuk hindari timeout 10 detik
# ================================================================
@app.route("/market-scan")
def market_scan():
    u        = request.args.get("universe", "all").lower()
    chunk    = int(request.args.get("chunk", 0))
    # Batasi max 10 per chunk di Vercel agar tidak timeout
    size     = min(int(request.args.get("size", 10)), 10)

    if u == "lq45":    universe = IDX_LQ45
    elif u == "idx30": universe = IDX_IDX30
    else:              universe = IDX_ALL

    total   = len(universe)
    start   = chunk * size
    end     = min(start + size, total)
    batch   = universe[start:end]
    is_last = end >= total

    results = []
    errors  = []
    for sym in batch:
        try:
            ticker = sym + ".JK"
            hist   = fetch_history(ticker, "1mo", "1d")
            if hist.empty or len(hist) < 15:
                errors.append(f"{sym}: data tidak cukup")
                continue

            closes    = hist["Close"].values
            rsi       = calc_rsi(closes)
            if rsi < 30 or rsi > 70:
                cur_price = round(float(closes[-1]), 2)
                prev      = float(closes[-2]) if len(closes) > 1 else cur_price
                chg_pct   = round((cur_price - prev) / prev * 100, 2)
                vol       = int(hist["Volume"].iloc[-1])
                avg_vol   = safe_avg(hist["Volume"], 20)
                vol_ratio = round(vol / avg_vol, 2) if avg_vol > 0 else 0
                ma20      = safe_avg(hist["Close"], 20)
                results.append({
                    "sym":           sym,
                    "rsi":           rsi,
                    "price":         cur_price,
                    "change_pct":    chg_pct,
                    "volume":        vol,
                    "vol_ratio":     vol_ratio,
                    "ma20":          round(ma20, 2),
                    "condition":     "OVERBOUGHT" if rsi >= 70 else "OVERSOLD",
                    "condition_cls": "overbought" if rsi >= 70 else "oversold",
                })
        except Exception as e:
            errors.append(f"{sym}: {str(e)}")
            continue

    return jsonify({
        "chunk":      chunk,
        "total":      total,
        "scanned":    end,
        "is_last":    is_last,
        "results":    results,
        "errors":     errors,
        "next_chunk": chunk + 1 if not is_last else None,
    })


# ================================================================
if __name__ == "__main__":
    app.run(debug=True, port=5000, threaded=True)