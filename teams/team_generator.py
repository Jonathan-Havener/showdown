from ctypes.wintypes import POINT
from collections import defaultdict
import json
from copy import deepcopy
import os
import random

def hasType(pokemon):
    return "ice" in pokemon["types"]

def getPokedex():
    return loadData("../data/pokedex.json")
def getGen3():
    return loadData("teamsByType/gen3anythinggoes/gen3randombattlepokemon")

def loadData(file):
    with open(file) as d:
        dictData = json.load(d)
    return dictData

def addTypeTo(file):
    pokedex = getPokedex()
    pkmnData = loadData(file)
    [pkmnData[pokemon].update({"types":pokedex[''.join(filter(str.isalnum, pokemon.lower()))]["types"]}) for pokemon in pkmnData]
    return pkmnData


def writeTeamToFile(pkmnTeamWType, folderToDeposit):
    teams = defaultdict(lambda:{None: lambda: None})

    for pokemon in pkmnTeamWType:
        for type in pkmnTeamWType[pokemon]["types"]:
            teams[type][pokemon]=pkmnTeamWType[pokemon]
    for team in teams:
        fileName=folderToDeposit+team+".json"
        del teams[team][None]
        with open(fileName, "w") as outfile:
            json.dump(dict(teams[team]), outfile)
    # print(type(dictData))
    # original_pokedex = deepcopy(pokedex)
    # deleteVals = []
    # for pokemon in dictData.keys():
    #     if pokemon.lower() in original_pokedex:
    #         dictData[pokemon]["types"] = original_pokedex[pokemon.lower()]["types"]
    #     else:
    #         deleteVals.append(pokemon)
    # for key in deleteVals:
    #     del dictData[key]
    # print(dictData)

def generateTeam(type,mode):
    baseDir =os.getcwd()+"/teams/teamsByType/"+mode+"/"
    if not os.path.exists(baseDir):
        os.makedirs(baseDir)

    with open(baseDir+type+".json") as d:
        dictData = json.load(d)
    team = random.sample(list(dictData), 6)
    
    printString = ""
    for pokemon in team:
        if "items" in dictData[pokemon]:
            printString+=pokemon+" @ "+ random.choice(dictData[pokemon]["items"])+'\n'
        printString+="Ability: "+random.choice(dictData[pokemon]["abilities"])+'\n'
        printString+="Level: "+ str(dictData[pokemon]["level"])+'\n'
        # if "evs" in dictData[pokemon].keys():
        printString += "EVs: 1 HP"+"\n"
        if len(dictData[pokemon]["moves"]) < 4 :
            moves = dictData[pokemon]["moves"]
        else:
            moves = random.sample(list(dictData[pokemon]["moves"]), 4)
        for move in moves:
            printString+="- "+move+'\n'
        printString+='\n'
    
    ouputDir = os.getcwd()+"/teams/teams/"+mode+"/randomMonotype/"
    if not os.path.exists(ouputDir):
        os.makedirs(ouputDir)
    f = open(ouputDir+type, 'w+')
    f.write(printString)
    f.close()

    return ouputDir+type
        # for k,v in dictData.items():
        #     print(k)

