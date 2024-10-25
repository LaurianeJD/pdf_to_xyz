import fitz
from PIL import Image
from io import BytesIO
import pytesseract

def image_to_text(image):
    config = '-c preserve_interword_spaces=1x1 --psm 6'
    return pytesseract.image_to_string(image, config=config)

def pdf_page_to_image(page, scale=8):
    pixmap = page.get_pixmap(matrix=fitz.Matrix(scale, scale))
    img_bytes = pixmap.tobytes("png")
    return Image.open(BytesIO(img_bytes))

def pdf_to_text(pdf_path, scale=8):
    with fitz.open(pdf_path) as doc:
        images = [pdf_page_to_image(doc.load_page(i), scale) for i in range(len(doc))]
    return [image_to_text(img) for img in images]