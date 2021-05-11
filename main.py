from JSONParser import JSONParser
from Data import Record, Dataset
from datetime import datetime

if __name__ == "__main__":

    jsonParser = JSONParser()
    registeredDataset = Dataset.createFromJson(JSONParser.readFile1("./registeredData.json"))
    newDataset = Dataset.createFromJson1(JSONParser.readFile1("./entry.json"))

    newDataset.saveDataset("./registeredData.json")

    print(registeredDataset)
    
