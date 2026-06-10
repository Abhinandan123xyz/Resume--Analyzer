import fitz  # PyMuPDF

def extract_text_from_pdf(uploaded_file):
    uploaded_file.seek(0)  # reset file pointer
    bytes_data = uploaded_file.read()
    doc = fitz.open(stream=bytes_data, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text.strip()