import os
from PyPDF2 import PdfReader

def chunk_pdf(pdf_path, chunk_size=500):
    reader = PdfReader(pdf_path)
    all_text = ""
    for page in reader.pages:
        all_text += page.extract_text() or ""
    # Naive chunking by N characters
    return [all_text[i:i+chunk_size] for i in range(0, len(all_text), chunk_size)]

def chunk_kiit_docs(doc_dir):
    docs = []
    for fname in os.listdir(doc_dir):
        if fname.endswith(".pdf"):
            chunks = chunk_pdf(os.path.join(doc_dir, fname))
            for ch in chunks:
                docs.append({"text": ch, "source": fname})
                return docs
