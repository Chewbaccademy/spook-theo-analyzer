import json
from datetime import datetime

class JSONParser:

    def __init__(self, filename:str):
        self.filename = filename

    # TODO : cette fontion est pour parser le json de base : A supprimer des que le http est en place
    def readFile1(self):
        file = open(self.filename, "r")
        jsonData = self.cleanJson1(json.loads(file.read()))
        file.close()
        return jsonData

    # TODO : cette fontion est pour parser le json de base : A supprimer des que le http est en place
    def cleanJson1(self, jsonList):
        new_jsonList = []
        for json in jsonList:
            json["date"] = datetime.fromisoformat(json["date"]["$date"].split('+')[0])
            new_jsonList.append(json)
        return new_jsonList

    #-- REAL METHODS --

    def readFile(self):
        file = open(self.filename, "r")
        return self.cleanJson(json.loads(file.read()))

    def cleanJson(self, jsonList):
        new_jsonList = []
        for json in jsonList:
            json["date"] = datetime.fromisoformat(json["date"]["$date"].split('+')[0])
            new_jsonList.append(json)
        return new_jsonList

    def saveJson(self, jsonList):
        file = open(self.filename, "w")
        file.write("[\n")
        if(len(jsonList) > 1):
            for i in range(len(jsonList)):
                jsonData = jsonList[i]
                file.write(json.dumps(jsonData) + ",\n")
        file.write(json.dumps(jsonList[len(jsonList) - 1]) + "\n")
        file.write("]\n")
        file.close()

        

