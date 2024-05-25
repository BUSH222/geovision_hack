from PIL import Image
import cv2
import numpy as np


def get_scale_from_coords(coords1, coords2, value1, value2, log=False, convert_number=None):
    (x1, y1), (x2, y2) = coords1, coords2
    # detect axis
    xaxis = False
    if abs(x2-x1) > abs(y2-y1):
        scale = abs(x2-x1)/abs(value1-value2)
        xaxis = True
    else:
        scale = abs(y2-y1)/abs(value1-value2)
    if convert_number is None:
        return scale, xaxis
    else:
        if xaxis:
            return x1+scale*convert_number, y1
        else:
            return x1, y1*scale*convert_number


def digitizer(img, coords1, coords2, value1, value2):  # image is already a PIL image, extracted from graph_processor
    image = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    height, width = img.shape
    x0 = coords1[0]
    y0 = coords1[1]
    dif = coords2[1] - coords1[1]
    difv = value2 - value1
    val0 = value1
    # Построчное прохождение по пикселям изображения
    black = []
    points = []
    while y0 > 0:
        points.append([y0, val0])
        y0 -= dif
        val0 += difv
    for y in range(y0)[::-1]:
        cnt = 0
        for x in range(x0 + 70, width):
            pixel = image[y, x]
            if pixel == 0:
                tempx = x
                cnt += 1
        if cnt == 1:
            black.append((tempx, y0))
        elif cnt > 1:
            print("2 точки или более")
        else:
            print("0 точек")
    return black, points


if __name__ == "__main__":
    # a = get_scale_from_coords((98, 876), (748, 878), 0, 100, convert_number=50)
    # print(a)

    a = get_scale_from_coords((98, 876), (748, 878), 0, 100)
    print(1/a[0]*(590-98))
    # print(digitizer(Image.open(), 100, 100))
    # get_scale_from_coords((0, 0), (10, 10), 0, 10, convert_number=1)