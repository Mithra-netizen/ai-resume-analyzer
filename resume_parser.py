try:
    import PyPDF2
except ImportError:
    try:
        import pypdf as PyPDF2
    except ImportError:
        PyPDF2 = None

try:
    from docx import Document
except ImportError:
    Document = None


def extract_text_from_pdf(file):
    if PyPDF2 is None:
        return "PyPDF2 is not installed in the active environment. Please run inside the project virtual environment (venv)."

    text = ""

    reader = PyPDF2.PdfReader(file)

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def extract_text_from_docx(file):
    if Document is None:
        return "python-docx is not installed in the active environment. Please run inside the project virtual environment (venv)."

    document = Document(file)

    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return text



def extract_resume_text(file):
    file_name = file.name.lower()

    if file_name.endswith(".pdf"):
        return extract_text_from_pdf(file)

    elif file_name.endswith(".docx"):
        return extract_text_from_docx(file)

    else:
        return "Unsupported file format."