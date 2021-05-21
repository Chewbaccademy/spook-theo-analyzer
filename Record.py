import math
from datetime import datetime


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

    def get_normed_euclidean_distance(self, toCompare, extrema):

        sum = 0

        if self.brightness and toCompare.brightness:
            if extrema["brightness"] != 0:
                sum += (self.brightness - toCompare.brightness) ** 2 / extrema["brightness"]
            else:
                sum += (self.brightness - toCompare.brightness) ** 2

        if self.pressure and toCompare.pressure:
            if extrema["pressure"] != 0:
                sum += (self.pressure - toCompare.pressure) ** 2 / extrema["pressure"]
            else:
                sum += (self.pressure - toCompare.pressure) ** 2

        if self.hygrometry and toCompare.hygrometry:
            if extrema["hygrometry"] != 0:
                sum += (self.hygrometry - toCompare.hygrometry) ** 2 / extrema["hygrometry"]
            else:
                sum += (self.hygrometry - toCompare.hygrometry) ** 2

        if self.temperature and toCompare.temperature:
            if extrema["temperature"] != 0:
                sum += (self.temperature - toCompare.temperature) ** 2 / extrema["temperature"]
            else:
                sum += (self.temperature - toCompare.temperature) ** 2

        return math.sqrt(sum)
