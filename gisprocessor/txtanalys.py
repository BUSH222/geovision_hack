import pytesseract
from PIL import Image
import cv2
import numpy as np
from pytesseract import Output
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
def txtconvert(filename):
    img = Image.open(filename)

    cust_config = r'--oem 3 --psm 6'

    text = pytesseract.image_to_string(img, lang="rus")
    print(text)



def divide_image_by_black_lines(image_path):
    img = cv2.imread(image_path)
    height, width, _ = img.shape
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    _, binary_img = cv2.threshold(edges, 127, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    columns = []

    if contours:
        # Получение координат первого столбца
        start_x = 0
        contours = contours[::-1]
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if h > height * 0.8:

                column = img[:, start_x:x]

                columns.append(column)

                start_x = x

                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Добавление последнего столбца
        columns.append(img[:, start_x:])

        return columns, img

    else:
        print("Черные линии не найдены на изображении.")
        return None, img

def get_text_coordinates(image_path, first_coord):
    def contains_three_digits(s):
        return sum(character.isdigit() for character in s) >= 3
    def remove_non_digits(s):
        return ''.join(character for character in s if character.isdigit() or character == ".")
    res = dict()
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    d = pytesseract.image_to_data(gray, output_type=Output.DICT, lang="rus")
    text_coordinates = []
    stcoords = False
    temp = 0
    for i in range(len(d['text'])):
        if first_coord in d["text"][i]:
            stcoords = True
        if int(d['conf'][i]) > 60 and stcoords and contains_three_digits(d["text"]):
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text_coordinates.append((x, y, w, h))
            res[remove_non_digits(d["text"][i])] = (x, y, w, h)
    return res, img


if __name__ == '__main__':
    # txtconvert("imageT.png")
    # columns, img_with_rectangles = divide_image_by_black_lines('imageT.png')

    # if columns is not None:
    #     for i, column in enumerate(columns):
    #         print(i, column)
    #         cv2.imwrite(f'column_{i+1}.jpg', column)

    # cv2.imwrite('img_with_rectangles.jpg', img_with_rectangles)
    coord, img_with_rectangles = get_text_coordinates("imageT.png", "2532")
    print(coord)
    cv2.imwrite('img_with_rectangles.jpg', img_with_rectangles)