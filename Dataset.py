import JSONParser


class Dataset:

    def __init__(self, datas):
        self.datas = datas

    def __str__(self):
        retstr = '[\n'
        for record in self.datas:
            retstr = retstr + '\t' + str(record) + ',\n'

        retstr += ']'

        return retstr

    def __len__(self):
        return len(self.datas)

    def __iter__(self):
        return iter(self.datas)

    def __getitem__(self, item):
        return self.datas[item]

    def sortByUserAndDate(self, key=None, reverse=None):
        return self.datas.sort(key=lambda data: (data.user, data.date))

    def saveDataset(self, filename):
        uniqueData = []
        for data in self:
            uniqueData.append(data.getSerializableData())

        JSONParser.saveJson(uniqueData, filename)

    def calculExtrema(self, toCompare):

        extrema = {
            'brightness': 0,
            'pressure': 0,
            'temperature': 0,
            'hygrometry': 0
        }

        for i in range(len(toCompare)):
            selfRecord = self[i]
            comparedRecord = toCompare[i]

            if selfRecord.brightness and comparedRecord.brightness:
                currentBrightness = (selfRecord.brightness - comparedRecord.brightness) ** 2
                extrema['brightess'] = currentBrightness if currentBrightness > extrema['brightness'] else \
                    extrema['brightness']

            if selfRecord.pressure and comparedRecord.pressure:
                currentPressure = (selfRecord.pressure - comparedRecord.pressure) ** 2
                extrema['pressure'] = currentPressure if currentPressure > extrema['pressure'] else extrema[
                    'pressure']

            if selfRecord.temperature and comparedRecord.temperature:
                currentTemperature = (selfRecord.temperature - comparedRecord.temperature) ** 2
                extrema['temperature'] = currentTemperature if currentTemperature > extrema['temperature'] else \
                    extrema['temperature']

            if selfRecord.hygrometry and comparedRecord.hygrometry:
                currentHygrometry = (selfRecord.hygrometry - comparedRecord.hygrometry) ** 2
                extrema['hygrometry'] = currentHygrometry if currentHygrometry > extrema['hygrometry'] else \
                    extrema['hygrometry']

        return extrema

    def get_evolution_brightness(self):
        first = self[0].brightness
        last = self[len(self) - 1].brightness

        if first is None or last is None:
            return 0
        return first - last

    def get_evolution_temperature(self):
        first = self[0].temperature
        last = self[len(self) - 1].temperature

        if first is None or last is None:
            return 0
        return first - last

    def get_evolution_pressure(self):
        first = self[0].pressure
        last = self[len(self) - 1].pressure
        if first is None or last is None:
            return 0
        return first - last

    def get_evolution_hygrometry(self):
        first = self[0].hygrometry
        last = self[len(self) - 1].hygrometry

        if first is None or last is None:
            return 0
        return first - last

    def getNormedEuclideanDistance(self, toCompare, global_dataset):

        extrema = self.calculExtrema(toCompare) # TODO : externalise

        distance = 0

        for i in range(len(toCompare)):
            self_record = self[i]
            compared_record = toCompare[i]
            distance += self_record.get_normed_euclidean_distance(compared_record, global_dataset)

        distance += ((self.get_evolution_brightness() - toCompare.get_evolution_brightness())**2)/((global_dataset.extrema_evol_brightness[1] - global_dataset.extrema_evol_brightness[0])**2)
        distance += ((self.get_evolution_hygrometry() - toCompare.get_evolution_hygrometry())**2)/((global_dataset.extrema_evol_hygrometry[1] - global_dataset.extrema_evol_hygrometry[0])**2)
        distance += ((self.get_evolution_pressure() - toCompare.get_evolution_pressure())**2)/((global_dataset.extrema_evol_pressure[1] - global_dataset.extrema_evol_pressure[0])**2)
        distance += ((self.get_evolution_temperature() - toCompare.get_evolution_temperature())**2)/((global_dataset.extrema_evol_temperature[1] - global_dataset.extrema_evol_temperature[0])**2)

        return distance

    def getNearestDataset(self, references, k: int, global_dataset):
        """

        :param global_dataset:
        :param k:
        :param references: Global dataset
        :return: list(tuple (float, int))
        """

        dists = [(-1, -1) for _ in range(k)]

        max_iter = len(references) + 1 - len(self) - 6

        for i in range(max_iter):
            reference = Dataset(references[i: i + len(self)])

            test_dist = self.getNormedEuclideanDistance(reference, global_dataset)

            for j in range(k):
                if dists[j][0] == -1 or dists[j][0] > test_dist:
                    dists[j] = (test_dist, i)
                    dists.sort(key=lambda s: s[0])
                    break

        return dists
