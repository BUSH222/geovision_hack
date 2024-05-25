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


def digitizer(img, coordsx1, coordsx2, valuex1, valuex2, coordsy1, coordsy2, valuey1, valuey2):  # image is already a PIL image, extracted from graph_processor
    image = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    height, width = img.shape
    x0 = coordsy1[0]
    y0 = coordsy1[1]
    dify = coordsy2[1] - coordsy1[1]
    difvy = valuey2 - valuey1
    scaly, _ = get_scale_from_coords(coordsy1, coordsy2, valuey1, valuey2)
    stepy = round(scaly * 0.2)
    scalx, _ = get_scale_from_coords(coordsy1, coordsy2, valuex1, valuex2)
    stepx = round(scalx * 0.2)
    val0 = valuey1
    # Построчное прохождение по пикселям изображения
    resblack = []
    points = []
    blackx = []
    # for y axis
    while y0 > coordsy2[1]:
        points.append(y0)
        y0 -= stepy
        cnt = 0
        for x in range(coordsx1[0], coordsx2[0]):
            pixel = image[x, y0]
            if pixel == 0:
                blackx.append(x)
                cnt += 1
        if max(blackx) - min(blackx) < 100:
            resblack.append(-9999)
        else:
            resblack.append(y0, sum(blackx)/cnt)
    # for x axis
    pointsx = []
    while x0 < coordsy2[0]:
        points.append(x0)
        x0 -= stepx
        cnt = 0
    return resblack
    # for y in range(y0)[::-1]:
    #     cnt = 0
    #     for x in range(x0 + 70, width):
    #         pixel = image[y, x]
    #         if pixel == 0:
    #             tempx = x
    #             cnt += 1
    #     if cnt == 1:
    #         black.append((tempx, y0))
    #     elif cnt > 1:
    #         print("2 точки или более")
    #     else:
    #         print("0 точек")
    # return black, points


if __name__ == "__main__":
    # a = get_scale_from_coords((98, 876), (748, 878), 0, 100, convert_number=50)
    # print(a)

    a = get_scale_from_coords((98, 876), (748, 878), 0, 100)
    print(1/a[0]*(590-98))
    # print(digitizer(Image.open(), 100, 100))
    # get_scale_from_coords((0, 0), (10, 10), 0, 10, convert_number=1)