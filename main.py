from JSONParser import JSONParser
from Dataset import Dataset
from datetime import datetime

if __name__ == "__main__":

    entryParser = JSONParser("./entry.json")
    parser = JSONParser("./registeredData.json")
    dataset = Dataset(entryParser.readFile(), parser)

    print(dataset.getFromTo(datetime.fromisoformat("2017-04-27T06:00:00"), datetime.fromisoformat("2017-04-27T12:00:33")))

    dataset.saveData()
    
