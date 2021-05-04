


class Dataset:

    def __init__(self, data, jsonparser):
        self.data = data
        self.jsonparser = jsonparser

    def getSerializableData(self):
        """
        return the data contained in dataset but serialized 
        
        for exemple, datetime are not serialazable so dates in data are returned in a str iso format
        """
        serData = []

        for datum in self.data:
            datum["date"] = datum["date"].isoformat() # serialize date

            serData.append(datum)
        return serData

    def getFromTo(self, date_debut, date_fin):
        """
        returns data from a date to another one

        param date_debut : the date from which we retrieve the data
        param date_fin : the date to which we retrieve the data
        """
        data_return = []
        for info in self.data:
            if( date_debut <= info["date"] <= date_fin ):
                data_return.append(info)
        return data_return

    def saveData(self):
        """
        save the data in a jsonfile
        """
        self.jsonparser.saveJson(self.getSerializableData())

    
    
