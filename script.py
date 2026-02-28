import os
import unicodedata
import pdfplumber
import pytesseract
from pdf2image import convert_from_path

# 📂 folder containing PDFs
FOLDER_PATH = "./pdf"
SEARCH_TERM = "বাংলা"

# Path to tesseract executable (adjust if needed)
# Example for Windows:
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Path to poppler executable (adjust if needed)
poppler_path = r"C:\Users\shovo\Downloads\poppler-25.12.0\Library\bin"

def normalize(text):
    """Normalize Unicode and collapse spaces."""
    return unicodedata.normalize("NFC", text).replace("\n", " ").replace("\r", " ").strip()

def snippet(text, term, radius=30):
    i = text.find(term)
    if i == -1:
        return ""
    return text[max(0, i - radius): i + len(term) + radius]

def search_pdf(pdf_path):
    found = False
    normalized_term = normalize(SEARCH_TERM)

    # Step 1: Try extracting text layer
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                text = page.extract_text() or ""
                norm_text = normalize(text)
                if normalized_term in norm_text:
                    print(f"✅ Found in {os.path.basename(pdf_path)} (text layer), page {page_num}: {snippet(norm_text, normalized_term)}")
                    found = True
    except Exception as e:
        print(f"⚠️ Error reading text layer in {pdf_path}: {e}")

    # Step 2: OCR fallback if nothing found
    if not found:
        try:
            images = convert_from_path(pdf_path, dpi=200, poppler_path=poppler_path)
            for page_num, img in enumerate(images, start=1):
                text = pytesseract.image_to_string(img, lang="ben")
                norm_text = normalize(text)
                if normalized_term in norm_text:
                    print(f"✅ Found in {os.path.basename(pdf_path)} (OCR), page {page_num}: {snippet(norm_text, normalized_term)}")
                    found = True
        except Exception as e:
            print(f"⚠️ OCR error in {pdf_path}: {e}")

    if not found:
        print(f"❌ Not found in {os.path.basename(pdf_path)}")

def main():
    files = [f for f in os.listdir(FOLDER_PATH) if f.lower().endswith(".pdf")]
    for file in files:
        search_pdf(os.path.join(FOLDER_PATH, file))
    print("\n✨ Search complete")

if __name__ == "__main__":
    main()
