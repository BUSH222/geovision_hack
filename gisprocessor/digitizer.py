from PIL import Image
import PIL
import pytesseract
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


def digitizer(img, x, y, value1, value2):  # image is already a PIL image, extracted from graph_processor
    # gray = img.convert('L')
    # width, height = img.size 
    # black = []
    # for y in range(height):
    #     cnt = 0
    #     for x in range(width):
    #         if gray.getpixel((x, y)) == 0:
    #             cnt += 1
    #     if cnt == 1:
    #         black.append((x, y))
    #     elif cnt > 1:
    #         print("2 точки или более")
    #     else:
    #         print("0 точек")
    # return black
    image = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    height, width = image.shape
    get_scale_from_coords(coords1, coords2, value1, value2, log=False, convert_number=None)
    # Построчное прохождение по пикселям изображения
    black = []
    for y in range(height):
        cnt = 0
        for x in range(width):
            pixel = image[y, x]
            if pixel == 0:
                cnt += 1
        if cnt == 1:
            black.append((x, y))
        elif cnt > 1:
            print("2 точки или более")
        else:
            print("0 точек")
    return black

if __name__ == "__main__":
    a = get_scale_from_coords((98, 876), (748, 878), 0, 100, convert_number=50)
    print(a)
    print(digitizer(Image.open(), 100, 100))
