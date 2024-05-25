from pil_converter import pil_convert
import cv2
import numpy as np
from PIL import Image


def split_hue(hue, delta):
    hue_minus_delta = hue - delta
    hue_plus_delta = hue + delta
    hue_split1 = hue
    if hue_minus_delta < 0:
        hue_minus_delta += 180
        hue_split1 = 180
    if hue_plus_delta > 180:
        hue_plus_delta -= 180
    return hue_minus_delta, hue_split1, hue_split1-180, hue_plus_delta


def graph_preprocess(image, color_range=[], use_hsv=False, approx_hue=0, delta_hue=40, denoise=0):
    if not use_hsv:
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        (R1, G1, B1), (R2, G2, B2) = color_range
        lower_range = np.array([B1, G1, R1], dtype=np.uint8)
        upper_range = np.array([B2, G2, R2], dtype=np.uint8)
        mask = cv2.inRange(image, lower_range, upper_range)
        mask_inv = cv2.bitwise_not(mask)

        image[mask_inv > 0] = [255, 255, 255]
        image[mask_inv <= 0] = [0, 0, 0]
    else:
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2HSV)
        (_, G1, G2), (_, B1, B2) = color_range
        hue1_low, hue1_high, hue2_low, hue2_high = split_hue(approx_hue, delta_hue)
        lower_range = np.array([hue2_low, G1, B1])
        upper_range = np.array([hue2_high, G2, B2])
        lower_range2 = np.array([hue1_low, G1, B1])
        upper_range2 = np.array([hue1_high, G2, B2])
        mask = cv2.inRange(image, lower_range, upper_range)
        mask2 = cv2.inRange(image, lower_range2, upper_range2)
        image = cv2.cvtColor(image, cv2.COLOR_HSV2RGB)
        mask_inv1 = cv2.bitwise_not(mask)
        mask_inv2 = cv2.bitwise_not(mask2)
        mask_inv = cv2.bitwise_and(mask_inv1, mask_inv2)
        image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
        image[mask_inv > 0] = [255, 255, 255]
        image[mask_inv <= 0] = [0, 0, 0]

    ## DENOISE 1
    if denoise >= 1:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        large_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 500]
        mask = np.zeros_like(gray)
        cv2.drawContours(mask, large_contours, -1, (255), thickness=cv2.FILLED)

        image = cv2.bitwise_and(image, image, mask=mask)

    ## DENOISE 2
    if denoise >= 2:
        blurred_img = cv2.medianBlur(image, 5)
        kernel = np.ones((3, 3), np.uint8)
        eroded_img = cv2.erode(blurred_img, kernel, iterations=1)
        _, image = cv2.threshold(eroded_img, 127, 255, cv2.THRESH_BINARY)

    return Image.fromarray(image)


if __name__ == "__main__":
    prepro1 = graph_preprocess(pil_convert('DATA/well_3_old.jpg'), [(0, 70, 255), (0, 70, 255)],
                               use_hsv=True, approx_hue=0, delta_hue=40)
    prepro1.save('DATA/OUT/res0.png')

    prepro2 = graph_preprocess(pil_convert('DATA/well_3_old.jpg'), [[0, 0, 0], [100, 100, 100]])
    prepro2.save('DATA/OUT/res1.png')

    prepro3 = graph_preprocess(pil_convert('DATA/well_4_old.jpg'), [(0, 120, 255), (0, 120, 255)],
                               use_hsv=True, approx_hue=0, delta_hue=40, denoise=2)
    prepro3.save('DATA/OUT/res2.png')

    prepro4 = graph_preprocess(pil_convert('DATA/well_4_old.jpg'), [[0, 0, 0], [100, 100, 100]])
    prepro4.save('DATA/OUT/res3.png')

    prepro5 = graph_preprocess(pil_convert('DATA/well_5.pdf'), [(0, 70, 255), (0, 70, 255)],
                               use_hsv=True, approx_hue=0, delta_hue=40)
    prepro5.save('DATA/OUT/res4.png')

    prepro6 = graph_preprocess(pil_convert('DATA/well_5.pdf'), [[100, 100, 100], [200, 200, 200]])

    prepro6.save('DATA/OUT/res5.png')
