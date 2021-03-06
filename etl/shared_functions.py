#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 20:08:44 2018

@author: chrisstrods
"""
from bs4 import BeautifulSoup
import pandas as pd
import numpy


#Load an html page and return it as s BS table
def loadPage(u):
    #page = urllib.request.urlopen(u)

    soup = BeautifulSoup(open(u), 'html.parser')

    tables = soup.findChildren('table')

    return tables


#Output row to the table
def initSummaries():
    return pd.DataFrame(columns = ['round','venue','date','day',
                                   'time','crowd','hteam','hteam_q1',
                                   'hteam_q2','hteam_q3','hteam_q4',
                                   'ateam','ateam_q1','ateam_q2',
                                   'ateam_q3','ateam_q4','umpire1',
                                   'umpire2','umpire3','umpire1games',
                                   'umpire2games','umpire3games',
                                   'hteam_et','ateam_et','season','matchid'])

def initPlayerStats():
    return pd.DataFrame(columns=['playerid','matchid','team','ha','first_name','last_name',
                                   'number','kicks','marks','handballs',
                                   'disposals','goals','behinds',
                                   'hitouts','tackles','rebound50',
                                   'inside50','clearances','clangers',
                                   'frees_for','frees_against',
                                   'brownlow','contested_poss',
                                   'uncontested_poss','contested_marks',
                                   'marks_in_50','one_percenters',
                                   'bounces','goal_assists','tog'])


#Create unique ID for each game, based on year, round, and teamcode
def createIndex(df):
    df['date'].replace("/","-")
    year = df['season']
    
    if((df["date"] == "2-Oct-2010") or \
       (df["date"] == "9-Oct-1948") or \
       (df["date"] == "1-Oct-1977")):
        tround = getRoundCode("GReplay")
    elif(df["date"] == "22-Sep-1962") :
        tround = str(getRoundCode("PReplay"))
    elif((df["date"] == "23-Sep-1972") or \
         (df["date"] == "22-Sep-1928") or \
         (df["date"] == "21-Sep-1946")):
        tround = str(getRoundCode("SReplay"))
    elif(df["date"] == "15-Sep-1990") :
        tround = str(getRoundCode("QReplay"))
    else:
        tround = getRoundCode(df['round'])
        
    hcode = getTeamCode(df['hteam'])
    acode = getTeamCode(df['ateam'])
    codes = [hcode,acode]
    codes.sort()
    
    
    gindex = str(year) + str(tround) + codes[0] + codes[1]
    return gindex

        #Assign game index to each game


def replaceTeam(team):
    if(team=="Western Bulldogs"):
        return "Footscray"
    elif(team=="Kangaroos"):
        return "North Melbourne"
    else:
        return team


def fixFullName(df):
    
    fullkey = df["fullkey"]
    
    try:
        return {
            '201315ESSPORamoore14' : '201315ESSPORamoore13',
            '201315ESSPORjhombsch3' : '201315ESSPORjhombsch4',
            '201801GCSNORjlyons18' : '201801GCSNORjlyons17',
            '201801GCSNORlweller11' : '201801GCSNORlweller12',
            '201801GCSNORdmacpherson15' : '201801GCSNORdmacpherson14',
            '201801GCSNORnholman7' : '201801GCSNORnholman8',
            '201801GCSNORjmacmillan20' : '201801GCSNORjmacmillan19',
            '201801GCSNORlmcdonald9' : '201801GCSNORlmcdonald10',
            '201802FOTWEGtmclean14' : '201802FOTWEGtmclean15',
            '201802FOTWEGanaughton9' : '201802FOTWEGanaughton8',
            '201809CARMELskerridge14' : '201809CARMELskerridge15',
            '201809CARMELmkreuzer7' : '201809CARMELmkreuzer6',
            '201815COLGCSdswallow17' : '201815COLGCSdswallow16',
            '201815FOTGEEgablett18' : '201815FOTGEEgablett17',
            '201823ADECARdthomas12' : '201823ADECARdthomas11',
            '2018QFHAWRCHdrioli7' : '2018QFHAWRCHdrioli8',
            '2018QFHAWRCHjriewoldt10' : '2018QFHAWRCHjriewoldt9',
            '201901ESSGWSatomlinson16' : '201901ESSGWSatomlinson15',
            '201903HAWNORdmirra12' : '201903HAWNORdmirra13',
            '201903HAWNORjomeara17' : '201903HAWNORjomeara16',
            '201907CARNORjanderson13' : '201907CARNORjanderson12',
            '201908FRERCHjcaddy17' : '201908FRERCHjcaddy16',
            '201908STKWEGjnewnes7' : '201908STKWEGjnewnes8',
            '201909CARGWSnhaynes15' : '201909CARGWSnhaynes14',
            '201909FOTGEEtmclean13' : '201909FOTGEEtmclean12',
            '201909GCSPORtrockliff21' : '201909GCSPORtrockliff20',
            '201915ESSGWSttaranto14' : '201915ESSGWSttaranto13',
            '201915FOTPORbsmith8' : '201915FOTPORbsmith9',
            '201915FOTPORrsmith15' : '201915FOTPORrsmith14',
            '201919MELSTKjgresham23' : '201919MELSTKjgresham22',
            '201921ADEWEGeyeo13' : '201921ADEWEGeyeo12',
            '2019EFESSWEGdshiel14' : '2019EFESSWEGdshiel13',
            '2019EFESSWEGlshuey23' : '2019EFESSWEGlshuey22',
            '2019SFGEEWEGjkolodjashnij10' : '2019SFGEEWEGjkolodjashnij11',
            '2019SFGEEWEGrstanley7' : '2019SFGEEWEGrstanley6'
            }[fullkey]
    except KeyError:
        return fullkey

    
def getMatchID(df):
    hcode = getTeamCode(df['hometeam'])
    acode = getTeamCode(df['awayteam'])
    codes = [hcode,acode]
    codes.sort()
    
    if((df["date"] == "2-Oct-2010") or \
       (df["date"] == "9-Oct-1948") or \
       (df["date"] == "1-Oct-1977")):
        tround = getRoundCode("GReplay")
    elif(df["date"] == "22-Sep-1962") :
        tround = str(getRoundCode("PReplay"))
    elif((df["date"] == "23-Sep-1972") or \
         (df["date"] == "22-Sep-1928") or \
         (df["date"] == "21-Sep-1946")):
        tround = str(getRoundCode("SReplay"))
    elif(df["date"] == "15-Sep-1990") :
        tround = str(getRoundCode("QReplay"))
    else:
        tround = str(getRoundCode(df["round"]))
    
    return (str(df["year"]) + tround + \
            codes[0] + codes[1])
    
def nameFormat(df,col):
    if(df[col] == "Western Bulldogs"):
        return "Footscray"
    elif(df[col] == "Kangaroos"):
        return "North Melbourne"
    elif(df[col] == "Brisbane"):
        return "Brisbane Lions"
    elif(df[col] == "GWS"):
        return "Greater Western Sydney"
    else:
        return df[col]
        
def replayFix(df):    
    if((df["date"] == "2-Oct-2010") or \
       (df["date"] == "9-Oct-1948") or \
       (df["date"] == "1-Oct-1977")):
        newstring = str(df["matchid"]).replace("GF","GR",1)    
    elif(df["date"] == "22-Sep-1962") :
        newstring = str(df["matchid"]).replace("PF","PR",1)    
    elif((df["date"] == "23-Sep-1972") or \
         (df["date"] == "22-Sep-1928") or \
         (df["date"] == "21-Sep-1946")):
        newstring = str(df["matchid"]).replace("SF","SR",1)    
    elif(df["date"] == "15-Sep-1990") :
        newstring = str(df["matchid"]).replace("QF","QR",1)    
    else:
        return df["matchid"]    
    return newstring

def roundFix(df):    
    if((df["date"] == "2-Oct-2010") or \
       (df["date"] == "9-Oct-1948") or \
       (df["date"] == "1-Oct-1977")):
        return "GReplay"
    elif((df["date"] == "23-Sep-1972") or \
         (df["date"] == "22-Sep-1928") or \
         (df["date"] == "21-Sep-1946")):
        return "SReplay"
    elif(df["date"] == "22-Sep-1962") :
        return "PReplay"
    elif(df["date"] == "15-Sep-1990") :
        return "QReplay"
    else:
        return df["round"]
    

def getPlayerMatchID(df):
    playerID = str(df["name"]).replace(" ","_")
    
    
    if(numpy.isnan(df["addcode"])):
        return str(playerID) + str(df["matchid"])
    else:
        return str(playerID) + str(df["matchid"]) + str(+ df["addcode"])
    


#Generate a three character 'teamcode' for each team
def getTeamCode(team):
    return {
           'Adelaide' : 'ADE',
           'Brisbane Bears' : 'BBL',
           'Brisbane Lions' : 'BRS',
           'Carlton' : 'CAR',
           'Collingwood' : 'COL',
           'Essendon' : 'ESS',
           'Fitzroy' : 'FIT',
           'Footscray' : 'FOT',
           'Fremantle' : 'FRE',
           'Geelong' : 'GEE',
           'Gold Coast' : 'GCS',
           'Greater Western Sydney' : 'GWS',
           'Hawthorn' : 'HAW',
           'Melbourne' : 'MEL',
           'North Melbourne' : 'NOR',
           'Port Adelaide' : 'POR',
           'Richmond' : 'RCH',
           'South Melbourne' : 'SMS',
           'St Kilda' : 'STK',
           'Sydney' : 'SYD',
           'University' : 'UNI',
           'West Coast' : 'WEG'
           }[team]

def fixFinalsRounds(df):
    if(df["round"] != "Final"):
        return df["round"]
    else:
        gid = df["gameID"]
        
        try:
            return {
                9927 : 'Grand',
                9925 : 'Preliminary',
                9926 : 'Preliminary',
                9923 : 'Semi',
                9924 : 'Semi',
                9919 : 'Elimination',
                9921 : 'Elimination',
                9920 : 'Qualifying',
                9922 : 'Qualifying',    
                9720 : 'Grand',
                9719 : 'Preliminary',
                9718 : 'Preliminary',
                9717 : 'Semi',
                9716 : 'Semi',
                9713 : 'Elimination',
                9714 : 'Elimination',
                9715 : 'Qualifying',
                9712 : 'Qualifying',
                9513 : 'Grand',
                9512 : 'Preliminary',
                9511 : 'Preliminary',
                9510 : 'Semi',
                9509 : 'Semi',
                9508 : 'Elimination',
                9507 : 'Elimination',
                9506 : 'Qualifying',
                9505 : 'Qualifying',
                9306 : 'Grand',
                9305 : 'Preliminary',
                9304 : 'Preliminary',
                9303 : 'Semi',
                9302 : 'Semi',
                9301 : 'Elimination',
                9300 : 'Qualifying',
                9299 : 'Qualifying',
                9298 : 'Elimination',
                6171 : 'Grand',
                6170 : 'Preliminary',
                6169 : 'Preliminary',
                6168 : 'Semi',
                6167 : 'Semi',
                6166 : 'Elimination',
                6165 : 'Elimination',
                6164 : 'Qualifying',
                6163 : 'Qualifying',
                5963 : 'Grand',
                5962 : 'Preliminary',
                5961 : 'Preliminary',
                5960 : 'Semi',
                5959 : 'Semi',
                5958 : 'Elimination',
                5957 : 'Elimination',
                5956 : 'Qualifying',
                5955 : 'Qualifying',
                5756 : 'Grand',
                5755 : 'Preliminary',
                5754 : 'Preliminary',
                5753 : 'Semi',
                5752 : 'Semi',
                5751 : 'Elimination',
                5750 : 'Elimination',
                5749 : 'Qualifying',
                5748 : 'Qualifying',
                5549 : 'Grand',
                5548 : 'Preliminary',
                5547 : 'Preliminary',
                5546 : 'Semi',
                5545 : 'Semi',
                5544 : 'Elimination',
                5543 : 'Elimination',
                5542 : 'Qualifying',
                5541 : 'Qualifying',
                5342 : 'Grand',
                5341 : 'Preliminary',
                5340 : 'Preliminary',
                5339 : 'Semi',
                5338 : 'Semi',
                5337 : 'Elimination',
                5336 : 'Elimination',
                5335 : 'Qualifying',
                5334 : 'Qualifying',
                5146 : 'GReplay',
                5145 : 'Grand',
                5144 : 'Preliminary',
                5143 : 'Preliminary',
                5142 : 'Semi',
                5141 : 'Semi',
                5140 : 'Elimination',
                5139 : 'Qualifying',
                5138 : 'Elimination',
                5137 : 'Qualifying'
                }[gid]
        except KeyError:
            print("Error for round: " + str(round))
        
    

#Turns each round into two characters
def getRoundCode(round):

    r = str(round)

    try:
        return {
                '1' : '01',
                '2' : '02',
                '3' : '03',
                '4' : '04',
                '5' : '05',
                '6' : '06',
                '7' : '07',
                '8' : '08',
                '9' : '09',
                '10' : '10',
                '11' : '11',
                '12' : '12',
                '13' : '13',
                '14' : '14',
                '15' : '15',
                '16' : '16',
                '17' : '17',
                '18' : '18',
                '19' : '19',
                '20' : '20',
                '21' : '21',
                '22' : '22',
                '23' : '23',
                '24' : '24',
                'Elimination' : 'EF',
                'Qualifying' : 'QF',
                'Semi' : 'SF',
                'Preliminary' : 'PF',
                'Grand' : 'GF',
                'QReplay' : 'QR',
                'SReplay' : 'SR',
                'PReplay' : 'PR',                
                'GReplay' : 'GR'

                }[r]

    except KeyError:
        print("Error for round: " + str(round))

def getMatchIndex(m,date):
    cells=list()
    for cell in m.findAll("td"):
        cells.append(cell.text)

    
    matchstring = str(cells[1]).split(" ")
    


    #If match is a final, remove 'FINAL' cell so that it aligns with
    #Round numbers
    if(str(matchstring[2]) == "Final"):
        del matchstring[2]


    #Create blank row to be filled

    theround = matchstring[1] #round


    if(len(matchstring) == 14): #Venue name two words
        year = str(matchstring[7].split("-")[2])
    elif(len(matchstring) == 13): #Venue name one word
        year = str(matchstring[6].split("-")[2])
    elif(len(matchstring) == 12): #Venue name two words, no crowd
        year = str(matchstring[7].split("-")[2])
    elif(len(matchstring) == 11): #Venue name one word, no crowd
        year = str(matchstring[6].split("-")[2])
    elif(len(matchstring) == 10): #Venue name two words, no venue or timezeone
        year = str(matchstring[7].split("-")[2])
    elif(len(matchstring) == 9): #Venue name one word, no venue or timezeone
        year = str(matchstring[6].split("-")[2])
    else:
        print ("Error with file:" + str(cells[1]) + "   " + str(len(matchstring)))


    #Process teams and quarter by quarter scores for non overtime games
    if(len(cells)==25): #Game finishing in regular time
        hteam = cells[3]    #hteam
        ateam = cells[8]   #ateam
    elif(len(cells)==29): #Game finishing in overtime
        hteam = cells[3]    #hteam
        ateam = cells[9]   #ateam
    elif(len(cells)==23): #Game finishing in overtime
        hteam = cells[3]    #hteam
        ateam = cells[8]   #ateam


    hcode = getTeamCode(replaceTeam(hteam))
    acode = getTeamCode(replaceTeam(ateam))
    
    codes = [hcode,acode]
    codes.sort()

    if((date == "2-Oct-2010") or \
        (date == "9-Oct-1948") or \
        (date == "1-Oct-1977")):
        rcode = getRoundCode("GReplay")
    elif(date == "22-Sep-1962") :
        rcode = getRoundCode("PReplay")
    elif((date == "23-Sep-1972") or \
         (date == "22-Sep-1928") or \
         (date == "21-Sep-1946")):        
        rcode = getRoundCode("SReplay")
    elif(date == "15-Sep-1990") :
        rcode = getRoundCode("QReplay") 
    else:
        rcode = getRoundCode(theround)

    return (str(year) + str(rcode) + codes[0] + codes[1])

def cleanNumber(df):
    if(len(str(df["number"])) > 2):
        return df["number"][:2]
    else:
        return df["number"]

#checks if a player was subbed on or off an creates a column for it
def checkSub(df):
    if(len(str(df["number"])) > 2):
        if("↓" in str(df["number"])):
            return "off"
        elif("↑" in str(df["number"])):
            return "on"
        else:
            return ""
    else:
        return ""
    
def changeDate(date):
    dstring = date.split(' ')
    newdate = str(dstring[1].strip('stndrh') + " " + dstring[2] + " " + dstring[3])
    return newdate

def convertStats(file,content):
    f = pd.read_csv(file, index_col = 0)
    m=[]
    if(content == "Match"):
         for index, row in f.iterrows():
             m.append({'gameID':row["gameID"],'ha':"Home", 'team':row["hometeam"], 'kicks':row["homekicks"],
                    'hb':row["homehb"], 'disp':row["homedisp"], 'marks':row["homemarks"], 
                    'tackles':row["hometackles"], 'hitouts':row["homehitout"], 'ff':row["homeff"],
                    'fa':row["homeff"], 'goals':row["homeg"], 'behinds':row["homebk"], 'score':(row["homeg"] * 6) + row["homebk"], 
                    'margin':(row["homeg"] * 6) + row["homebk"] - ((row["awayg"] * 6) + row["awaybk"]),'rushed':row["homerush"], 'i50':row["homei50"]})
    
             m.append({'gameID':row["gameID"], 'ha':"Away",'team':row["awayteam"], 'kicks':row["awaykicks"],
                    'hb':row["awayhb"], 'disp':row["awaydisp"], 'marks':row["awaymarks"], 
                    'tackles':row["awaytackles"], 'hitouts':row["awayhitout"], 'ff':row["awayff"],
                    'fa':row["awayff"], 'goals':row["awayg"], 'behinds':row["awaybk"], 'score':(row["awayg"] * 6) + row["awaybk"], 
                    'margin':(row["awayg"] * 6) + row["awaybk"] - ((row["homeg"] * 6) + row["homebk"]), 'rushed':row["awayrush"], 'i50':row["awayi50"]})
    return pd.DataFrame.from_dict(m)


def getYear(df):
#<<<<<<< HEAD
    #date = df["date"].split("/")
    #return "20" + date[2]
    return pd.to_datetime(df["date"]).year
    #return df["date"].year
#=======
#    date = df["date"].split("/")
#    return "20" + date[2]
#>>>>>>> 11cc48be996f73df4ac9a8dc6b7353238b68eb85

def getNameKeyFW(df):
    namesplit = df["fullname"].split(" ")
    one = namesplit[0][0]
    
    if("." in namesplit[1]):
        two = namesplit[2]
    else:
        two = namesplit[1]
        
    try:
        d = int(df["kicks"])
    except ValueError:
        d = 0
    
    three = str(d)
    return str(one + two + three).lower()

def getNameKeyAT(df):
    one = df["first_name"][1]
    two = df["last_name"].split(" ")[0]
    
    try:
        d = int(df["kicks"])
    except ValueError:
        d = 0
    
    three = str(d)
    return str(one + two + three).lower()

def getFullKey(df):
    return df["matchid"] + df["namekey"]

def fillYear(df):
    yearstring = df["matchid"][:4]
    return int(yearstring)

def nameClean(df):
    return {
            'Gary Jnr Ablett': 'Gary Ablett',
            'G Ablett': 'Gary Ablett',
            'Darcy BJones' : 'Darcy ByrneJones',
            'Josh DCardillo' : 'Josh Deluca',
            'Trent DLane' : 'Trent DennisLane',
            'Cameron EYolmen' : 'Cam EllisYolmen',
            'Michael S Gardiner' : 'Michael Gardiner',
            'George HSmith' : 'George HorlinSmith',
            'Will HElliott' : 'Will HoskinElliott',
            'Jarrod KThomson' : 'Jarrod KaylerThomson',
            'Josh P Kennedy' : 'Josh Kennedy',
            'J Kennedy' : 'Josh Kennedy',
            'Josh P. Kennedy' : 'Josh Kennedy',
            'Jay KHarris' : 'Jay Kennedy',
            'Nathan LMurray' : 'Nathan LovettMurray',
            'Anthony MTipungwuti' : 'Anthony McDonaldTipungwuti',
            'Alex NBullen' : 'Alex NealBullen',
            'Sam PSeton' : 'Sam PetrevskiSeton',
            'Sam PPepper' : 'Sam PowellPepper',
            'Lewis RThomson' : 'Lewis RobertsThomson',
            'Ed VWillis' : 'Ed VickersWillis',
            'Luke DUniacke' : 'Luke DaviesUniacke',
            'Brandon ZThatcher' : 'Brandon ZerkThatcher',
            'Derek ESmith' : 'Derek EggmolesseSmith',
            'Ian Hill' : 'Bobby Hill',            
            'Callum CJones' : 'Callum ColemanJones',      

            }.get(df["name"],df["name"])
    
            #return NAMESWAP.get(df.loc[])
            #str(df["fullname"])

def shortName(df):
    fullname = df["name"]
    
    initial = fullname.split(" ")[0]
    rest = fullname.split(" ")[-1]
    
    return initial[0] + " " + rest

                          