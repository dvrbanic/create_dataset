from PIL import Image
from os.path import isfile, join
from os import listdir

path_labels = "/home/dominik/PycharmProjects/create_dataset/labels"
path_images = "/home/dominik/PycharmProjects/create_dataset/JPEGImages"
path_cropped_img = "/home/dominik/PycharmProjects/create_dataset/cropped"

labels = [f[:-4] for f in listdir(path_labels) if isfile(join(path_labels, f))]

for label in labels:
    img = Image.open(f"{path_images}/{label}.jpg")
    with open(f"{path_labels}/{label}.txt") as f:
        contents = f.read().split()[1:]
        contents = [float(coord) for coord in contents]

        if len(contents) == 0:
            continue

        x_dim = img.size[0]
        y_dim = img.size[1]

        x1 = contents[0] - contents[2] / 2
        y1 = contents[1] - contents[3] / 2
        x2 = contents[0] + contents[2] / 2
        y2 = contents[1] + contents[3] / 2

        x1 = int(x1 * x_dim)
        y1 = int(y1 * y_dim)
        x2 = int(x2 * x_dim)
        y2 = int(y2 * y_dim)

        img_res = img.crop((x1, y1, x2, y2))
        img_res.save(f"{path_cropped_img}/{label}.jpg")

        # img_res.show()
