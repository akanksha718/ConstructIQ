import pytesseract

from PIL import Image


class OCRService:

    @staticmethod
    def extract(image_path):

        return pytesseract.image_to_string(

            Image.open(image_path)

        )