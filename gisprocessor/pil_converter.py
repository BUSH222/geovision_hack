from PIL import Image
import os
import fitz


def pil_convert(path, dpi=300):
    ext = os.path.splitext(path)[-1].lower()
    if ext == '.png' or ext == '.jpg':
        return Image(path)
    elif ext == '.pdf':
        doc = fitz.open(path)
        page = doc.load_page(0)
        pixmap = page.get_pixmap(dpi=dpi)
        width, height = pixmap.width, pixmap.height
        img_bytes = pixmap.samples
        return Image.frombytes("RGB", (width, height), img_bytes)
    else:
        return None


if __name__ == "__main__":
    print(pil_convert('DATA/well_5.pdf'))
    
