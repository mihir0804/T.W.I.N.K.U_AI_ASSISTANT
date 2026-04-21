import os
try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

try:
    import docx
except ImportError:
    docx = None

from app import resolve_path 

MAX_CHARS = 10000

def extract_from_pdf(filepath: str) -> str:
    if not PyPDF2:
        return "[Error: PyPDF2 library not installed.]"
        
    text = ""
    try:
        with open(filepath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                if len(text) > MAX_CHARS:
                    break
        return text[:MAX_CHARS]
    except Exception as e:
        return f"[Error reading PDF: {str(e)}]"

def extract_from_docx(filepath: str) -> str:
    if not docx:
        return "[Error: python-docx library not installed.]"
        
    text = ""
    try:
        doc = docx.Document(filepath)
        for para in doc.paragraphs:
            text += para.text + "\n"
            if len(text) > MAX_CHARS:
                break
        return text[:MAX_CHARS]
    except Exception as e:
        return f"[Error reading DOCX: {str(e)}]"

def extract_from_txt(filepath: str) -> str:
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
            return file.read(MAX_CHARS)
    except Exception as e:
        return f"[Error reading TXT: {str(e)}]"

def read_document(location_hint: str, filename: str) -> str:
    """Reads up to 10,000 characters from a PDF, DOCX, or TXT file."""
    base_path = resolve_path(location_hint)
    full_path = os.path.join(base_path, filename)
    
    if not os.path.exists(full_path):
        import glob
        base_name = filename.split('.')[0] if '.' in filename else filename
        search_pattern = os.path.join(base_path, f"*{base_name}*.*")
        matches = glob.glob(search_pattern)
        if matches:
            full_path = matches[0] 
        else:
            return f"Boss, I couldn't find any document related to '{filename}' in your {base_path}. Are you sure it's located there?"
            
    ext = full_path.lower().split('.')[-1]
    
    if ext == 'pdf':
        text = extract_from_pdf(full_path)
    elif ext in ['docx', 'doc']:
        text = extract_from_docx(full_path)
    elif ext in ['txt', 'md', 'csv', 'json', 'log']:
        text = extract_from_txt(full_path)
    else:
        return f"I'm sorry Boss, but I don't know how to read files with a .{ext} extension just yet!"
        
    if not text.strip():
        text = "[The document appears to be entirely empty or solely composed of unreadable images.]"
        
    return f"===== BEGIN EXTRACTED DOCUMENT TEXT for {filename} =====\n{text}\n===== END EXTRACTED TEXT ====="
