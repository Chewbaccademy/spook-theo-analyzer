import JSONParser
from Dataset import Dataset
import time

DATASET_LENGTH = 5
RESULTS_PER_HOUR = 6
RECORDS_LENGTH = 10011

if __name__ == "__main__":
    print("Load dataset...")
    records = JSONParser.read_file_icampus('data.json')[:RECORDS_LENGTH]
    print("Dataset loaded")
    records_length = len(records)

    t = 0

    iter_count = records_length - DATASET_LENGTH - RESULTS_PER_HOUR
    success_count = 0

    print(f'Started at : {time.strftime("%X")}')
    print("\rStarting...")
    for i in range(iter_count):
        print(f'\rTest : {i} / {iter_count}', end="")
        subject = Dataset(records[i:i + DATASET_LENGTH])

        ref = Dataset(records[:i] + records[i + DATASET_LENGTH:])

        nearest = subject.getNearestDataset(ref)

        n_rain = ref[nearest[1] + RESULTS_PER_HOUR].rain
        r_rain = records[i + (DATASET_LENGTH - 1) + RESULTS_PER_HOUR].rain

        if n_rain and r_rain and (n_rain > 0 and r_rain > 0) or (n_rain == 0 and r_rain == 0):
            success_count += 1

    print(f'\nEnded at : {time.strftime("%X")}')
    print(f'Success count = {success_count}')
    print(f'Result = {(success_count * 100) / iter_count}%')

    # random.seed()
    #
    # registeredDataset = Dataset.createFromJson(JSONParser.readFile("./registeredData.json"))
    # newDataset = Dataset.createFromJson1(JSONParser.readFile1("./entry.json"))
    #
    # Datatest1 = Dataset([
    #     newDataset.datas[5],
    #     newDataset.datas[6],
    #     newDataset.datas[7],
    # ])
    #
    # print(Dataset(Datatest1.getNearestDataset(registeredDataset)))
