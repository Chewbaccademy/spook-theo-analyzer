from multiprocessing import Pool

from tqdm import tqdm
import JSONParser
from Dataset import Dataset
import time

from GlobalDataset import GlobalDataset

DATASET_LENGTH = 5
RESULTS_PER_HOUR = 6
RECORDS_LENGTH = 1000
POOL_SIZE = 7
K = 20


def f(index):
    # print(f'\rTest : {Compter.get_instance().cpt} / {iter_count}', end="")
    subject = Dataset(records[index:index + DATASET_LENGTH])

    ref = Dataset(records[:index] + records[index + DATASET_LENGTH:])

    r_rain = records[index + (DATASET_LENGTH - 1) + RESULTS_PER_HOUR].rain

    nearest = subject.getNearestDataset(ref, K, global_dataset)

    knn = []

    for k in range(K):
        knn.append(ref[nearest[k][1] + RESULTS_PER_HOUR].rain != 0)

    return r_rain, knn


if __name__ == "__main__":
    print("Load dataset...")
    records = JSONParser.read_file_icampus('data.json')[:RECORDS_LENGTH]
    print("Dataset loaded")

    global_dataset = GlobalDataset(records, DATASET_LENGTH)

    records_length = len(records)

    t = 0

    iter_count = records_length - DATASET_LENGTH - RESULTS_PER_HOUR
    pool = Pool(POOL_SIZE)

    print(f'Started at : {time.strftime("%X")}')
    print("\rStarting...")

    result_list_tqdm = []
    knn_success_count = [0 for i in range(K)]
    for res in tqdm(pool.imap_unordered(f, range(iter_count)), total=iter_count):
        for k in range(K):
            c = res[1][:k + 1].count(True)
            if c > k / 2 and res[0]:
                knn_success_count[k] += 1
            elif c <= k / 2 and not res[0]:
                knn_success_count[k] += 1

    print(f'\nEnded at : {time.strftime("%X")}')

    for k in range(K):
        print(f'K={k + 1} => {knn_success_count[k]}\t\t{(knn_success_count[k] * 100) / iter_count}%')
