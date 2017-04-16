from __future__ import print_function
from pyspark import SparkContext
from datetime import datetime
from csv import reader
from csv import writer

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


def name_of_type(x):
    if not x:
        return "null"
    try:
        int(x)
        return "int"
    except ValueError:
        pass
    try:
        float(x)
        return "decimal"
    except ValueError:
        pass
    try:
        datetime.strptime(x, '%m/%d/%Y')
        return "date"
    except ValueError:
        pass
    try:
        datetime.strptime(x, '%H:%M:%S')
        return "time"
    except ValueError:
        pass
    return "string"


def check_type(x):
    return (name_of_type(x[0]) == "int" and name_of_type(x[1]) == "date" or "null" and
            name_of_type(x[2]) == "time" and name_of_type(x[3]) == ("date" or "null") and
            name_of_type(x[4]) == ('time' or 'null') and name_of_type(x[5]) == "date" and
            name_of_type(x[6]) == "int" and name_of_type(x[7]) != "null" and
            name_of_type(x[8]) == "int" and name_of_type(x[9]) != "null" and
            name_of_type(x[10]) != "null" and name_of_type(x[11]) != "null" and
            name_of_type(x[12]) != "null" and name_of_type(x[13]) != "null" and
            name_of_type(x[14]) == "int" and name_of_type(x[19]) == "int" and
            name_of_type(x[20]) == "int" and name_of_type(x[21]) == ("int" or "decimal") and
            name_of_type(x[22]) == ("int"or "decimal") and name_of_type(x[23]) != "null")


def check_1_year(x):
    if not x[1]:
        return "null"
    mm_dd_yyyy = x[1].split("/")
    try:
        year = int(mm_dd_yyyy[2])
        if year >= 2006:
            return "valid"
        else:
            return "invalid"
    except:
        return "error"


def check_1_2_3_4_is_time_valid(x):
    if (not x[1]) or (not x[2]):
        return "null"
    if (not x[3]) and (not x[4]):
        return "valid"
    if x[3] and x[4]:
        try:
            from_time = datetime.strptime(x[1] + x[2], '%m/%d/%Y%H:%M:%S')
            to_time = datetime.strptime(x[3] + x[4], '%m/%d/%Y%H:%M:%S')
            if from_time <= to_time:
                return "valid"
        except ValueError:
            return "invalid"


def check_6_7_ky_code(x):
    if (not x[6]) or (not x[7]):
        return "null"
    if dic_6_7[x[6]] == x[7]:
        return "valid"


def check_8_9_pd_code(x):
    if (not x[8]) or (not x[9]):
        return "null"
    try:
        if dic_8_9[x[8]] == x[9]:
            return "valid"
    except:
        print(x)


def check_validation(x):
    return check_1_year(x) == "valid" and check_1_2_3_4_is_time_valid(x) == "valid" and \
           check_6_7_ky_code(x) == "valid" and check_8_9_pd_code(x) == "valid"


def is_valid(x):
    return check_type(x) and check_validation(x)


def write_csv(x):
    output = StringIO("")
    writer(output).writerow(x)
    return output.getvalue().strip()


dic_6_7 = {'347': 'INTOXICATED & IMPAIRED DRIVING', '881': 'OTHER TRAFFIC INFRACTION', '578': 'HARRASSMENT 2', '572': 'DISORDERLY CONDUCT', '571': 'LOITERING/GAMBLING (CARDS', '577': 'UNDER THE INFLUENCE OF DRUGS', '455': 'UNLAWFUL POSS. WEAP. ON SCHOOL', '115': 'PROSTITUTION & RELATED OFFENSES', '114': 'ARSON', '117': 'DANGEROUS DRUGS', '116': 'SEX CRIMES', '238': 'FRAUDULENT ACCOSTING', '110': 'GRAND LARCENY OF MOTOR VEHICLE', '113': 'FORGERY', '112': 'THEFT-FRAUD', '234': 'PROSTITUTION & RELATED OFFENSES', '235': 'DANGEROUS DRUGS', '236': 'DANGEROUS WEAPONS', '237': 'ESCAPE 3', '230': 'JOSTLING', '231': "BURGLAR'S TOOLS", '232': 'POSSESSION OF STOLEN PROPERTY', '233': 'SEX CRIMES', '119': 'INTOXICATED/IMPAIRED DRIVING', '118': 'DANGEROUS WEAPONS', '344': 'ASSAULT 3 & RELATED OFFENSES', '345': 'OFFENSES RELATED TO CHILDREN', '346': 'ALCOHOLIC BEVERAGE CONTROL LAW', 'KY_CD': 'OFNS_DESC', '340': 'FRAUDS', '341': 'PETIT LARCENY', '342': 'PETIT LARCENY OF MOTOR VEHICLE', '343': 'THEFT OF SERVICES', '366': 'NEW YORK CITY HEALTH CODE', '364': 'OTHER STATE LAWS (NON PENAL LA', '365': 'ADMINISTRATIVE CODE', '362': 'OFFENSES AGAINST MARRIAGE UNCL', '363': 'OFFENSES AGAINST PUBLIC SAFETY', '360': 'LOITERING FOR DRUG PURPOSES', '361': 'OFF. AGNST PUB ORD SENSBLTY ', '678': 'MISCELLANEOUS PENAL LAW', '109': 'GRAND LARCENY', '675': 'ADMINISTRATIVE CODE', '676': 'NEW YORK CITY HEALTH CODE', '677': 'NYS LAWS-UNCLASSIFIED VIOLATION', '460': 'LOITERING/DEVIATE SEX', '672': 'LOITERING', 'N': 'U', '120': 'CHILD ABANDONMENT/NON SUPPORT', '121': 'CRIMINAL MISCHIEF & RELATED OF', '122': 'GAMBLING', '123': 'ABORTION', '124': 'KIDNAPPING & RELATED OFFENSES', '125': 'NYS LAWS-UNCLASSIFIED FELONY', '126': 'MISCELLANEOUS PENAL LAW', '102': 'HOMICIDE-NEGLIGENT-VEHICLE', '103': 'HOMICIDE-NEGLIGENT', '101': 'MURDER & NON-NEGL. MANSLAUGHTER', '106': 'FELONY ASSAULT', '107': 'BURGLARY', '104': 'RAPE', '105': 'ROBBERY', '348': 'VEHICLE AND TRAFFIC LAWS', '349': 'DISRUPTION OF A RELIGIOUS SERV', '357': 'FORTUNE TELLING', '356': 'PROSTITUTION & RELATED OFFENSES', '355': 'OFFENSES AGAINST THE PERSON', '354': 'ANTICIPATORY OFFENSES', '353': 'UNAUTHORIZED USE OF A VEHICLE', '352': 'CRIMINAL TRESPASS', '351': 'CRIMINAL MISCHIEF & RELATED OF', '350': 'GAMBLING', '685': 'ADMINISTRATIVE CODES', '111': 'POSSESSION OF STOLEN PROPERTY', '359': 'OFFENSES AGAINST PUBLIC ADMINI', '358': 'OFFENSES INVOLVING FRAUD'}

dic_8_9 = {'818': 'ABANDON ANIMAL', '819': 'EDUCATION LAW,STREET TRADE', '347': 'PETIT LARCENY-CHECK FROM MAILB', '341': 'LARCENY,PETIT OF AUTO', '342': 'LARCENY, PETIT OF AUTO - ATTEM', '343': 'LARCENY,PETIT OF BICYCLE', '811': 'DOG STEALING', '812': 'AGRICULTURE & MARKETS LAW,UNCL', '814': 'ATTEND/SPECTATOR ANIMAL FIGHTING', '815': 'NEGLECT/POISON ANIMAL', '817': 'TORTURE/INJURE ANIMAL CRUELTY', '719': 'FRAUD,UNCLASSIFIED-MISDEMEANOR', '718': 'FRAUD,UNCLASSIFIED-MISDEMEANOR', '715': 'POSSESSION ANTI-SECURITY ITEM', '711': 'TAMPERING WITH A WITNESS', '916': 'LEAVING SCENE-ACCIDENT-PERSONA', '299': 'FACILITATION 3,2,1, CRIMINAL', '297': 'FACILITATION 4, CRIMINAL', '293': 'CONSPIRACY 2, 1', '291': 'CONSPIRACY 4, 3', '591': 'OBSCENITY, PERFORMANCE 3', '593': 'OBSCENITY, MATERIAL 3', '595': 'UNLAWFUL POSS. WEAPON UPON SCH', '594': 'OBSCENITY 1', '596': 'OBSCENE MATERIAL - UNDER 17 YE', '195': 'COERCION 2', '197': 'COERCION 1', '191': 'CUSTODIAL INTERFERENCE 2', '193': 'CUSTODIAL INTERFERENCE 1', '271': 'TAMPERING 3,2, CRIMINAL', '273': 'TAMPERING 1,CRIMINAL', '275': 'POSTING ADVERTISEMENTS', '277': 'RECKLESS ENDANGERMENT OF PROPE', 'PD_CD': 'PD_DESC', '524': 'CONTROLLED SUBSTANCE,POSSESS', '520': 'CONTROLLED SUBSTANCE, SALE 4', '521': 'CONTROLLED SUBSTANCE, SALE 5', '522': 'USE CHILD TO COMMIT CONT SUB OFF', '523': 'SALE SCHOOL GROUNDS', '529': 'SALES OF PRESCRIPTION', '345': 'LARCENY,PETIT OF BOAT', '443': 'LARCENY,GRAND OF BICYCLE', '442': 'LARCENY, GRAND OF AUTO - ATTEM', '441': 'LARCENY,GRAND OF AUTO', '447': 'GRAND LARCENY-CHECK FROM MAILB', '445': 'LARCENY,GRAND OF BOAT', '109': 'ASSAULT 2,1,UNCLASSIFIED', '101': 'ASSAULT 3', '106': 'ASSAULT 2,1,PEACE OFFICER', '107': 'END WELFARE VULNERABLE ELDERLY PERSON', '104': 'VEHICULAR ASSAULT (INTOX DRIVE', '105': 'STRANGULATION 1ST', '907': 'IMPAIRED DRIVING,DRUG', '904': 'INTOXICATED DRIVING,ALCOHOL', '905': 'INTOXICATED DRIVING,ALCOHOL', '641': 'HEALTHCARE/RENT.REG', '640': 'AGGRAVATED HARASSMENT 1', '643': 'ASSEMBLY,UNLAWFUL', '645': 'FALSE ALARM FIRE', '644': 'FALSE REPORT 1,FIRE', '438': 'LARCENY,GRAND FROM BUILDING (NON-RESIDENCE) UNATTENDED', '646': 'DISSEMINATING A FALSE SEX OFFEND', '436': 'LARCENY,GRAND BY CREDIT CARD COMPROMISE-UNAUTHORIZE PURCHASE', '437': 'LARCENY,GRAND BY FALSE PROMISE-IN PERSON CONTACT', '434': 'LARCENY,GRAND BY OPEN BANK ACCT', '435': 'LARCENY,GRAND FROM TRUCK, UNATTENDED', '432': 'LARCENY,GRAND BY IDENTITY THEFT-UNCLASSIFIED', '433': 'LARCENY,GRAND FROM STORE-SHOPL', '430': 'LARCENY,GRAND BY BANK ACCT COMPROMISE-UNCLASSIFIED', '431': 'LARCENY,GRAND FROM PIER, UNATTENDED', '339': 'LARCENY,PETIT FROM OPEN AREAS', '338': 'LARCENY,PETIT FROM BUILDING,UN', '335': 'LARCENY,PETIT FROM TRUCK', '331': 'LARCENY,PETIT FROM PIER', '333': 'LARCENY,PETIT FROM STORE-SHOPL', '344': 'PETIT LARCENY OF ANIMAL', '853': 'CIGARETTE,NO TAX STAMP,POSSESS', '858': 'IMITATION PISTOL/AIR RIFLE', '349': 'LARCENY,PETIT OF LICENSE PLATE', '742': 'ESCAPE 3', '744': 'BAIL JUMPING 3', '746': 'PERJURY 3,ETC', '748': 'CONTEMPT,CRIMINAL', '749': 'VIOLATION OF ORDER OF PROTECTI', '557': 'GAMBLING 1,PROMOTING,POLICY', '553': 'GAMBLING 1,PROMOTING,BOOKMAKIN', '234': 'BURGLARY,UNKNOWN TIME', '231': 'BURGLARY,TRUCK DAY', '233': 'BURGLARY,TRUCK NIGHT', '146': 'ABORTION 2, 1, SELF', '618': 'LOITERING FOR PROSTITUTION OR', '619': 'LOITERING,UNCLASSIFIED', '143': 'ABORTION 1', '610': 'LOITERING,GAMBLING,OTHER', '614': 'LOITERING,SCHOOL', '689': 'MARRIAGE,OFFENSES AGAINST,UNCL', '688': 'INCOMPETENT PERSON,RECKLESSY ENDANGERING', '685': 'CHILD,LICENSED PREMISES', '687': 'CHILD,OFFENSES AGAINST,UNCLASS', '681': 'CHILD, ENDANGERING WELFARE', '683': 'CHILD,ALCOHOL SALE TO', '498': 'STOLEN PROPERTY 2,POSSESSION B', '494': 'STOLEN PROPERTY 2,1,POSSESSION', '490': 'STOLEN PROPERTY 3,POSSESSION', '491': 'STOLEN PROP-MOTOR VEHICLE 3RD', '493': 'STOLEN PROPERTY-MOTOR VEH 2ND', '407': 'LARCENY,GRAND BY DISHONEST EMP', '406': 'LARCENY,GRAND FROM PERSON, BAG OPEN/DIP', '405': 'LARCENY,GRAND BY THEFT OF CREDIT CARD', '404': 'LARCENY,GRAND FROM PERSON,PERSONAL ELECTRONIC DEVICE(SNATCH', '403': 'LARCENY,GRAND BY BANK ACCT COMPROMISE-REPRODUCED CHECK', '402': 'LARCENY,GRAND BY FALSE PROMISE-NOT IN PERSON CONTACT', '401': 'LARCENY,GRAND BY ACQUIRING LOS', '409': 'LARCENY,GRAND BY EXTORTION', '408': 'LARCENY,GRAND FROM PERSON,LUSH WORKER(SLEEPING/UNCON VICTIM', '379': 'ROBBERY,GAS STATION', '829': 'LABOR LAW,EMPLOYING CHILDREN', '371': 'ROBBERY,CHECK CASHING BUSINESS', '827': 'GENERAL BUSINESS LAW / UNCLASSIFIED', '826': 'GENERAL BUSINESS LAW,TICKET SP', '375': 'ROBBERY,PHARMACY', '820': 'EDUCATION LAW, TRUANCY', '377': 'ROBBERY,BODEGA/CONVENIENCE STORE', '822': 'EDUCATION LAW', '708': 'IMPERSONATION 1, POLICE OFFICE', '705': 'FORGERY,ETC.-MISD', '706': 'RECORDS,FALSIFY-TAMPER', '707': 'IMPERSONATION 2, PUBLIC SERVAN', '701': 'BRIBERY,COMMERCIAL', '703': 'CHECK,BAD', '393': 'ROBBERY,OF TRUCK DRIVER', '392': 'ROBBERY,UNLICENSED FOR HIRE VEHICLE', '391': 'ROBBERY,LICENSED MEDALLION CAB', '390': 'ROBBERY,HOME INVASION', '397': 'ROBBERY,OPEN AREA UNCLASSIFIED', '396': 'ROBBERY,BEGIN AS SHOPLIFTING', '395': 'ROBBERY,ON BUS/ OR BUS DRIVER', '394': 'ROBBERY,LICENSED FOR HIRE VEHICLE', '399': 'ROBBERY,COMMERCIAL UNCLASSIFIED', '398': 'ROBBERY,PUBLIC PLACE INSIDE', '797': 'WOUNDS,REPORTING OF', '796': 'WEAPONS,PROHIBITED USE', '793': 'WEAPONS POSSESSION 3', '792': 'WEAPONS POSSESSION 1 & 2', '799': 'PUBLIC SAFETY,UNCLASSIFIED MIS', '170': 'SEXUAL MISCONDUCT,INTERCOURSE', '586': 'SEX TRAFFICKING', '587': 'PROSTITUTION 2, COMPULSORY', '584': 'PROSTITUTION 3, PROMOTING UNDE', '585': 'PROSTITUTION 3,PROMOTING BUSIN', '588': 'PROSTITUTION 2, UNDER 16', '589': 'PROSTITUTION 1, UNDER 11', '244': 'BURGLARY,UNCLASSIFIED,UNKNOWN', '241': 'BURGLARY,UNCLASSIFIED,DAY', '148': 'ABORTIONAL ARTICLES,ISSUING', '243': 'BURGLARY,UNCLASSIFIED,NIGHT', '248': 'RADIO DEVICES,UNLAWFUL POSSESS', '519': 'SALE SCHOOL GROUNDS 4', '511': 'CONTROLLED SUBSTANCE, POSSESSI', '510': 'CONTROLLED SUBSTANCE, INTENT T', '513': 'POSS METH MANUFACT MATERIAL', '512': 'CONTROLLED SUBSTANCE,SALE 1', '515': 'CONTROLLED SUBSTANCE,SALE 3', '514': 'CONTROLLED SUBSTANCE,SALE 2', '622': 'UNDER THE INFLUENCE OF DRUGS', '627': 'DIS. CON.,AGGRAVATED', '625': 'DISORDERLY CONDUCT', '450': 'LARCENY, GRAND OF MOPED', '451': 'LARCENY,GRAND OF MOTORCYCLE', '455': 'LARCENY,GRAND OF TRUCK', '457': 'LARCENY,GRAND OF VEHICULAR/MOTORCYCLE ACCESSORIES', '179': 'AGGRAVATED SEXUAL ASBUSE', '178': 'FAC. SEXUAL OFFENSE W/CONTROLL', '177': 'SEXUAL ABUSE', '199': 'AGGRAVATED CRIMINAL CONTEMPT', '175': 'SEXUAL ABUSE 3,2', '174': 'SEXUAL MISCONDUCT,DEVIATE', '198': 'CRIMINAL CONTEMPT 1', '975': 'ENVIRONMENTAL CONTROL BOARD', '183': 'IMPRISONMENT 1,UNLAWFUL', '180': 'COURSE OF SEXUAL CONDUCT AGAIN', '181': 'IMPRISONMENT 2,UNLAWFUL', '652': 'RIOT 2/INCITING', '187': 'KIDNAPPING 1', '184': 'LABOR TRAFFICKING', '185': 'KIDNAPPING 2', '186': 'LURING A CHILD', '659': 'NUISANCE,CRIMINAL,UNCLASSIFIED', '868': 'GYPSY CAB', '861': 'AIRPOLLUTION', '860': 'AIR POLLUTION-MOTOR VEH (ADM C', '862': 'ALCOHOLIC BEVERAGES,PUBLIC CON', '864': 'BUILDING MATERIAL', '866': 'FIREWORKS', '880': 'POSSES OR CARRY A KNIFE', '887': 'GRAFFITI (ADMINISTRATIVE CODE', '885': 'SMOKING TRANSPORTATION FACILIT', '889': 'HEALTH CODE,VIOLATION', '888': 'HEALTH CODE,UNCLASSIFIED MISDE', '756': 'ABSCONDING FROM WORK RELEASE 2', '809': 'TAX LAW', '323': 'LARCENY,PETIT FROM BOAT', '321': 'LARCENY,PETIT FROM AUTO', '327': 'LARCENY,PETIT FROM PARKING MET', '329': 'LARCENY,PETIT FROM COIN MACHIN', '775': 'MONEY LAUNDERING 1 & 2', '203': 'TRESPASS 3, CRIMINAL', '205': 'TRESPASS 2, CRIMINAL', '770': 'COMPUTER UNAUTH. USE/TAMPER', '772': 'COMPUTER TAMPER/TRESSPASS', '209': 'BURGLARS TOOLS,UNCLASSIFIED', '779': 'PUBLIC ADMINISTRATION,UNCLASSI', '669': 'PRIVACY,OFFENSES AGAINST,UNCLA', '665': 'MAKING TERRORISTIC THREAT', '664': 'TERRORISM PROVIDE SUPPORT', '663': 'SUPP. ACT TERR 2ND', '662': 'MATERIAL              OFFENSIV', '661': 'LEWDNESS,PUBLIC', '693': 'INCEST', '691': 'BIGAMY', '696': 'PROMOTING A SEXUAL PERFORMANCE', '697': 'USE OF A CHILD IN A SEXUAL PER', '694': 'INCEST', '695': 'CHILD ABANDONMENT', '698': 'INCOMPETENT PERSON,KNOWINGLY ENDANGERING', '544': 'GAMBLING 2,PROMOTING,UNCLASSIF', '548': 'GAMBLING, DEVICE, POSSESSION', '121': 'HOMICIDE,NEGLIGENT,VEHICLE', '122': 'HOMICIDE, NEGLIGENT, VEHICLE', '125': 'HOMICIDE,NEGLIGENT,UNCLASSIFIE', '176': 'SEX CRIMES', '414': 'LARCENY,GRAND PERSON,NECK CHAI', '415': 'LARCENY,GRAND FROM PERSON,PICK', '416': 'LARCENY,GRAND FROM NIGHT CLUB, UNATTENDED', '417': 'LARCENY,GRAND FROM PERSON,PURS', '410': 'LARCENY,GRAND FROM RETAIL STORE, UNATTENDED', '411': 'LARCENY,GRAND FROM EATERY, UNATTENDED', '412': 'LARCENY,GRAND FROM RESIDENCE, UNATTENDED', '413': 'LARCENY,GRAND BY FALSE PROMISE', '922': 'TRAFFIC,UNCLASSIFIED MISDEMEAN', '418': 'LARCENY,GRAND BY ACQUIRING LOST CREDIT CARD', '419': 'LARCENY,GRAND FROM PERSON,UNCL', '313': 'LARCENY,PETIT BY FALSE PROMISE', '836': 'NAVIGATION LAW', '839': 'PUBLIC HEALTH LAW,GLUE,INHALAT', '366': 'ROBBERY,BICYCLE', '367': 'ROBBERY, CHAIN STORE', '365': 'ROBBERY,LIQUOR STORE', '363': 'ROBBERY,BAR/RESTAURANT', '360': 'ROBBERY,ATM LOCATION', '361': 'ROBBERY,BANK', '380': 'ROBBERY,CAR JACKING', '381': 'ROBBERY,HIJACKING', '382': 'ROBBERY,NECKCHAIN/JEWELRY', '384': 'ROBBERY,POCKETBOOK/CARRIED BAG', '385': 'ROBBERY, PAYROLL', '386': 'ROBBERY,PERSONAL ELECTRONIC DEVICE', '387': 'ROBBERY,CLOTHING', '388': 'ROBBERY,RESIDENTIAL COMMON AREA', '389': 'ROBBERY,DWELLING', '784': 'WEAPONS,MFR,TRANSPORT,ETC', '786': 'WEAPONS,PROHIBITED USE', '787': 'WEAPONS,PROHIBITED USE IMITATI', '780': 'NUISANCE, CRIMINAL', '781': 'CRIMINAL DISPOSAL FIREARM 1 ', '782': 'WEAPONS, POSSESSION, ETC', '788': 'FIREWORKS, SALE', '789': 'FIREWORKS, POSSESS/USE', '570': 'MARIJUANA, SALE 1, 2 & 3', '576': 'PROSTITUTION 4,PROMOTING&SECUR', '574': 'PROSTITUTION,PERMITTING', '258': 'CRIMINAL MISCHIEF 4TH, GRAFFIT', '259': 'CRIMINAL MISCHIEF,UNCLASSIFIED 4', '256': 'MISCHIEF, CRIMINAL 4, BY FIRE', '254': 'MISCHIEF, CRIMINAL 4, OF MOTOR', '731': 'SALE OF UNAUTHORIZED RECORDING', '730': 'MANUFACTURE UNAUTHORIZED RECOR', '733': 'ENTERPRISE CORRUPTION', '508': 'DRUG PARAPHERNALIA,   POSSESSE', '509': 'POSSESSION HYPODERMIC INSTRUME', '739': 'FRAUD,UNCLASSIFIED-FELONY', '507': 'CONTROLLED SUBSTANCE, POSSESSI', '505': 'CONTROLLED SUBSTANCE, POSSESSI', '502': 'CONTROLLED SUBSTANCE,POSSESS', '503': 'CONTROLLED SUBSTANCE,INTENT TO', '500': 'CONTROLLED SUBSTANCE,POSSESS', '501': 'CONTROLLED SUBSTANCE,POSSESS', '633': 'EXPOSURE OF A PERSON', '468': 'FORTUNE TELLING', '637': 'HARASSMENT,SUBD 1,CIVILIAN', '638': 'HARASSMENT,SUBD 3,4,5', '639': 'AGGRAVATED HARASSMENT 2', '466': 'ACCOSTING,FRAUDULENT', '461': 'UNAUTHORIZED USE VEHICLE 2', '462': 'UNAUTHORIZED USE VEHICLE 3', '168': 'SODOMY 1', '164': 'SODOMY 3', '166': 'SODOMY 2', '162': 'SODOMY,CONSENSUAL', '969': 'TRAFFIC,UNCLASSIFIED INFRACTIO', '878': 'ADM.CODE,UNCLASSIFIED MISDEMEA', '879': 'ADM.CODE,UNCLASSIFIED VIOLATIO', '874': 'PEDDLING,UNLAWFUL', '872': 'NOISE,UNECESSARY', '890': 'N.Y.C. TRANSIT AUTH. R&R', '892': 'PARK R&R,GAMBLING', '647': 'FALSE REPORT BOMB', '899': 'PARKR&R,UNCLASSIFIED VIOLATION', '439': 'LARCENY,GRAND FROM OPEN AREAS, UNATTENDED', '649': 'FALSE REPORT UNCLASSIFIED', '648': 'PLACE FALSE BOMB', '357': 'LARCENY,PETIT OF VEHICLE ACCES', '355': 'LARCENY,PETIT OF TRUCK', '808': 'TAX LAW', '351': 'LARCENY,PETIT OF MOTORCYCLE', '350': 'LARCENY, PETIT OF MOPED', '803': 'A.B.C.,FALSE PROOF OF AGE', '802': 'ALCOHOLIC BEVERAGE CONTROL LAW', '214': 'BURGLARY,COMMERCIAL,UNKNOWN TI', '213': 'BURGLARY,COMMERCIAL,NIGHT', '211': 'BURGLARY,COMMERCIAL,DAY', '762': 'ESCAPE 2,1', '760': 'BRIBERY,PUBLIC ADMINISTRATION', '761': 'BRIBERY, POLICE OFFICER', '766': 'PERJURY 2,1,ETC', '764': 'BAIL JUMPING 1 & 2', '289': 'CONSPIRACY 6, 5', '281': 'SOLICITATION 5,CRIMINAL', '283': 'SOLICITATION 4, CRIMINAL', '285': 'SOLICITATION 3,2,1, CRIMINAL', '678': 'ANARCHY,CRIMINAL', '674': 'EAVESDROPPING', '672': 'RIOT 1', '263': 'ARSON 2,3,4', '261': 'ARSON 1', '267': 'MISCHIEF, CRIMINAL 3 & 2, OF M', '266': 'MISCHIEF, CRIMINAL 3&2, BY FIR', '265': 'MISCHIEF 1,CRIMINAL,EXPLOSIVE', '264': 'ARSON, MOTOR VEHICLE 1 2 3 & 4', '269': 'MISCHIEF,CRIMINAL,    UNCL 2ND', '268': 'CRIMINAL MIS 2 & 3', '537': 'GAMBLING 2, PROMOTING, POLICY', '533': 'GAMBLING 2, PROMOTING, BOOKMAK', '532': 'CONTROLLED SUBSTANCE,POSSESS', '531': 'DRUG PARAPHERNALIA,   POSSESSE', '530': 'DRUG, INJECTION OF', '201': 'TRESPASS 4,CRIMINAL SUB 2', '115': 'RECKLESS ENDANGERMENT 2', '114': 'OBSTR BREATH/CIRCUL', '117': 'RECKLESS ENDANGERMENT 1', '111': 'MENACING,PEACE OFFICER', '110': 'MENACING 1ST DEGREE (VICT PEAC', '113': 'MENACING,UNCLASSIFIED', '112': 'MENACING 1ST DEGREE (VICT NOT', '119': 'PROMOTING SUICIDE ATTEMPT', '204': 'TRESPASS 1,CRIMINAL', '429': 'LARCENY,GRAND FROM COIN MACHIN', '428': 'LARCENY,GRAND BY BANK ACCT COMPROMISE-UNAUTHORIZED PURCHASE', '918': 'RECKLESS DRIVING', '421': 'LARCENY,GRAND FROM VEHICLE/MOTORCYCLE', '420': 'LARCENY,GRAND BY OPEN/COMPROMISE CELL PHONE ACCT', '423': 'LARCENY,GRAND FROM BOAT, UNATTENDED', '422': 'LARCENY,GRAND BY OPEN CREDIT CARD (NEW ACCT', '425': 'LARCENY,GRAND BY BANK ACCT COMPROMISE-ATM TRANSACTION', '424': 'LARCENY,GRAND BY CREDIT CARD ACCT COMPROMISE-EXISTING ACCT', '427': 'LARCENY,GRAND FROM PARKING MET', '426': 'LARCENY,GRAND BY BANK ACCT COMPROMISE-TELLER', '301': 'LARCENY,PETIT BY ACQUIRING LOS', '303': 'LARCENY,PETIT BY CHECK USE', '305': 'LARCENY,PETIT BY CREDIT CARD U', '307': 'LARCENY,PETIT BY DISHONEST EMP', '373': 'ROBBERY,DOCTOR/DENTIST OFFICE', '847': 'NY STATE LAWS,UNCLASSIFIED FEL', '846': 'CONFINING ANIMAL IN VEHICLE/SHELTER', '845': 'BREED/TRAIN/HOST ANIMAL FIGHTING', '844': 'CAUSE SPI/KILL ANIMAL', '843': 'INAPPROPIATE SHELTER DOG LEFT', '841': 'PUBLIC HEALTH LAW,UNCLASSIFIED', '840': 'PUBLIC HEALTH LAW,GLUE,UNLAWFU', '821': 'EDUCATION LAW,UNCLASSIFIED', '849': 'NY STATE LAWS,UNCLASSIFIED VIO', '848': 'NY STATE LAWS,UNCLASSIFIED MIS', '568': 'MARIJUANA, POSSESSION 1, 2 & 3', '569': 'MARIJUANA, SALE 4 & 5', '750': 'RESISTING ARREST', '737': 'USURY,CRIMINAL', '754': 'APPEARANCE TICKET FAIL TO RESP', '561': 'PROSTITUTION, PATRONIZING 2, 1', '759': 'PUBLIC ADMINISTATION,UNCLASS M', '563': 'PROSTITUTION', '565': 'PROSTITUTION, PATRONIZING 4, 3', '566': 'MARIJUANA, POSSESSION', '567': 'MARIJUANA, POSSESSION 4 & 5', '224': 'BURGLARY,RESIDENCE,UNKNOWN TIM', '223': 'BURGLARY,RESIDENCE,NIGHT', '221': 'BURGLARY,RESIDENCE,DAY', '727': 'FORGERY,PRESCRIPTION', '724': 'FORGERY-ILLEGAL POSSESSION,VEH', '725': 'FORGERY,M.V. REGISTRATION', '723': 'FORGERY,DRIVERS LICENSE', '721': 'BRIBERY,FRAUD', '729': 'FORGERY,ETC.,UNCLASSIFIED-FELO', '605': 'LOITERING TO PROMOTE PROSTITUT', '604': 'LOITERING 1ST DEGREE FOR DRUG', '153': 'RAPE 3', '155': 'RAPE 2', '157': 'RAPE 1', '602': 'LOITERING,DEVIATE SEX', '159': 'RAPE 1,ATTEMPT', '464': 'JOSTLING', '489': 'THEFT,RELATED OFFENSES,UNCLASS', 'N': 'U', '476': 'CREDIT CARD,UNLAWFUL USE OF', '477': 'THEFT OF SERVICES- CABLE TV SE', '475': 'UNAUTH. SALE OF TRANS. SERVICE', '478': 'THEFT OF SERVICES, UNCLASSIFIE', '479': 'THEFT,RELATED OFFENSES,UNCLASS'}
if __name__ == "__main__":
    file_name = "rows.csv"
    # file_name = "ten_thousand_lines_data.csv"
    result_file = "clean_rows.csv"
    sc = SparkContext()
    lines = sc.textFile(file_name, 1)
    cells = lines.mapPartitions(lambda x: reader(x)). \
        filter(lambda x: is_valid(x) is True).\
        map(lambda x: write_csv(x)).\
        saveAsTextFile(result_file)
    sc.stop()