import math
from datetime import datetime

from GlobalDataset import GlobalDataset


class Record:

    def __init__(self, date, pressure, brightness, hygrometry, temperature, rain, user=None):
        self.date = date
        self.pressure = pressure
        self.brightness = brightness
        self.hygrometry = hygrometry
        self.temperature = temperature
        self.user = user
        self.rain = rain

    def __str__(self):
        return str(self.get_serializable_data())

    @staticmethod
    def create_from_json(jsonRecord):
        return Record(datetime.fromisoformat(jsonRecord["date"]), jsonRecord["pressure"], jsonRecord["brightness"],
                      jsonRecord["hygrometry"], jsonRecord["temperature"], jsonRecord["user"])

    # TODO : Methode à détruire des qu'on a le http
    @staticmethod
    def create_from_json1(jsonRecord):
        return Record(datetime.fromisoformat(jsonRecord["date"]["$date"]), jsonRecord["pressure"],
                      jsonRecord["light"], jsonRecord["humidity"], jsonRecord["temperature"])

    def get_serializable_data(self):
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

    def get_euclidean_distance(self, toCompare):
        count = 0
        count += (self.brightness - toCompare.brightness) ** 2
        count += (self.pressure - toCompare.pressure) ** 2
        count += (self.hygrometry - toCompare.hygrometry) ** 2
        count += (self.temperature - toCompare.temperature) ** 2

        return math.sqrt(count)

    def get_normed_euclidean_distance(self, toCompare, global_dataset: GlobalDataset):

        sum = 0

        if self.brightness and toCompare.brightness:
            if global_dataset.extrema_brightness[1] - global_dataset.extrema_brightness[0] != 0:
                sum += (self.brightness - toCompare.brightness) ** 2 / (global_dataset.extrema_brightness[1] - global_dataset.extrema_brightness[0])**2
            else:
                sum += (self.brightness - toCompare.brightness) ** 2

        if self.pressure and toCompare.pressure:
            if global_dataset.extrema_pressure[1] - global_dataset.extrema_pressure[0] != 0:
                sum += (self.pressure - toCompare.pressure) ** 2 / (global_dataset.extrema_pressure[1] - global_dataset.extrema_pressure[0])**2
            else:
                sum += (self.pressure - toCompare.pressure) ** 2

        if self.hygrometry and toCompare.hygrometry:
            if global_dataset.extrema_hygrometry[1] - global_dataset.extrema_hygrometry[0] != 0:
                sum += (self.hygrometry - toCompare.hygrometry) ** 2 / (global_dataset.extrema_hygrometry[1] - global_dataset.extrema_hygrometry[0])**2
            else:
                sum += (self.hygrometry - toCompare.hygrometry) ** 2

        if self.temperature and toCompare.temperature:
            if global_dataset.extrema_temperature[1] - global_dataset.extrema_temperature[0] != 0:
                sum += (self.temperature - toCompare.temperature) ** 2 / (global_dataset.extrema_temperature[1] - global_dataset.extrema_temperature[0])**2
            else:
                sum += (self.temperature - toCompare.temperature) ** 2

        return math.sqrt(sum)
