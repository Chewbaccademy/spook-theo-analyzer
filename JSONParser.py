import json
from datetime import datetime

class JSONParser:

    # TODO : cette fontion est pour parser le json de base : A supprimer des que le http est en place
    @staticmethod
    def readFile1(filename):
        file = open(filename, "r")
        jsonData = json.loads(file.read())

        # remise en iso de la date
        for i in range(len(jsonData)):
            jsonData[i]["date"]["$date"] = jsonData[i]["date"]["$date"].split('+')[0]
        

        file.close()
        return jsonData

    #-- REAL METHODS --

    @staticmethod
    def readFile(filename):
        file = open(filename, "r")
        return json.loads(file.read())

    @staticmethod
    def saveJson(jsonList, filename):
        file = open(filename, "w")
        file.write("[\n")
        if(len(jsonList) > 1):
            for i in range(len(jsonList)):
                jsonData = jsonList[i]
                file.write(json.dumps(jsonData) + ",\n")
        file.write(json.dumps(jsonList[len(jsonList) - 1]) + "\n")
        file.write("]\n")
        file.close()

        

