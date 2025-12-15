import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import os

def extract_images_and_ocr(pdf_path, image_dir="data/images"):
    os.makedirs(image_dir, exist_ok=True)
    doc = fitz.open(pdf_path)

    ocr_text = ""

    for page_num, page in enumerate(doc):
        images = page.get_images(full=True)
        for img_index, img in enumerate(images):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)

            if pix.n - pix.alpha >= 4:
                pix = fitz.Pixmap(fitz.csRGB, pix)

            img_path = f"{image_dir}/page{page_num}_img{img_index}.png"
            pix.save(img_path)

            try:
                text = pytesseract.image_to_string(Image.open(img_path))
                ocr_text += text + "\n"
            except Exception:
                pass

    return ocr_text
