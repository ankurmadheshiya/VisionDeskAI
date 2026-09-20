import os
# pyrefly: ignore [missing-import]
import fitz  # PyMuPDF library, imported as fitz

def extract_text_from_pdf(file_path: str) -> list[dict]:
    """
    Extracts text from each page of a PDF document using PyMuPDF.

    This function opens a PDF file from the specified path, iterates through
    all of its pages, extracts raw text content from each page, and returns
    a list of dictionaries containing page numbers and their corresponding text.

    Args:
        file_path (str): The absolute or relative path to the PDF file.

    Returns:
        list[dict]: A list of dictionaries. Each dictionary has two keys:
            - "page_number" (int): The 1-based index of the page.
            - "text" (str): The full text extracted from that page.

    Raises:
        FileNotFoundError: If the specified PDF file does not exist.
        Exception: If PyMuPDF fails to open or parse the PDF document.
    """
    # Verify that the input file path exists before attempting to open it
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF file not found at: {file_path}")

    extracted_pages = []
    
    try:
        # Open the PDF document using PyMuPDF
        doc = fitz.open(file_path)
        
        # Iterate through each page of the document
        for page_num in range(len(doc)):
            # Load the individual page object
            page = doc.load_page(page_num)
            
            # Extract plain text from the page
            page_text = page.get_text()
            
            # Clean up the text: strip leading/trailing whitespace
            clean_text = page_text.strip() if page_text else ""
            
            # Store the extracted page details (1-based indexing for page numbers)
            extracted_pages.append({
                "page_number": page_num + 1,
                "text": clean_text
            })
            
        # Close the document object to release system resources
        doc.close()
        
    except Exception as e:
        # Handle and re-raise any parsing exceptions with descriptive error message
        raise Exception(f"Failed to parse PDF document at {file_path}. Error: {str(e)}")

    return extracted_pages
