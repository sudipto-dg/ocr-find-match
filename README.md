# OCR Find Match

A Python tool to search for text terms in PDF files using both text layer extraction and OCR (Optical Character Recognition). Perfect for searching scanned PDFs or PDFs with embedded text layers, especially for non-Latin scripts like Bengali.

## Features

- 🔍 **Dual Search Strategy**: First attempts to extract text from PDF text layers, then falls back to OCR if needed
- 🌐 **Unicode Normalization**: Handles text matching properly across different Unicode encodings
- 📄 **Multi-Page Support**: Searches through all pages in PDF files
- 📝 **Context Snippets**: Shows surrounding text when matches are found
- 🎯 **Batch Processing**: Processes all PDFs in a specified folder

## Requirements

- Python 3.6+
- [Poppler](https://poppler.freedesktop.org/) (required by `pdf2image` for converting PDF pages to images)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) (for OCR functionality)
- Bengali language pack for Tesseract (for searching Bengali text)

## Installation

1. Clone or download this repository:
```bash
git clone <repository-url>
cd ocr-find-match
```

2. Install Python dependencies:
```bash
pip install pdfplumber pytesseract pdf2image
```

3. Install Poppler (required for `pdf2image`):
   - **Windows**: Download from [poppler-windows releases](https://github.com/oschwartz10612/poppler-windows/releases/) and add the `bin` folder to your system PATH, or extract and note the path for configuration
   - **macOS**: `brew install poppler`
   - **Linux**: `sudo apt-get install poppler-utils` (Ubuntu/Debian) or `sudo yum install poppler-utils` (CentOS/RHEL)

4. Install Tesseract OCR:
   - **Windows**: Download from [GitHub releases](https://github.com/UB-Mannheim/tesseract/wiki) and install
   - **macOS**: `brew install tesseract`
   - **Linux**: `sudo apt-get install tesseract-ocr` (Ubuntu/Debian) or `sudo yum install tesseract` (CentOS/RHEL)

5. Install Bengali language pack for Tesseract:
   - **Windows**: Download `ben.traineddata` from [tessdata](https://github.com/tesseract-ocr/tessdata) and place it in `C:\Program Files\Tesseract-OCR\tessdata\`
   - **macOS/Linux**: Usually included with Tesseract installation, or download from tessdata repository

6. (Optional) Configure paths in `script.py` if they're not in your system PATH:
   - **Tesseract path** (if needed):
```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```
   - **Poppler path** (if needed, for Windows):
```python
from pdf2image import convert_from_path
# Add this before using convert_from_path:
# convert_from_path(pdf_path, poppler_path=r"C:\path\to\poppler\bin")
```

## Usage

1. Place your PDF files in a `pdf` folder (or update `FOLDER_PATH` in `script.py`)

2. Update the search term in `script.py`:
```python
SEARCH_TERM = "বাংলা"  # Change this to your desired search term
```

3. Run the script:
```bash
python script.py
```

## Configuration

Edit the following variables in `script.py`:

- `FOLDER_PATH`: Path to the folder containing PDF files (default: `"./pdf"`)
- `SEARCH_TERM`: The text term to search for (default: `"বাংলা"`)
- `pytesseract.pytesseract.tesseract_cmd`: Path to Tesseract executable (uncomment and set if needed)

## How It Works

1. **Text Layer Extraction**: First attempts to extract text directly from PDF text layers using `pdfplumber`
2. **OCR Fallback**: If no matches are found, converts PDF pages to images and uses Tesseract OCR to extract text
3. **Unicode Normalization**: Normalizes text using NFC (Canonical Composition) to ensure consistent matching
4. **Context Display**: Shows a snippet of surrounding text (30 characters on each side) when a match is found

## Example Output

```
✅ Found in document1.pdf (text layer), page 3: ...some context বাংলা more context...
✅ Found in document2.pdf (OCR), page 1: ...some context বাংলা more context...
❌ Not found in document3.pdf

✨ Search complete
```

## Notes

- OCR processing is slower than text layer extraction but necessary for scanned PDFs
- The script searches all PDFs in the specified folder sequentially
- Unicode normalization ensures matches work across different text encodings
- For best OCR results, ensure PDFs have good image quality (200 DPI is used by default)

## License

See LICENSE file for details.