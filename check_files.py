from os import listdir
from os.path import isfile, join

path_images = "/home/dominik/PycharmProjects/create_dataset/JPEGImages"
path_labels = "/home/dominik/PycharmProjects/create_dataset/labels"

images = [f[:-4] for f in listdir(path_images) if isfile(join(path_images, f))]
print(len(images), images[0])

labels = [f[:-4] for f in listdir(path_labels) if isfile(join(path_labels, f))]
print(len(labels), labels[0])

ct_good = 0
ct_bad = 0
bad_images = []
for i in labels:
    if i in images:
        ct_good += 1
    else:
        ct_bad += 1
        bad_images.append(i)

print("ct_good: ", ct_good)
print("ct_bad: ", ct_bad)
print(bad_images)
