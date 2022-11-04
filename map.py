import random
import os
import numpy as np
from PIL import Image
import pygame
import sys
from pygame.locals import *

players=1
bots=3
hirelingsEnabled=False
bannedFactions=[]
forcedFactions=[]
forcedBots=[]
bannedHirelings=[]
bannedVagabonds=[]
bannedLandmarks=[]
minLandmarks=0
maxLandmarks=2
landmarkWeight=0.1
landmarkVariance=0.557
vagabond2Depriority=0.5 #[0,1] and higher means less likely
baseDeckChance=0.1
balancedSuits=False
forcedMaps=[] #leave as empty if no forced map
imageSize=1.2

mapData = {
    "fall": {
        1:  { "slots": 1, "adjacent": [5,9,10],       "corner": True,  "edge": True,  "river": False, "ruins": False, "position": (18, 18), "opposite":3,},
        2:  { "slots": 2, "adjacent": [5,6,10],       "corner": True,  "edge": True,  "river": False, "ruins": False, "position": (358, 89), "opposite":4,},
        3:  { "slots": 1, "adjacent": [6,7,11],       "corner": True,  "edge": True,  "river": False, "ruins": False, "position": (362, 367), "opposite":1,},
        4:  { "slots": 1, "adjacent": [8,9,12],       "corner": True,  "edge": True,  "river": True,  "ruins": False, "position": (15, 320), "opposite":2,},
        5:  { "slots": 2, "adjacent": [1,2],          "corner": False, "edge": True,  "river": True,  "ruins": False, "position": (233, 23), "opposite":"",},
        6:  { "slots": 2, "adjacent": [2,3,11],       "corner": False, "edge": True,  "river": False, "ruins": True,  "position": (368, 206), "opposite":"",},
        7:  { "slots": 2, "adjacent": [3,8,12],       "corner": False, "edge": True,  "river": True,  "ruins": False, "position": (248, 318), "opposite":"",},
        8:  { "slots": 2, "adjacent": [4,7],          "corner": False, "edge": True,  "river": False, "ruins": False, "position": (140, 364), "opposite":"",},
        9:  { "slots": 2, "adjacent": [1,4,12],       "corner": False, "edge": True,  "river": False, "ruins": False, "position": (18, 134), "opposite":"",},
        10: { "slots": 2, "adjacent": [1,2,12],       "corner": False, "edge": False, "river": True,  "ruins": True,  "position": (157, 87), "opposite":"",},
        11: { "slots": 3, "adjacent": [3,6,12],       "corner": False, "edge": False, "river": True,  "ruins": True,  "position": (264, 192), "opposite":"",},
        12: { "slots": 2, "adjacent": [4,7,8,9,11],   "corner": False, "edge": False, "river": False, "ruins": True,  "position": (124, 227), "opposite":"",},
        "paths": {
            1:  {"position":(160,40)},
            2:  {"position":(27,95)},
            3:  {"position":(107,87)},
            4:  {"position":(320,76)},
            5:  {"position":(383,170)},
            6:  {"position":(280,114)},
            7:  {"position":(405,310)},
            8:  {"position":(330,365)},
            9:  {"position":(335,300)},
            10:  {"position":(100,365)},
            11:  {"position":(20,240)},
            12:  {"position":(90,295)},
            13:  {"position":(340,220)},
            14:  {"position":(220,367)},
            15:  {"position":(200,295)},
            16:  {"position":(90,195)},
            17:  {"position":(175,180)},
            18:  {"position":(215,230)},
        },
        "forests":{
            1:  {"position":(125,60), 'adjacent':[1,2,5,10],},
            2:  {"position":(100,130), 'adjacent':[1,9,10,12],},
            3:  {"position":(245,150), 'adjacent':[2,6,10,11,12],},
            4:  {"position":(60,230), 'adjacent':[4,9,12],},
            5:  {"position":(140,315), 'adjacent':[4,7,8,12],},
            6:  {"position":(245,270), 'adjacent':[3,7,11,12],},
            7:  {"position":(360,280), 'adjacent':[3,6,11],},
        },
    },
    "winter": {
        1:  { "slots": 1, "adjacent": [5,10,11],      "corner": True,  "edge": True,  "river": False, "ruins": False, "position": (18, 10), "opposite":3,},
        2:  { "slots": 1, "adjacent": [6,7,12],       "corner": True,  "edge": True,  "river": False, "ruins": False, "position": (363, 7), "opposite":4,},
        3:  { "slots": 2, "adjacent": [7,8,12],       "corner": True,  "edge": True,  "river": False, "ruins": False, "position": (363, 336), "opposite":1,},
        4:  { "slots": 2, "adjacent": [9,10,11],      "corner": True,  "edge": True,  "river": False, "ruins": False, "position": (21, 301), "opposite":2,},
        5:  { "slots": 2, "adjacent": [1,6],          "corner": False, "edge": True,  "river": False, "ruins": False, "position": (137, 18), "opposite":"",},
        6:  { "slots": 2, "adjacent": [2,5],          "corner": False, "edge": True,  "river": False, "ruins": False, "position": (243, 38), "opposite":"",},
        7:  { "slots": 1, "adjacent": [2,3],          "corner": False, "edge": True,  "river": True,  "ruins": False, "position": (367, 180), "opposite":"",},
        8:  { "slots": 2, "adjacent": [3,9,12],       "corner": False, "edge": True,  "river": False, "ruins": True,  "position": (251, 294), "opposite":"",},
        9:  { "slots": 2, "adjacent": [4,8,11],       "corner": False, "edge": True,  "river": False, "ruins": True,  "position": (144, 340), "opposite":"",},
        10: { "slots": 1, "adjacent": [1,4],          "corner": False, "edge": True,  "river": True,  "ruins": False, "position": (12, 159), "opposite":"",},
        11: { "slots": 3, "adjacent": [1,4,9],        "corner": False, "edge": False, "river": True,  "ruins": True,  "position": (145, 164), "opposite":"",},
        12: { "slots": 3, "adjacent": [2,3,8],        "corner": False, "edge": False, "river": True,  "ruins": True,  "position": (262, 170), "opposite":"",},
        "paths": {
            1:  {"position":(98,40)},
            2:  {"position":(33,106)},
            3:  {"position":(102,103)},
            4:  {"position":(322,42)},
            5:  {"position":(391,115)},
            6:  {"position":(332,111)},
            7:  {"position":(394,272)},
            8:  {"position":(325,336)},
            9:  {"position":(327,271)},
            10:  {"position":(105,346)},
            11:  {"position":(36,248)},
            12:  {"position":(98,261)},
            13:  {"position":(212,45)},
            14:  {"position":(222,344)},
            15:  {"position":(279,257)},
            16:  {"position":(170,272)},
        },
        "forests":{
            1:  {"position":(74,134), 'adjacent':[1,10,11],},
            2:  {"position":(214,123), 'adjacent':[1,2,5,6,11,12],},
            3:  {"position":(359,137), 'adjacent':[2,7,12],},
            4:  {"position":(80,224), 'adjacent':[4,10,11],},
            5:  {"position":(127,290), 'adjacent':[4,9,11],},
            6:  {"position":(216,253), 'adjacent':[8,9,11,12],},
            7:  {"position":(303,276), 'adjacent':[3,8,12],},
            8:  {"position":(346,240), 'adjacent':[3,7,12],},
        },
    },
    "lake": {
        1:  { "slots": 2, "adjacent": [5,9],          "corner": True,   "edge": True,  "river": True,  "ruins": False, "position": (353, 319), "opposite":2,},
        2:  { "slots": 1, "adjacent": [7,8,10],       "corner": True,   "edge": True,  "river": False, "ruins": False, "position": (24, 10), "opposite":1,},
        3:  { "slots": 1, "adjacent": [8,9,12],       "corner": True,   "edge": True,  "river": False, "ruins": False, "position": (25, 307), "opposite":4,},
        4:  { "slots": 1, "adjacent": [5,6],          "corner": True,   "edge": True,  "river": False, "ruins": False, "position": (366, 7), "opposite":3,},
        5:  { "slots": 3, "adjacent": [1,4,11],       "corner": False,  "edge": True,  "river": False, "ruins": True,  "position": (370, 181), "opposite":"",},
        6:  { "slots": 2, "adjacent": [4,7,11],       "corner": False,  "edge": True,  "river": False, "ruins": False, "position": (267, 39), "opposite":"",},
        7:  { "slots": 1, "adjacent": [2,6,10,11],    "corner": False,  "edge": True,  "river": False, "ruins": False, "position": (163, 19), "opposite":"",},
        8:  { "slots": 1, "adjacent": [2,3,10],       "corner": False,  "edge": True,  "river": False, "ruins": False, "position": (16, 161), "opposite":"",},
        9:  { "slots": 1, "adjacent": [1,3,12],       "corner": False,  "edge": True,  "river": False, "ruins": False, "position": (230, 342), "opposite":"",},
        10: { "slots": 3, "adjacent": [2,7,8],        "corner": False,  "edge": False, "river": True,  "ruins": True,  "position": (135, 136), "opposite":"",},
        11: { "slots": 3, "adjacent": [5,6,7],        "corner": False,  "edge": False, "river": True,  "ruins": True,  "position": (267, 171), "opposite":"",},
        12: { "slots": 3, "adjacent": [3,9],          "corner": False,  "edge": False, "river": True,  "ruins": True,  "position": (152, 260), "opposite":"",},
        "paths": {
            1:  {"position":(388,267)},
            2:  {"position":(313,352)},
            3:  {"position":(114,32)},
            4:  {"position":(39,108)},
            5:  {"position":(101,91)},
            6:  {"position":(39,257)},
            7:  {"position":(149,349)},
            8:  {"position":(109,292)},
            9:  {"position":(396,119)},
            10:  {"position":(338,42)},
            11:  {"position":(340,196)},
            12:  {"position":(236,49)},
            13:  {"position":(168,100)},
            14:  {"position":(91,171)},
            15:  {"position":(217,320)},
            16:  {"position":(295,129)},
            17:  {"position":(227,124)},
        },
        "forests":{
            1:  {"position":(80,122), 'adjacent':[2,8,10],},
            2:  {"position":(125,70), 'adjacent':[2,7,10],},
            3:  {"position":(216,156), 'adjacent':[7,10,11],},
            4:  {"position":(253,105), 'adjacent':[6,7,11],},
            5:  {"position":(347,115), 'adjacent':[4,5,6,11],},
            6:  {"position":(349,239), 'adjacent':[1,5,11],},
            7:  {"position":(263,305), 'adjacent':[1,9,12],},
            8:  {"position":(124,324), 'adjacent':[3,9,12],},
            9:  {"position":(95,238), 'adjacent':[3,8,10,12],},
        },
    },
    "mountain": {
        1:  { "slots": 2, "adjacent": [8,9],          "corner": True,   "edge": True,  "river": False, "ruins": False, "position": (22, 15), "opposite":3, "closedAdjacent":[],},
        2:  { "slots": 2, "adjacent": [6,11],         "corner": True,   "edge": True,  "river": True,  "ruins": False, "position": (362, 16), "opposite":4, "closedAdjacent":[5],},
        3:  { "slots": 2, "adjacent": [6,11],         "corner": True,   "edge": True,  "river": False, "ruins": False, "position": (364, 350), "opposite":1, "closedAdjacent":[7],},
        4:  { "slots": 2, "adjacent": [8,12],         "corner": True,   "edge": True,  "river": True,  "ruins": False, "position": (26, 310), "opposite":2, "closedAdjacent":[],},
        5:  { "slots": 1, "adjacent": [10,11],        "corner": False,  "edge": True,  "river": False, "ruins": False, "position": (227, 26), "opposite":"", "closedAdjacent":[2,9],},
        6:  { "slots": 1, "adjacent": [2,3],          "corner": False,  "edge": True,  "river": False, "ruins": False, "position": (367, 191), "opposite":"", "closedAdjacent":[11],},
        7:  { "slots": 1, "adjacent": [12],           "corner": False,  "edge": True,  "river": False, "ruins": False, "position": (189, 348), "opposite":"", "closedAdjacent":[3],},
        8:  { "slots": 1, "adjacent": [1,4],          "corner": False,  "edge": True,  "river": False, "ruins": False, "position": (16, 165), "opposite":"", "closedAdjacent":[9],},
        9:  { "slots": 3, "adjacent": [1,10,12],      "corner": False,  "edge": True,  "river": False, "ruins": True,  "position": (117, 126), "opposite":"", "closedAdjacent":[5,8],},
        10: { "slots": 2, "adjacent": [5,9,11,12],    "corner": False,  "edge": False, "river": True,  "ruins": True,  "position": (204, 143), "opposite":"", "closedAdjacent":[],},
        11: { "slots": 3, "adjacent": [2,3,5,10],     "corner": False,  "edge": False, "river": False, "ruins": True,  "position": (253, 232), "opposite":"", "closedAdjacent":[6,12],},
        12: { "slots": 3, "adjacent": [4,7,9,10],     "corner": False,  "edge": True,  "river": False, "ruins": True,  "position": (124, 228), "opposite":"", "closedAdjacent":[11],},
        "paths": {
            1:  {"position":(39,108)},
            2:  {"position":(92,90)},
            3:  {"position":(389,122)},
            4:  {"position":(328,138)},
            5:  {"position":(392,289)},
            6:  {"position":(334,308)},
            7:  {"position":(37,259)},
            8:  {"position":(94,286)},
            9:  {"position":(234,103)},
            10:  {"position":(272,150)},
            11:  {"position":(179,308)},
            12:  {"position":(183,152)},
            13:  {"position":(142,198)},
            14:  {"position":(250,208)},
            15:  {"position":(189,209)},
        },
        "forests":{
            1:  {"position":(74,122), 'adjacent':[1,8,9],},
            2:  {"position":(202,113), 'adjacent':[5,9,10],},
            3:  {"position":(172,189), 'adjacent':[9,10,12],},
            4:  {"position":(248,113), 'adjacent':[5,10,11],},
            5:  {"position":(305,106), 'adjacent':[2,5,11],},
            6:  {"position":(350,154), 'adjacent':[2,6,11],},
            7:  {"position":(357,279), 'adjacent':[3,6,11],},
            8:  {"position":(270,313), 'adjacent':[3,7,11,12],},
            9:  {"position":(218,223), 'adjacent':[10,11,12],},
            10:  {"position":(82,237), 'adjacent':[4,8,9,12],},
        },
    },
}
factionData={
    "marquise": {
        "militant": True,
        "insurgent": False,
        "hireling" : "patrol",
    },
    "eyrie": {
        "militant": True,
        "insurgent": False,
        "hireling" : "dynasty",
    },
    "woodland": {
        "militant": False,
        "insurgent": True,
        "hireling" : "uprising",
    },
    "vagabond": {
        "militant": False,
        "insurgent": True,
        "hireling" : "exile",
    },
    "vagabond2": {
        "militant": False,
        "insurgent": True,
        "hireling" : "exile",
    },
    "cult": {
        "militant": False,
        "insurgent": True,
        "hireling" : "prophets",
    },
    "riverfolk": {
        "militant": False,
        "insurgent": True,
        "hireling" : "flotilla",
    },
    "duchy": {
        "militant": True,
        "insurgent": False,
        "hireling" : "expedition",
    },
    "corvid": {
        "militant": False,
        "insurgent": True,
        "hireling": "spies",
    },    
    "warlord": {
        "militant": True,
        "insurgent": False,
        "hireling" : "flamebearers",
    },
    "keepers": {
        "militant": True,
        "insurgent": False,
        "hireling" : "vaultkeepers",
    },
}
hirelingData={
    "band":{
        "faction":"",
    },
    "bandits":{
        "faction":"",
    },
    "dynasty":{
        "faction":"eyrie",
    },
    "exile":{
        "faction":"vagabond",
    },
    "expedition":{
        "faction":"duchy",
    },
    "flamebearers":{
        "faction":"warlord",
    },
    "flotilla":{
        "faction":"riverfolk",
    },
    "patrol":{
        "faction":"marquise",
    },
    "prophets":{
        "faction":"cult",
    },
    "protector":{
        "faction":"",
    },
    "spies":{
        "faction":"corvid",
    },
    "uprising":{
        "faction":"woodland",
    },
    "vaultkeepers":{
        "faction":"keepers",
    },  
}
def setMap():
    maps=["fall","winter","lake","mountain"]
    if len(forcedMaps)>0:
        maps = [i for i in maps if i in forcedMaps]
    map = random.choice(maps)
    image = Image.open('assets/map-'+ str(map) +'.png')
    image2=image.resize((int(450),int(450/image.width*image.height)))
    image2.filename=image.filename
    return image2

def getName(image):
    return image.filename[11:-4]

def placeSuit(image,suit,num):
    imgSuit=Image.open('assets/clearing-'+ str(suit) +'.png')
    imgSuit=imgSuit.resize((75,75))
    image.paste(imgSuit,mapData[getName(image)][num]["position"],mask=imgSuit)
    mapData[getName(image)][num]["suit"] = [suit]

def setSuits(image):
    suits=['rabbit', 'rabbit', 'rabbit', 'rabbit', 'fox', 'fox', 'fox', 'fox', 'mouse', 'mouse', 'mouse', 'mouse']
    random.shuffle(suits)
    if balancedSuits:
        balanced = True
        a=0
        while balanced:
            random.shuffle(suits)
            balanced=False
            """if a%10000==0:
                print(suits)"""
            for i,suit in enumerate(suits):
                adjacent=mapData[getName(image)][i+1]["adjacent"]
                if getName(image)=="mountain":
                    adjacent=adjacent+mapData[getName(image)][i+1]["closedAdjacent"]
                if len([j for j in adjacent if suits[j-1]==suit])>0:
                    balanced=True 
            a+=1
    for i, suit in enumerate(suits):
        placeSuit(image,suit,i+1)

def getLocation(image,landmark,used):
    name=getName(image)
    clearing = random.randint(1,12)
    r=random.random()
    if name == "mountain" and r<0.2:
        clearing=10
    works=True
    clearingData=mapData[name][clearing]
    if clearing in used:
        works = False
    if landmark != "tower" and bool(set(clearingData["adjacent"]) & set(used.keys())):
        works = False
    if landmark == "tower" and not (clearingData["ruins"]):
        works = False
    elif landmark == "market" and not (clearingData["slots"]==1 and not clearingData["ruins"]):
        works = False
    elif landmark == "city" and not (clearingData["river"]):
        works = False
    elif landmark == "ferry" and not (clearingData["river"]):
        works = False
    #elif landmark == "treetop" and not (mapData[name][clearing]["corner"]):
    #elif landmark == "treetop" and not (not clearingData["corner"] and not any([i for i in clearingData["adjacent"] if mapData[name][i]["corner"]])):
    elif landmark == "treetop" and not (not clearingData["corner"] and len(clearingData["adjacent"])>2):
        works = False
    return clearing,works

def placeLandmark(image,landmark,clearing):
    imgLand=Image.open('assets/landmark-'+ str(landmark) +'.png')
    size=(int(imgLand.width/15),int(imgLand.height/15))
    imgLand=imgLand.resize(size)
    position=tuple(x+45 for x in mapData[getName(image)][clearing]["position"])
    image.paste(imgLand,position,mask=imgLand)
    if landmark == "treetop":
        mapData[getName(image)][clearing]["slots"]+=1
    if landmark == "city":
        mapData[getName(image)][clearing]["suit"] = mapData[getName(image)][clearing]["suit"] + list(set(["rabbit","fox","mouse"]) - set(mapData[getName(image)][clearing]["suit"]))

def setLandmarks(image,skip):
    specificLandmark=random.random()
    used=setLandmark(image)
    while ((specificLandmark<0.40 and "ferry" not in list(used.values()) and getName(image)=="lake")):
        used=setLandmark(image)
    while ((specificLandmark<0.40 and "tower" not in list(used.values()) and getName(image)=="mountain")):
        used=setLandmark(image)
    if not skip:
        for clearing in used:
            placeLandmark(image,used[clearing],clearing)
    return used

def setLandmark(image):
    landmarks = ["tower","market","city","ferry","treetop","forge"]
    landmarks = [i for i in landmarks if i not in bannedLandmarks]
    mean=(maxLandmarks+minLandmarks)/2
    numLandmarks = round(max(minLandmarks, min(np.random.normal(mean+landmarkWeight,mean*landmarkVariance), maxLandmarks)))
    running = True
    used={}
    while running:
        used={}
        running = False
        random.shuffle(landmarks)
        for i in range(numLandmarks):
            landmark=landmarks[i]
            clearing,works=getLocation(image,landmarks[i],used)
            used[clearing]=landmark
            if not works:
                running=True
    return used
def pickLargest(l):
    n=-1000000
    result=[]
    for i,element in enumerate(l):
        if element == n:
            result.append(i)
        elif element>n:
            result=[i]
            n=element
    return random.choice(result)
def botsList():
    factionOptions=list(factionData.keys())
    factionOptions.remove("vagabond2")
    factionOptions.remove("keepers")
    factionOptions.remove("warlord")
    factionOptions = [i for i in factionOptions if i not in bannedFactions]
    return random.sample(factionOptions,bots)
def setBots(image):
    botList=[]
    b=0
    while True:
        botList=botsList()
        if all(elem in botList for elem in forcedBots):
            break
        elif b>999:
            print("Could not find set of bots given forced and banned options.")
            break
        b+=1
    botList=sorted(botList,key=list(factionData.keys()).index)
    for bot in botList:
        bannedFactions.append(bot)
        bannedHirelings.append(factionData[bot]["hireling"])
    taken=[]
    used=[]
    for faction in botList:
        if faction == "marquise":
            buildings=["piece-recruiter","piece-workshop","piece-sawmill"]
            clearing=random.choice([i for i in range(1, 13) if mapData[getName(image)][i]["corner"]])
            taken.append(clearing)
            clearings=list(range(1,13))
            clearings.remove(mapData[getName(image)][clearing]["opposite"])    
            for i in clearings:
                drawHirelingPiece(image,["faction-marquise"],used,i)
            adjacent=mapData[getName(image)][clearing]["adjacent"]
            if len(adjacent)<3:
                adjacent.extend([clearing for i in range(3-len(adjacent))])
            adjacent=random.sample(adjacent,3)
            drawHirelingPiece(image,["faction-marquise","piece-keep"],used,clearing)
            for i in range(len(buildings)):
                drawHirelingPiece(image,[buildings[i]],used,adjacent[i])
        if faction == "eyrie":
            if len(taken)==1:
                clearing=mapData[getName(image)][taken[0]]["opposite"]
            else:
                clearing=random.choice([i for i in range(1, 13) if mapData[getName(image)][i]["corner"] and i not in taken])
            taken.append(clearing)
            drawHirelingPiece(image,["faction-eyrie","faction-eyrie","faction-eyrie","faction-eyrie","faction-eyrie","faction-eyrie","piece-roost",],used,clearing)
        if faction == "woodland":
            
            drawObject(image,(0,image.height-400),["faction-woodland"])
        if faction == "vagabond":
            forestSizes = [len(mapData[getName(image)]["forests"][i]["adjacent"]) for i in mapData[getName(image)]["forests"]]
            clearing=pickLargest(forestSizes)+1-12
            drawHirelingPiece(image,["faction-vagabond2"],used,clearing)
        if faction == "cult":
            if len(taken)==1:
                clearing=mapData[getName(image)][taken[0]]["opposite"]
            else:
                clearing=random.choice([i for i in range(1, 13) if mapData[getName(image)][i]["corner"] and i not in taken])
            taken.append(clearing)
            drawHirelingPiece(image,["faction-cult","faction-cult","faction-cult","faction-cult","piece-garden"+mapData[getName(image)][clearing]["suit"][0]],used,clearing)
            for i in mapData[getName(image)][clearing]["adjacent"]:
                drawHirelingPiece(image,["faction-cult"],used,i)
        if faction == "riverfolk":
            rivers=[i for i in range(1, 13) if mapData[getName(image)][i]["river"]]
            for river in rivers:
               drawHirelingPiece(image,["faction-riverfolk"],used,river)
        if faction == "duchy":
            if len(taken)==1:
                clearing=mapData[getName(image)][taken[0]]["opposite"]
            else:
                clearing=random.choice([i for i in range(1, 13) if mapData[getName(image)][i]["corner"] and i not in taken])
            taken.append(clearing)
            drawHirelingPiece(image,["faction-duchy","faction-duchy","piece-tunnel"],used,clearing)
            for i in mapData[getName(image)][clearing]["adjacent"]:
                drawHirelingPiece(image,["faction-duchy","faction-duchy",],used,i)
        if faction == "corvid":
            drawHirelingPiece(image,["faction-corvid"],used,[i for i in range(1, 13) if mapData[getName(image)][i]["suit"][0]=="rabbit"][-1])
            drawHirelingPiece(image,["faction-corvid"],used,[i for i in range(1, 13) if mapData[getName(image)][i]["suit"][0]=="mouse"][-1])
            drawHirelingPiece(image,["faction-corvid"],used,[i for i in range(1, 13) if mapData[getName(image)][i]["suit"][0]=="fox"][-1])    
    return used,botList
def factionsList(botList):
    factionOptions=list(factionData.keys())
    factionOptions.remove("vagabond2")
    factionOptions = [i for i in  factionOptions if i not in bannedFactions]
    factionMilitant= [i for i in factionOptions if factionData[i]["militant"]]
    if not any([factionData[i]["militant"] for i in botList]):
        militant = random.choice(factionMilitant)
        factionOptions.remove(militant)
        factionMilitant.remove(militant)
        factionList=[militant]
    else:
        factionList=[random.choice(factionOptions)]
        factionOptions.remove(factionList[0])
    if players <= 2 and not any([factionData[i]["militant"] for i in botList]):
        factionOptions=factionMilitant
    for i in range(max(players,2)):
        if (len(factionOptions)==0):
            print("Too many banned factions or hirelings caused an insufficent amount of factions in play. Try restarting the program or unbanning more options to fix it.")
            break
        faction = random.choice(factionOptions)
        if faction == "vagabond" and not "vagabond2" in bannedFactions and random.random() < vagabond2Depriority:
            factionOptions.append("vagabond2")
        factionList.append(faction)
        factionOptions.remove(faction)
    return factionList

def setFactions(image,yPos,botList):
    b=0
    while True:
        factions=factionsList(botList)
        if all(elem in factions for elem in forcedFactions):
            break
        elif b>999:
            print("Could not find set of factions given forced and banned options.")
            break
        b+=1
    xPos=0
    tallest=0
    vagabonds=["adventurer","arbiter","harrier","ranger","ronin","scoundrel","thief","tinker","vagrant"]
    if "vagabond2" not in factions:
        vagabonds = [i for i in  vagabonds if i not in bannedVagabonds]
    for faction in factions:
        imgFaction=Image.open('assets/faction-'+ str(faction) +'.png').convert("RGBA")
        size=(int(imgFaction.width/5),int(imgFaction.height/5))
        imgFaction=imgFaction.resize(size)
        image.paste(imgFaction,(xPos,yPos),mask=imgFaction)
        height=imgFaction.height
        if faction == "vagabond" or faction == "vagabond2":
            character = random.choice(vagabonds)
            charImage=Image.open('assets/vagabond-' + str(character)+'.png').convert("RGBA")
            charImage=charImage.resize((int(charImage.width/6),int(charImage.height/6)))
            image.paste(charImage,(xPos,yPos+50),mask=charImage)
            vagabonds.remove(character)
            if (charImage.height+50>height):
                height=charImage.height+50
        if factions.index(faction) == len(factions)-1 and factionData[faction]["insurgent"] and not any([factionData[i]["militant"] for i in botList]):
            lock=Image.open('assets/icon-lock.png').convert("RGBA")
            lock=lock.resize((38,50))
            image.paste(lock,(xPos+45,yPos+35),mask=lock)
            if (50+35>height):
                height=50+35
        if height>tallest:
            tallest=height
        xPos+=imgFaction.width+3
    return tallest+yPos,factions

def setDeck(image,yPos):
    r = random.random()
    if r<baseDeckChance:
        deck="base"
    else:
        deck="exiles"
    imgDeck=Image.open('assets/deck-'+ str(deck) +'.png').convert("RGBA")
    size=(int(imgDeck.width/7),int(imgDeck.height/7))
    imgDeck=imgDeck.resize(size)
    image.paste(imgDeck,(0,yPos),mask=imgDeck)
    return imgDeck.width

def hirelingsList():
    hirelings=["band","bandits","dynasty","exile","expedition","flamebearers","flotilla","patrol","prophets","protector","spies","uprising","vaultkeepers"]
    hirelings = [i for i in  hirelings if i not in bannedHirelings and hirelingData[i]["faction"] not in forcedFactions]
    random.shuffle(hirelings)
    hirelingList=hirelings[0:min(3,len(hirelings))]
    for hireling in hirelingList:
        if not hirelingData[hireling]["faction"] in bannedFactions:
            bannedFactions.append(hirelingData[hireling]["faction"])
    return hirelingList

def setHirelings(image,xPos,yPos,hirelingList):
    for i,hireling in enumerate(hirelingList):
        arrow="up"
        if i+(players+bots)>4:
            arrow="down"
        imgHireling=Image.open('assets/hireling-'+ str(hireling)+'.png').convert("RGBA")
        size=(75,int(75/imgHireling.width*imgHireling.height))
        imgHireling=imgHireling.resize(size)
        image.paste(imgHireling,(xPos,yPos),mask=imgHireling)
        imgArrow=Image.open('assets/icon-'+ str(arrow) +'.png').convert("RGBA")
        size=(int(imgArrow.width/30),int(imgArrow.height/30))
        imgArrow=imgArrow.resize(size)
        image.paste(imgArrow,(xPos+50,yPos+48),mask=imgArrow)
        xPos+=imgHireling.width+3
def drawObject(image,position,listObjects):
    start=0
    for ob in listObjects:
        img=Image.open('assets/'+ str(ob) +'.png').convert("RGBA")
        sizes=(30,int(30/img.width*img.height))
        img=img.resize(sizes)
        positions=(position[0]+start,position[1])
        image.paste(img,positions,mask=img)
        start+=img.width
        vagabonds=["arbiter","ranger","scoundrel","thief","tinker","vagrant"]
        if ob == "faction-vagabond" or ob == "faction-vagabond2":
            character = random.choice(vagabonds)
            charImage=Image.open('assets/vagabond-' + str(character)+'.png').convert("RGBA")
            charImage=charImage.resize((20,int((20/charImage.width)*charImage.height)))
            image.paste(charImage,(positions[0]+20,positions[1]+20),mask=charImage)
            vagabonds.remove(character)
def drawHirelingPiece(image,hirelings,used,clearing):
    width=used.count(clearing)*30
    if clearing>12:
        position=(mapData[getName(image)]["paths"][clearing-12]["position"][0]+width,mapData[getName(image)]["paths"][clearing-12]["position"][1])
    elif clearing<1:
        position=(mapData[getName(image)]["forests"][clearing+12]["position"][0]+width,mapData[getName(image)]["forests"][clearing+12]["position"][1])
    else:
        position=(mapData[getName(image)][clearing]["position"][0]+width,mapData[getName(image)][clearing]["position"][1])
    drawObject(image,position,hirelings)
    for i in range(len(hirelings)):
        used.append(clearing)
def placeHirelingPieces(image,hirelingList,used):
    for i,hireling in enumerate(hirelingList):
        if i+(players+bots)<=4:
            #promoted
            if hireling=="vaultkeepers":
                clearing = random.choice(range(1,13))
                drawHirelingPiece(image,["hireling-vaultkeepers","hireling-vaultkeepers","hireling-vault"],used,clearing)
            if hireling=="band":
                clearings = random.sample(range(1, 13), 2)
                drawHirelingPiece(image,["hireling-band"],used,clearings[0])
                drawHirelingPiece(image,["hireling-band"],used,clearings[1])
            if hireling == "spies":
                suit=random.choice(["rabbit","fox","mouse"])
                clearings = random.sample([i for i in range(1, 13) if suit in mapData[getName(image)][i]["suit"]],2)
                drawHirelingPiece(image,["hireling-spies"],used,clearings[0])
                drawHirelingPiece(image,["hireling-spies"],used,clearings[1])
            if hireling == "prophets":
                clearings = [i for i in range(1, 13) if mapData[getName(image)][i]["ruins"]]
                for clearing in clearings:
                    drawHirelingPiece(image,["hireling-prophets"],used,clearing)
            if hireling == "expedition":
                clearing = random.choice(range(1,13))
                drawHirelingPiece(image,["hireling-expedition","hireling-expedition","hireling-expedition","hireling-foothold"],used,clearing)
            if hireling == "dynasty":
                clearing = random.choice([i for i in range(1, 13) if mapData[getName(image)][i]["edge"]])
                drawHirelingPiece(image,["hireling-dynasty","hireling-dynasty","hireling-dynasty","hireling-dynasty","hireling-dynasty",],used,clearing)
            if hireling == "patrol":
                for clearing in range(1,13):
                    drawHirelingPiece(image,["hireling-patrol"],used,clearing)
            if hireling == "protector":
                clearing = random.choice(range(1,13))
                drawHirelingPiece(image,["hireling-protector"],used,clearing)
            if hireling == "flamebearers":
                clearing = random.choice(range(1,13))
                drawHirelingPiece(image,["hireling-flamebearers"],used,clearing)
                clearing = random.choice(range(1,13))
                drawHirelingPiece(image,["hireling-flamebearers"],used,clearing)
            if hireling == "flotilla":
                clearing = random.choice([i for i in range(1, 13) if mapData[getName(image)][i]["edge"] and mapData[getName(image)][i]["river"]])
                drawHirelingPiece(image,["hireling-flotilla"],used,clearing)
            if hireling == "uprising":
                suit=random.choice(["rabbit","fox","mouse"])
                clearing = random.choice([i for i in range(1, 13) if suit in mapData[getName(image)][i]["suit"]])
                drawHirelingPiece(image,["hireling-uprising"],used,clearing)
                suit=random.choice(["rabbit","fox","mouse"])
                clearing = random.choice([i for i in range(1, 13) if suit in mapData[getName(image)][i]["suit"]])
                drawHirelingPiece(image,["hireling-uprising"],used,clearing)
            if hireling == "bandits":
                paths=random.sample(list(mapData[getName(image)]["paths"].keys()),2)
                #print(paths)
                for path in paths:
                    drawHirelingPiece(image,["hireling-bandits"],used,path+12)
            if hireling == "exile":
                forest=random.choice(list(mapData[getName(image)]["forests"].keys()))
                drawHirelingPiece(image,["hireling-exile"],used,forest-12)

        #else:
            #demoted if there was one
    return


image = setMap()
result = Image.new(mode="RGBA", size=(image.width+220, image.height+300))
result.filename=image.filename
setSuits(result)
result.paste(image,(0,0),mask=image)
im=result
used,botList=setBots(im)
setLandmarks(im,False)
hirelingList=[]
if hirelingsEnabled:
    hirelingList=hirelingsList()
    placeHirelingPieces(im,hirelingList,used)

posY,factions=setFactions(im,image.height,botList)
posX=setDeck(im,posY+5)
if hirelingsEnabled:
    setHirelings(im,posX,posY+5,hirelingList)
im.save("assets/generate-fullSetup.png",format="png")
pygame.init()
screen = pygame.display.set_mode((820, 820))

player = pygame.image.load(os.path.join("assets/generate-fullSetup.png"))
size = (int(player.get_width()*imageSize),int(player.get_height()*imageSize))
player = pygame.transform.scale(player,size)
player.convert()
running=True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((240,240,255))
    screen.blit(player, (10, 10))
    pygame.display.flip()

pygame.quit()
"""a=0
b=0
n=100000
for i in range(n):
    land=setLandmarks(im,True)
    if 10 in list(land.keys()):
        a+=1
    if "tower" in list(land.values()):
        b+=1
print(a/n)
print(b/n)"""