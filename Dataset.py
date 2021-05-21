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


    def getNormedEuclideanDistance(self, toCompare):

        extrema = self.calculExtrema(toCompare)

        distance = 0

        for i in range(len(toCompare)):
            self_record = self[i]
            compared_record = toCompare[i]
            distance += self_record.get_normed_euclidean_distance(compared_record, extrema)

        return distance

    def getNearestDataset(self, datas):
        """

        :param datas: [Dataset]
        :return:
        """

        nbIteration = len(datas) + 1 - len(self) - 6

        maxDist = -1
        nearestNeighbour = None

        datas.sortByUserAndDate()


        for i in range(nbIteration):
            testNeighbour = datas[i: i + len(self)]

            testDist = self.getNormedEuclideanDistance(Dataset(testNeighbour))
            if maxDist == -1 or maxDist > testDist:
                maxDist = testDist
                nearestNeighbour = (testDist, i)

        return nearestNeighbour
