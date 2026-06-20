import pdfplumber
import re
import pytesseract

from pdf2image import convert_from_path

# WINDOWS USERS
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

SKILLS = [

    "python",
    "java",
    "c++",
    "sql",

    "excel",
    "power bi",

    "machine learning",
    "deep learning",
    "tensorflow",

    "flask",
    "django",

    "aws",
    "docker",
    "linux",

    "data analysis",
    "data visualization",

    "communication",
    "teamwork",
    "problem solving",

    "network security"
]


def extract_text(pdf_path):

    text = ""

    try:

        with pdfplumber.open(pdf_path) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

    except Exception as e:

        print("PDF Error:", e)

    # OCR FALLBACK

    if len(text.strip()) < 50:

        print("Running OCR...")

        try:

            images = convert_from_path(pdf_path)

            for image in images:

                ocr_text = pytesseract.image_to_string(
                    image
                )

                text += ocr_text

        except Exception as e:

            print("OCR Error:", e)

    return text


def clean_text(text):

    text = re.sub(
        r'http\S+',
        '',
        str(text)
    )

    text = re.sub(
        r'[^a-zA-Z ]',
        ' ',
        text
    )

    text = text.lower()

    return text


def extract_skills(text):

    text = text.lower()

    found = []

    for skill in SKILLS:

        if skill in text:

            found.append(skill)

    return list(set(found))


def extract_name(text):

    lines = text.split("\n")

    for line in lines[:10]:

        line = line.strip()

        if len(line) > 3 and len(line.split()) <= 4:

            return line

    return "Unknown Candidate"

def extract_email(text):

    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+'

    match = re.search(pattern,text)

    if match:
        return match.group()

    return "Not Found"

def extract_phone(text):

    pattern = r'\b\d{10}\b'

    match = re.search(pattern,text)

    if match:
        return match.group()

    return "Not Found"

def extract_education(text):

    education_keywords = [

        "b.tech",
        "btech",

        "b.e",
        "be",

        "m.tech",
        "mtech",

        "mba",

        "bca",
        "mca",

        "computer science",

        "information technology"

    ]

    text = text.lower()

    found = []

    for edu in education_keywords:

        if edu in text:
            found.append(edu)

    if found:
        return ", ".join(found)

    return "Not Found"

def calculate_score(skills):

    score = 0

    score += len(skills) * 10

    if "python" in skills:
        score += 10

    if "sql" in skills:
        score += 10

    if "machine learning" in skills:
        score += 20

    if "aws" in skills:
        score += 15

    if "docker" in skills:
        score += 15

    return min(score, 100)


def get_rating(score):

    if score >= 80:
        return "Excellent"

    elif score >= 60:
        return "Good"

    else:
        return "Needs Improvement"