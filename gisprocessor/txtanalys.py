import pytesseract
from PIL import Image
import cv2
import numpy as np

def txtconvert(filename):
    img = Image.open(filename)

    cust_config = r'--oem 3 --psm 6'
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    text = pytesseract.image_to_string(img, lang="rus")
    print(text)



def divide_image_by_black_lines(image_path):
    img = cv2.imread(image_path)
    height, width, _ = img.shape
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, binary_img = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)

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


if __name__ == '__main__':
    # txtconvert("image.png")
    columns, img_with_rectangles = divide_image_by_black_lines('imageg.png')

    if columns is not None:
        for i, column in enumerate(columns):
            print(i, column)
            # cv2.imwrite(f'column_{i+1}.jpg', column)

    cv2.imwrite('img_with_rectangles.jpg', img_with_rectangles)
