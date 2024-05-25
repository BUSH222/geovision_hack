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


def digitizer(img, coordsy1, coordsy2, valuey1, valuey2, coordsx1, coordsx2, valuex1, valuex2):  # image is already a PIL image, extracted from graph_processor
    image = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    height, width = img.shape
    x0 = coordsy1[0]
    y0 = coordsy1[1]
    dify = coordsy2[1] - coordsy1[1]
    difvy = valuey2 - valuey1
    scaly, _ = get_scale_from_coords(coordsy1, coordsy2, valuey1, valuey2)
    step = round(scaly * 0.2)
    val0 = valuey1
    # Построчное прохождение по пикселям изображения
    black = []
    points = []
    while y0 > coordsy2[1]:
        points.append([y0, val0])
        y0 -= step
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