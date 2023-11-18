import os
from PyPDF2 import PdfReader
import docx2txt
import html2text

def pdf_to_text(path: str) -> str:
    reader = PdfReader(path) 
    text = ""
    for page in reader.pages:
        text += page.extract_text() 
    return text

def docx_to_text(path: str) -> str:
    text = docx2txt.process(path)
    return text

def html_to_text(path: str) -> str:
    h = html2text.HTML2Text()
    h.ignore_links = False
    with open(path) as f:
        input_html = f.read()
    text = h.handle(input_html)
    return text

def txt_to_text(path: str) -> str:
    with open(path) as f:
        text = f.read()
    return text

def get_extractor(ext: str) -> callable:
    ext = ext.lower()
    _map = {
        ".pdf": pdf_to_text,
        ".docx": docx_to_text,
        ".doc": docx_to_text,
        ".html": html_to_text,
        ".txt": txt_to_text
    }

    extractor = _map.get(ext)
    if extractor is None:
        raise Exception(f"Extraction from file with extension '{ext}' not supported")
    
    return extractor

def get_extension(path: str) -> str:
    return os.path.splitext(path)[1]

def extract_text(path: str, ext=None) -> str:
    if ext is None:
        ext = get_extension(path)

    extractor = get_extractor(ext)
    return extractor(path)


if __name__ == "__main__":
    import sys
    path = sys.argv[1]
    text = extract_text(path)
    with open("out.txt", 'w') as f:
        f.write(text)