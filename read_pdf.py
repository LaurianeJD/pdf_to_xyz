import PyPDF2

def read_pdf(pdf_path:str):
    """Read PDF and return a string"""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text