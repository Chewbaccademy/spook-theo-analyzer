from Dataset import Dataset


class GlobalDataset(Dataset):
    def __init__(self, datas, dataset_size):
        super().__init__(datas)

        self.extrema_hygrometry = self.get_extrema_hygrometry()
        self.extrema_pressure = self.get_extrema_pressure()
        self.extrema_temperature = self.get_extrema_temperature()
        self.extrema_brightness = self.get_extrema_brightness()

        self.extrema_evol_temperature = self.get_evolution_extrema_temperature(dataset_size)
        self.extrema_evol_brightness = self.get_evolution_extrema_brightness(dataset_size)
        self.extrema_evol_hygrometry = self.get_evolution_extrema_hygrometry(dataset_size)
        self.extrema_evol_pressure = self.get_evolution_extrema_pressure(dataset_size)

    def get_extrema_brightness(self):
        max_metric = self[0].brightness
        min_metric = self[0].brightness

        for i in self:
            if i.brightness is None:
                continue
            if i.brightness > max_metric:
                max_metric = i.brightness
            elif i.brightness < min_metric:
                min_metric = i.brightness

        return min_metric, max_metric

    def get_extrema_temperature(self):
        max_metric = self[0].temperature
        min_metric = self[0].temperature

        for i in self:
            if i.temperature is None:
                continue
            if i.temperature > max_metric:
                max_metric = i.temperature
            elif i.temperature < min_metric:
                min_metric = i.temperature

        return min_metric, max_metric

    def get_extrema_hygrometry(self):
        max_metric = self[0].hygrometry
        min_metric = self[0].hygrometry

        for i in self:
            if i.hygrometry is None:
                continue
            if i.hygrometry > max_metric:
                max_metric = i.hygrometry
            elif i.hygrometry < min_metric:
                min_metric = i.hygrometry

        return min_metric, max_metric

    def get_extrema_pressure(self):
        max_metric = self[0].pressure
        min_metric = self[0].pressure

        for i in self:
            if i.pressure is None:
                continue
            if i.pressure > max_metric:
                max_metric = i.pressure
            elif i.pressure < min_metric:
                min_metric = i.pressure

        return min_metric, max_metric

    def get_evolution_extrema_pressure(self, dataset_size):
        max_metric = -1000
        min_metric = 1000
        for i in range(len(self) - dataset_size):
            dataset = Dataset(self[i: i + dataset_size])
            evolution = dataset.get_evolution_pressure()
            if evolution > max_metric:
                max_metric = evolution
            elif evolution < min_metric:
                min_metric = evolution

        return min_metric, max_metric

    def get_evolution_extrema_brightness(self, dataset_size):
        max_metric = -1000
        min_metric = 1000
        for i in range(len(self) - dataset_size):
            dataset = Dataset(self[i: i + dataset_size])
            evolution = dataset.get_evolution_brightness()
            if evolution > max_metric:
                max_metric = evolution
            elif evolution < min_metric:
                min_metric = evolution

        return min_metric, max_metric

    def get_evolution_extrema_hygrometry(self, dataset_size):
        max_metric = -1000
        min_metric = 1000
        for i in range(len(self) - dataset_size):
            dataset = Dataset(self[i: i + dataset_size])
            evolution = dataset.get_evolution_hygrometry()
            if evolution > max_metric:
                max_metric = evolution
            elif evolution < min_metric:
                min_metric = evolution

        return min_metric, max_metric

    def get_evolution_extrema_temperature(self, dataset_size):
        max_metric = -1000
        min_metric = 1000
        for i in range(len(self) - dataset_size):
            dataset = Dataset(self[i: i + dataset_size])
            evolution = dataset.get_evolution_temperature()
            if evolution > max_metric:
                max_metric = evolution
            elif evolution < min_metric:
                min_metric = evolution

        return min_metric, max_metric
