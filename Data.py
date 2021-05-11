from datetime import datetime
from JSONParser import JSONParser


class Record:

    def __init__(self, date, pressure, brightness, hygrometry, temperature):
        self.date = date
        self.pressure = pressure
        self.brightness = brightness
        self.hygrometry = hygrometry
        self.temperature = temperature

    @staticmethod
    def createFromJson(jsonRecord):
        newRecord = Record(datetime.fromisoformat(jsonRecord["date"]), jsonRecord["pressure"], jsonRecord["brightness"], jsonRecord["hygrometry"], jsonRecord["temperature"])

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
        }

    def __str__(self):
        return str(self.getSerializableData())

    # def getEuclideanDistance(self, toCompare):
        



    
    
class Dataset:


    def __init__(self, datas):
        self.datas = datas

    @staticmethod
    def createFromJson(jsonList):
        newDataset = Dataset([])

        newDataset.addFromJson(jsonList)

        return newDataset

    # TODO : D2TRUIRE AVEC HTTP
    @staticmethod
    def createFromJson1(jsonList):
        newDataset = Dataset([])

        newDataset.addFromJson1(jsonList)

        return newDataset


    def saveDataset(self, filename):
        uniqueData = []
        for data in self.datas:
            uniqueData.append(data.getSerializableData())

        JSONParser.saveJson(uniqueData, filename)

    
    def getFromTo(self, date_debut, date_fin):
        """
        returns data from a date to another one

        param date_debut : the date from which we retrieve the data
        param date_fin : the date to which we retrieve the data
        """
        data_return = []
        for record in self.datas:
            if( date_debut <= record.date <= date_fin ):
                data_return.append(record)
        return data_return

    def addData(self, recordList):
        for data in recordList:
            self.datas.append(data)

    # TODO : détruire avec http
    def addFromJson1(self, jsonList):
        for jsonRecord in jsonList:
            self.datas.append(Record.createFromJson1(jsonRecord))

    def addFromJson(self, jsonList):
        for jsonRecord in jsonList:
            self.datas.append(Record.createFromJson(jsonRecord))

    def __str__(self):
        retstr = '[ '
        for record in self.datas:
            retstr = retstr + str(record)
            retstr = retstr + ',\n'
        
        retstr = retstr + ' ]'

        return retstr

    