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


def graph_preprocess(image, color_range=[], use_hsv=False, approx_hue=0, delta_hue=40):
    if not use_hsv:
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
    else:
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2HSV)
        (G1, G2), (B1, B2) = (70, 255), (70, 255)
        hue1_low, hue1_high, hue2_low, hue2_high = split_hue(approx_hue, delta_hue)
        print(split_hue(approx_hue, delta_hue))
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
        image[mask_inv > 0] = [200, 255, 255]
        return Image.fromarray(image)


if __name__ == "__main__":
    prepro = graph_preprocess(pil_convert('DATA/well_3_old.jpg'), use_hsv=True, approx_hue=0, delta_hue=40)
    prepro.save('DATA/OUT/res0.png')

    # prepro2 = process_image(pil_convert('DATA/well_3_old.jpg'), [[0, 0, 0], [100, 100, 100]])
    # prepro2.save('DATA/OUT/res1.png')
