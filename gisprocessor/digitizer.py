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


def digitizer(img, coordsx1, coordsx2, valuex1, valuex2, coordsy1, coordsy2, valuey1, valuey2):
    image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    x0 = coordsy1[0]
    y0 = coordsy1[1]
    scaly, _ = get_scale_from_coords(coordsy1, coordsy2, valuey1, valuey2)
    stepy = round(scaly * 0.2)
    scalx, _ = get_scale_from_coords(coordsy1, coordsy2, valuex1, valuex2)
    stepx = round(scalx * 0.2)
    # Построчное прохождение по пикселям изображения
    resblack = []
    points = []
    # for y axis
    while y0 < coordsy2[1]:
        points.append(y0)
        y0 += stepy
        cnt = 0
        blackx = []
        for x in range(coordsx1[0], coordsx2[0]):
            pixel = list(image[y0, x])
            if pixel == [0, 0, 0]:
                blackx.append(x)
                cnt += 1
        if cnt == 0:
            resy = 1/get_scale_from_coords(coordsy1, coordsy2, valuey1, valuey2)[0]*(y0 - coordsy1[1])
            resblack.append([round(resy, 4), -9999])
        else:
            resx = 1/get_scale_from_coords(coordsx1, coordsx2, valuex1, valuex2)[0]*(round(sum(blackx)/cnt) - coordsx1[0])
            resy = 1/get_scale_from_coords(coordsy1, coordsy2, valuey1, valuey2)[0]*(y0 - coordsy1[1])
            # resblack.append([y0, round(sum(blackx)/cnt)])
            resblack.append([round(resy, 4), round(resx, 4)])
    # for x axis
    print(resblack)
    return resblack



if __name__ == "__main__":
    # a = get_scale_from_coords((98, 876), (748, 878), 0, 100, convert_number=50)
    # print(a)

    a = get_scale_from_coords((98, 876), (748, 878), 0, 100)
    print(1/a[0]*(590-98))
    # print(digitizer(Image.open(), 100, 100))
    # get_scale_from_coords((0, 0), (10, 10), 0, 10, convert_number=1)
