import glob
import random

dir = 'person'

path = 'dataset/' + dir
tmp = []
for i in glob.glob(path + '/annotations/*.xml'):
    name = i.replace('\\', '/').split('/')[-1][:-4]
    tmp.append(name)
random.shuffle(tmp)
# print(tmp)
train = tmp[:int(len(tmp) * 0.8)]
val = tmp[int(len(tmp) * 0.8):]
print('train:', len(train), 'val:', len(val))
with open('dataset/' + dir + '/train.txt', 'w', encoding='utf-8') as f:
    for i in train:
        output = glob.glob('dataset/' + dir + '/images/' + i + '.???')[0].replace('\\', '/').split('/')[-1]
        f.write('./images/' + output + ' ./annotations/' + i + '.xml\n')
with open('dataset/' + dir + '/valid.txt', 'w', encoding='utf-8') as f:
    for i in val:
        output = glob.glob('dataset/' + dir + '/images/' + i + '.???')[0].replace('\\', '/').split('/')[-1]
        f.write('./images/' + output + ' ./annotations/' + i + '.xml\n')