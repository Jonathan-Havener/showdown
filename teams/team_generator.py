from ctypes.wintypes import POINT
from collections import defaultdict
import json
from copy import deepcopy
import os
import random

def hasType(pokemon):
    return "ice" in pokemon["types"]

def funcA(pokedex):
    teams = defaultdict(lambda:{None: lambda: None})

    with open("teams/gen8randombattlepokemon.json") as d:
        dictData = json.load(d)
    for pokemon in dictData:
        for type in dictData[pokemon]["types"]:
            teams[type][pokemon]=dictData[pokemon]
    for team in teams:
        fileName="test/"+team+".json"
        del teams[team][None]
        with open(fileName, "w") as outfile:
            json.dump(dict(teams[team]), outfile)
    print ("end")
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

def generateTeam(type):
    baseDir =os.getcwd()+"/teams/teamsByType/"

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
    
    f = open(os.getcwd()+"/teams/teams/randomMonotype/"+type, 'w')
    f.write(printString)
    f.close()

    return os.getcwd()+"/teams/teams/randomMonotype/"+type
        # for k,v in dictData.items():
        #     print(k)

