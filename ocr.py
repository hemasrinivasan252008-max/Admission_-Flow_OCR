import pytesseract
import re

from PIL import Image, ImageOps


# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_text(image_file):

    image = Image.open(image_file)

    image = image.convert("L")

    image = ImageOps.autocontrast(image)

    image = image.resize(
        (
            image.width * 2,
            image.height * 2
        )
    )

    text = pytesseract.image_to_string(
        image,
        config="--psm 3"
    )

    return text


def extract_marksheet_details(text):

    details = {}

    dob_match = re.search(
        r"DATE OF BIRTH.*?(\d{2}/\d{2}/\d{4})",
        text,
        re.IGNORECASE | re.DOTALL
    )

    if dob_match:
        details["date_of_birth"] = dob_match.group(1)

    reg_match = re.search(
        r"PERMANENT REGISTER NUMBER.*?(\d{10})",
        text,
        re.IGNORECASE | re.DOTALL
    )

    if reg_match:
        details["register_number"] = reg_match.group(1)

    return details
