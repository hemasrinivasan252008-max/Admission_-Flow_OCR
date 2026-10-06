import pytesseract
import re
import shutil

from PIL import Image, ImageOps


# =========================================================
# TESSERACT CONFIGURATION
# =========================================================

# Windows
windows_tesseract = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# Check Windows installation
if shutil.which("tesseract"):

    pytesseract.pytesseract.tesseract_cmd = (
        shutil.which("tesseract")
    )

else:

    pytesseract.pytesseract.tesseract_cmd = (
        windows_tesseract
    )


# =========================================================
# OCR TEXT EXTRACTION
# =========================================================

def extract_text(image_file):

    image = Image.open(image_file)

    # Convert to grayscale
    image = image.convert("L")

    # Improve contrast
    image = ImageOps.autocontrast(image)

    # Increase image size
    image = image.resize(
        (
            image.width * 2,
            image.height * 2
        )
    )

    # OCR
    text = pytesseract.image_to_string(
        image,
        config="--psm 3"
    )

    return text


# =========================================================
# MARKSHEET DETAILS
# =========================================================

def extract_marksheet_details(text):

    details = {}

    # Date of Birth
    dob_match = re.search(
        r"DATE OF BIRTH.*?(\d{2}/\d{2}/\d{4})",
        text,
        re.IGNORECASE | re.DOTALL
    )

    if dob_match:

        details["date_of_birth"] = (
            dob_match.group(1)
        )

    # Permanent Register Number
    reg_match = re.search(
        r"PERMANENT REGISTER NUMBER.*?(\d{10})",
        text,
        re.IGNORECASE | re.DOTALL
    )

    if reg_match:

        details["register_number"] = (
            reg_match.group(1)
        )

    return details
