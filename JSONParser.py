import json
from datetime import datetime

# TODO : cette fontion est pour parser le json de base : A supprimer des que le http est en place
from Record import Record


def read_file_icampus(filename):
    records = []

    with open(filename, 'r') as file:
        for line in file:
            data = json.loads(line)

            date = datetime.fromisoformat(data['date']['$date'].split('+')[0])
            pressure = data['pressure'] if 'pressure' in data else None
            light = data['light'] if 'light' in data else None
            humidity = data['humidity'] if 'humidity' in data else None
            temperature = data['temperature'] if 'temperature' in data else None
            rain = data['rain'] if 'rain' in data else None
            record = Record(
                date,
                pressure,
                light,
                humidity,
                temperature,
                rain)

            records.append(record)

    return records


# -- REAL METHODS --

def readFile(filename):
    with open(filename, 'r') as f:
        return json.loads(f.read())


def saveJson(jsonList, filename):
    file = open(filename, "w")
    file.write("[\n")
    if (len(jsonList) > 1):
        for i in range(len(jsonList)):
            jsonData = jsonList[i]
            file.write(json.dumps(jsonData) + ",\n")
    file.write(json.dumps(jsonList[len(jsonList) - 1]) + "\n")
    file.write("]\n")
    file.close()
