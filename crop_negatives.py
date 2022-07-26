import random

from PIL import Image
from os.path import isfile, join
from os import listdir

path_labels = "/home/dominik/PycharmProjects/create_dataset/labels"
path_images = "/home/dominik/PycharmProjects/create_dataset/JPEGImages"
path_cropped_neg_img = "/home/dominik/PycharmProjects/create_dataset/cropped_negatives"


def get_iou(bb1, bb2):
    """
    Calculate the Intersection over Union (IoU) of two bounding boxes.

    Parameters
    ----------
    bb1 : dict
        Keys: {'x1', 'x2', 'y1', 'y2'}
        The (x1, y1) position is at the top left corner,
        the (x2, y2) position is at the bottom right corner
    bb2 : dict
        Keys: {'x1', 'x2', 'y1', 'y2'}
        The (x, y) position is at the top left corner,
        the (x2, y2) position is at the bottom right corner

    Returns
    -------
    float
        in [0, 1]
    """
    assert bb1['x1'] < bb1['x2']
    assert bb1['y1'] < bb1['y2']
    assert bb2['x1'] < bb2['x2']
    assert bb2['y1'] < bb2['y2']

    # determine the coordinates of the intersection rectangle
    x_left = max(bb1['x1'], bb2['x1'])
    y_top = max(bb1['y1'], bb2['y1'])
    x_right = min(bb1['x2'], bb2['x2'])
    y_bottom = min(bb1['y2'], bb2['y2'])

    if x_right < x_left or y_bottom < y_top:
        return 0.0

    # The intersection of two axis-aligned bounding boxes is always an
    # axis-aligned bounding box
    intersection_area = (x_right - x_left) * (y_bottom - y_top)

    # compute the area of both AABBs
    bb1_area = (bb1['x2'] - bb1['x1']) * (bb1['y2'] - bb1['y1'])
    bb2_area = (bb2['x2'] - bb2['x1']) * (bb2['y2'] - bb2['y1'])

    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = intersection_area / float(bb1_area + bb2_area - intersection_area)
    assert iou >= 0.0
    assert iou <= 1.0
    return iou


labels = [f[:-4] for f in listdir(path_labels) if isfile(join(path_labels, f))]

ct = 0
for label in labels:
    ct += 1
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

    x1_real = int(x1 * x_dim)
    y1_real = int(y1 * y_dim)
    x2_real = int(x2 * x_dim)
    y2_real = int(y2 * y_dim)

    x2 = random.randrange(10, int(x_dim*0.8))
    y2 = random.randrange(10, int(y_dim*0.8))

    x1 = random.randrange(0, x2)
    y1 = random.randrange(0, y2)

    bb1 = {'x1': x1, 'x2': x2, 'y1': y1, 'y2': y2}
    bb2 = {'x1': x1_real, 'x2': x2_real, 'y1': y1_real, 'y2': y2_real}

    if get_iou(bb1, bb2) > 0:
        continue

    img_res = img.crop((x1, y1, x2, y2))
    img_res.save(f"{path_cropped_neg_img}/{label}_2.jpg")

    if ct % 100 == 0:
        print(ct)

    # img_res.show()
