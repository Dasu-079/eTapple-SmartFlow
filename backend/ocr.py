import pytesseract
from PIL import Image
import fitz

def get_text(path):
    if path.lower().endswith(".pdf"):
        doc = fitz.open(path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    else:
        return pytesseract.image_to_string(Image.open(path))
