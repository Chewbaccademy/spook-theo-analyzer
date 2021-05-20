from JSONParser import JSONParser
from Data import Record, Dataset
import random

    

if __name__ == "__main__":
    random.seed()

    jsonParser = JSONParser()
    registeredDataset = Dataset.createFromJson(JSONParser.readFile("./registeredData.json"))
    newDataset = Dataset.createFromJson1(JSONParser.readFile1("./entry.json"))

    Datatest1 = Dataset([
        newDataset.datas[5],
        newDataset.datas[6],
        newDataset.datas[7],
    ])

    print(Dataset(Datatest1.getNearestDataset(registeredDataset)))

    

    
    
