import io
from pypdf import PdfReader

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extracts and cleans text from PDF byte content.
    """
    try:
        pdf_file = io.BytesIO(pdf_bytes)
        reader = PdfReader(pdf_file)
        full_text = []
        
        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                full_text.append(text)
                
        cleaned_text = "\n".join(full_text).strip()
        if not cleaned_text:
            raise ValueError("No text could be extracted from the PDF. It might be scanned or image-only.")
            
        return cleaned_text
    except Exception as e:
        raise ValueError(f"Failed to parse PDF file: {str(e)}")
