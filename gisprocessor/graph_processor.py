from pil_converter import pil_convert


def process_image(img, color_range):
    (R1, G1, B1), (R2, G2, B2) = color_range
    data = img.load()

    # Iterate over each pixel
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = data[x, y]

            # Check if the pixel color is outside the range
            if not(R1 <= r <= R2 and G1 <= g <= G2 and B1 <= b <= B2) or (r < g+20 and r < b+20):
                # Change the color to black
                data[x, y] = (0, 0, 0)

    return img


process_image(pil_convert('DATA/well_3_old.jpg'), [[130, 70, 70], [200, 160, 160]]).save('DATA/OUT/res.png')
