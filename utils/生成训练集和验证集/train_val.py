import glob
import random
import multiprocessing

def process_file(file_name):
    output = glob.glob('dataset/' + dir + '/images/' + file_name + '.???')[0]
    output.replace('\\', '/').split('/')[-1]
    return './images/' + output + ' ./annotations/' + file_name + '.xml\n'

dir = '6.19_gray_court_voc'
num_processes = multiprocessing.cpu_count() * 1.5  # 指定使用的进程数为 CPU 数量的两倍

path = 'dataset/' + dir
tmp = []
for i in glob.glob(path + '/annotations/*.xml'):
    name = i.replace('\\', '/').split('/')[-1][:-4]
    tmp.append(name)
random.shuffle(tmp)

train = tmp[:int(len(tmp) * 0.8)]
val = tmp[int(len(tmp) * 0.8):]
print('train:', len(train), 'val:', len(val))

# Create a pool of worker processes with specified number of processes
pool = multiprocessing.Pool(processes=num_processes)

with open('dataset/' + dir + '/train.txt', 'w', encoding='utf-8') as f:
    # Process train data using multiple processes
    results = pool.map(process_file, train)
    f.writelines(results)

with open('dataset/' + dir + '/valid.txt', 'w', encoding='utf-8') as f:
    # Process validation data using multiple processes
    results = pool.map(process_file, val)
    f.writelines(results)

# Close the pool of worker processes
pool.close()
pool.join()
