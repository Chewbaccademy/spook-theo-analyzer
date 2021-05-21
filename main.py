from multiprocessing import Pool

from tqdm import tqdm
import JSONParser
from Dataset import Dataset
import time

DATASET_LENGTH = 5
RESULTS_PER_HOUR = 6
RECORDS_LENGTH = 10011
POOL_SIZE = 5


def f(index):
    # print(f'\rTest : {Compter.get_instance().cpt} / {iter_count}', end="")
    subject = Dataset(records[index:index + DATASET_LENGTH])

    ref = Dataset(records[:index] + records[index + DATASET_LENGTH:])

    nearest = subject.getNearestDataset(ref)

    n_rain = ref[nearest[1] + RESULTS_PER_HOUR].rain
    r_rain = records[index + (DATASET_LENGTH - 1) + RESULTS_PER_HOUR].rain

    return n_rain and r_rain and (n_rain > 0 and r_rain > 0) or (n_rain == 0 and r_rain == 0)


if __name__ == "__main__":
    print("Load dataset...")
    records = JSONParser.read_file_icampus('data.json')[:RECORDS_LENGTH]
    print("Dataset loaded")
    records_length = len(records)

    t = 0

    iter_count = records_length - DATASET_LENGTH - RESULTS_PER_HOUR
    pool = Pool(POOL_SIZE)

    print(f'Started at : {time.strftime("%X")}')
    print("\rStarting...")
    # with pool:
    result_list_tqdm = []
    # results = pool.map(f, range(iter_count))
    success_count = 0
    for i in tqdm(pool.imap_unordered(f, range(iter_count)), total=iter_count):
        success_count += 1 if i  else 0

    print(f'\nEnded at : {time.strftime("%X")}')
    print(f'Success count = {success_count}')
    print(f'Result = {(success_count * 100) / iter_count}%')
