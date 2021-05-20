from datetime import datetime
from typing import List
from JSONParser import JSONParser
import math


class Record:

    def __init__(self, date, pressure, brightness, hygrometry, temperature, user = None):
        self.date = date
        self.pressure = pressure
        self.brightness = brightness
        self.hygrometry = hygrometry
        self.temperature = temperature
        self.user = user


    def __str__(self):
        return str(self.getSerializableData())


    @staticmethod
    def createFromJson(jsonRecord):
        newRecord = Record(datetime.fromisoformat(jsonRecord["date"]), jsonRecord["pressure"], jsonRecord["brightness"], jsonRecord["hygrometry"], jsonRecord["temperature"], jsonRecord["user"])

        return newRecord
    
    # TODO : Methode à détruire des qu'on a le http
    @staticmethod
    def createFromJson1(jsonRecord):
        newRecord = Record(datetime.fromisoformat(jsonRecord["date"]["$date"]), jsonRecord["pressure"], jsonRecord["light"], jsonRecord["humidity"], jsonRecord["temperature"])

        return newRecord


    def getSerializableData(self):
        """
        return the data but in a serialized dict
        
        for exemple, datetime are not serialazable so dates in data are returned in a str iso format
        """
        return {
            'date': self.date.isoformat(),
            'temperature': self.temperature,
            'pressure': self.pressure,
            'hygrometry': self.hygrometry,
            'brightness': self.brightness,
            "user": self.user,
        }



    def getEuclideanDistance(self, toCompare):
        sum = 0
        sum += (self.brightness - toCompare.brightness) ** 2
        sum += (self.pressure - toCompare.pressure) ** 2
        sum += (self.hygrometry - toCompare.hygrometry) ** 2
        sum += (self.temperature - toCompare.temperature) ** 2

        return math.sqrt(sum)


    def getNormedEuclideanDistance(self, toCompare, extrema):

        sum = 0
        if extrema["brightness"] != 0:
            sum += (self.brightness - toCompare.brightness) ** 2 / extrema["brightness"]
        else:
            sum += (self.brightness - toCompare.brightness) ** 2

        
        if extrema["pressure"] != 0:
            sum += (self.pressure - toCompare.pressure) ** 2 / extrema["pressure"]
        else:
            sum += (self.pressure - toCompare.pressure) ** 2
        
        if extrema["hygrometry"] != 0:
            sum += (self.hygrometry - toCompare.hygrometry) ** 2 / extrema["hygrometry"]
        else:
            sum += (self.hygrometry - toCompare.hygrometry) ** 2
        
        if extrema["temperature"] != 0:
            sum += (self.temperature - toCompare.temperature) ** 2 / extrema["temperature"]
        else:
            sum += (self.temperature - toCompare.temperature) ** 2
        

        return math.sqrt(sum)



    
    
class Dataset:


    def __init__(self, datas):
        self.datas = datas
        self.extrema = {
            'brightness': 0,
            'pressure': 0,
            'temperature': 0,
            'hygrometry': 0
        }

    def __str__(self):
        retstr = '[\n'
        for record in self.datas:
            retstr = retstr + '\t' +  str(record) + ',\n'
        
        retstr = retstr + ']'

        return retstr

    def __len__(self):
        return len(self.datas)

    def __iter__(self):
        return iter(self.datas)

    def __getitem__(self, item):
        return self.datas[item]

    def sortByUserAndDate(self, key=None, reverse=None):
        return self.datas.sort(key = lambda data: (data.user, data.date))



    @staticmethod
    def createFromJson(jsonList):
        newDataset = Dataset([])

        newDataset.addFromJson(jsonList)

        return newDataset

    # TODO : DÉTRUIRE AVEC HTTP
    @staticmethod
    def createFromJson1(jsonList):
        newDataset = Dataset([])

        newDataset.addFromJson1(jsonList)

        return newDataset

    @staticmethod
    def createFromAPI():
        return Dataset([])


    def saveDataset(self, filename):
        uniqueData = []
        for data in self:
            uniqueData.append(data.getSerializableData())

        JSONParser.saveJson(uniqueData, filename)

    # TODO : détruire avec http
    def addFromJson1(self, jsonList):
        for jsonRecord in jsonList:
            self.datas.append(Record.createFromJson1(jsonRecord))

    def addFromJson(self, jsonList):
        for jsonRecord in jsonList:
            self.datas.append(Record.createFromJson(jsonRecord))

    def calculExtrema(self, toCompare):

        for i in range(len(toCompare)):
            selfRecord = self[i]
            comparedRecord = toCompare[i]

            currentBrightness = (selfRecord.brightness - comparedRecord.brightness) ** 2
            self.extrema['brightess'] = currentBrightness if currentBrightness > self.extrema['brightness'] else self.extrema['brightness']

            currentPressure = (selfRecord.pressure - comparedRecord.pressure) ** 2
            self.extrema['pressure'] = currentPressure if currentPressure > self.extrema['pressure'] else self.extrema['pressure']

            currentTemperature = (selfRecord.temperature - comparedRecord.temperature) ** 2
            self.extrema['temperature'] = currentTemperature if currentTemperature > self.extrema['temperature'] else self.extrema['temperature']

            currentHygrometry = (selfRecord.hygrometry - comparedRecord.hygrometry) ** 2
            self.extrema['hygrometry'] = currentHygrometry if currentHygrometry > self.extrema['hygrometry'] else self.extrema['hygrometry']


    def getNormedEuclideanDistance(self, toCompare):

        self.calculExtrema(toCompare)
        distance = 0        

        for i in range(len(toCompare)):
                selfRecord = self[i]
                comparedRecord = toCompare[i]
                distance += selfRecord.getNormedEuclideanDistance(comparedRecord, self.extrema)

        return distance


    def getNearestDataset(self, datas):

        nbIteration = len(datas) + 1 - len(self)

        maxDist = -1
        nearestNeighbour = []


        
        datas.sortByUserAndDate()

        print(datas)

        for i in range(nbIteration):
            testNeighbour = datas[i : i+len(self)]

            testDist = self.getNormedEuclideanDistance(Dataset(testNeighbour))
            if maxDist == -1 or maxDist > testDist:
                maxDist = testDist
                nearestNeighbour = testNeighbour

        return nearestNeighbour



