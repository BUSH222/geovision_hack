from pil_converter import pil_convert
import cv2
import numpy as np
from PIL import Image


def process_image(image, color_range):
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    (R1, G1, B1), (R2, G2, B2) = color_range
    lower_range = np.array([B1, G1, R1], dtype=np.uint8)
    upper_range = np.array([B2, G2, R2], dtype=np.uint8)

    mask = cv2.inRange(image, lower_range, upper_range)
    mask_inv = cv2.bitwise_not(mask)

    image[mask_inv > 0] = [255, 255, 200]

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # _, binary = cv2.threshold(gray, 0, 0, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    large_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 50]
    mask = np.zeros_like(gray)
    cv2.drawContours(mask, large_contours, -1, (255), thickness=cv2.FILLED)

    cleaned_image = cv2.bitwise_and(image, image, mask=mask)

    cleaned_image = Image.fromarray(cv2.cvtColor(cleaned_image, cv2.COLOR_BGR2RGB))

    return cleaned_image


prepro = process_image(pil_convert('DATA/well_3_old.jpg'), [[130, 70, 70], [200, 160, 160]])
prepro.save('DATA/OUT/res0.png')

prepro2 = process_image(pil_convert('DATA/well_3_old.jpg'), [[0, 0, 0], [100, 100, 100]])
prepro2.save('DATA/OUT/res1.png')