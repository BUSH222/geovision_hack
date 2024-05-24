from pil_converter import pil_convert
import cv2
import numpy as np
from PIL import Image


def process_image(img, color_range):
    (R1, G1, B1), (R2, G2, B2) = color_range
    data = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = data[x, y]
            if not (R1 <= r <= R2 and G1 <= g <= G2 and B1 <= b <= B2) or (r < g+20 and r < b+20):
                # Change the color to black
                data[x, y] = (0, 0, 0)
    return img


def remove_noise(image):
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #_, binary = cv2.threshold(gray, 0, 0, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    large_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 10]
    mask = np.zeros_like(gray)
    cv2.drawContours(mask, large_contours, -1, (255), thickness=cv2.FILLED)

    cleaned_image = cv2.bitwise_and(image, image, mask=mask)

    cleaned_image = Image.fromarray(cv2.cvtColor(cleaned_image, cv2.COLOR_BGR2RGB))

    return cleaned_image


prepro = process_image(pil_convert('DATA/well_3_old.jpg'), [[130, 70, 70], [200, 160, 160]])
prepro.save('DATA/OUT/res0.png')
remove_noise(prepro).save('DATA/OUT/res.png')