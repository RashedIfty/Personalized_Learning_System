import os
import pickle
from sqlalchemy.orm import Session
from fastapi import HTTPException
from PyPDF2 import PdfReader
from keybert import KeyBERT
from app.models.book import Book

# Additional imports for OCR fallback using PyMuPDF and EasyOCR
import fitz  # PyMuPDF
import numpy as np
import easyocr

# Define central data storage paths
DATA_FOLDER = "data"
BOOKS_FOLDER = os.path.join(DATA_FOLDER, "books")
EMBEDDINGS_FOLDER = os.path.join(DATA_FOLDER, "embeddings")
MAX_FILE_SIZE = 200 * 1024 * 1024  # 200MB

# Ensure directories exist
os.makedirs(BOOKS_FOLDER, exist_ok=True)
os.makedirs(EMBEDDINGS_FOLDER, exist_ok=True)

def save_pdf_file(file, file_path):
    """Saves the uploaded PDF file in chunks to avoid memory overload."""
    try:
        with open(file_path, "wb") as f:
            for chunk in file.file:
                f.write(chunk)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

def extract_text_from_pdf(pdf_path, ocr_threshold=100):
    """
    Extracts text from a PDF file.
    1. Tries to extract text using PyPDF2.
    2. If the extracted text is shorter than ocr_threshold, falls back to OCR:
       - Uses PyMuPDF (fitz) to render PDF pages to images.
       - Uses EasyOCR to extract text from those images.
    """
    text = ""
    try:
        pdf_reader = PdfReader(pdf_path)
        max_pages = min(len(pdf_reader.pages), 500)
        for i in range(max_pages):
            page_text = pdf_reader.pages[i].extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        # If PyPDF2 extraction fails, set text to empty to force OCR fallback
        text = ""
    
    if len(text.strip()) < ocr_threshold:
        try:
            # Open the PDF using PyMuPDF
            doc = fitz.open(pdf_path)
            reader = easyocr.Reader(['en'], gpu=False)
            ocr_text = ""
            for page in doc:
                # Render page to a pixmap (image)
                pix = page.get_pixmap()
                # Create a numpy array from pixmap samples
                img_array = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
                # If the image has an alpha channel, remove it
                if pix.n >= 4:
                    img_array = img_array[:, :, :3]
                # Use EasyOCR to extract text
                result = reader.readtext(img_array, detail=0, paragraph=True)
                ocr_text += " ".join(result) + "\n"
            return ocr_text.strip()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"OCR extraction failed: {str(e)}")
    
    if not text.strip():
        raise HTTPException(status_code=400, detail="Failed to extract text from PDF. The file may be empty or not text-based.")

    return text.strip()

def extract_keywords(text, num_keywords=10):
    """Extracts key topics from the text using KeyBERT."""
    kw_model = KeyBERT()
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1,2), stop_words='english', top_n=num_keywords)
    return [kw[0] for kw in keywords if kw]

def save_embeddings_to_file(embedding_path, embeddings):
    """Save embeddings as a file in `data/embeddings/`."""
    try:
        with open(embedding_path, "wb") as f:
            pickle.dump(embeddings, f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving embeddings file: {str(e)}")

def store_pdf_in_db(db: Session, filename: str, text_content: str, embeddings: list, user_id: int):
    """Stores the book, its embeddings, and the user ID in the database."""
    new_book = Book(
        filename=filename,
        text_content=text_content,
        embedding=pickle.dumps(embeddings),
        user_id=user_id
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

def get_first_book_text(db: Session):
    """Retrieve text from the first uploaded book PDF in the database."""
    book = db.query(Book).order_by(Book.uploaded_at.asc()).first()
    if not book:
        return None
    return book.text_content

def list_uploaded_books(db: Session, user_id: int):
    """List all books uploaded by a specific user."""
    books = db.query(Book).filter(Book.user_id == user_id).order_by(Book.uploaded_at.desc()).all()
    return [{"id": book.id, "filename": book.filename, "uploaded_at": book.uploaded_at} for book in books]
