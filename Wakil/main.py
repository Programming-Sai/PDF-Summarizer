import fitz  # PyMuPDF
import os


def extract_highlighted_text(pdf_file):
    """
    Extracts and prints all highlighted text from a given PDF file.

    Args:
        pdf_file (str): Path to the input PDF file.
    """
    # Open the PDF file
    doc = fitz.open(pdf_file)

    print("Extracting highlighted text from the PDF...\n")
    
    # Iterate through all pages in the PDF
    for page_num in range(doc.page_count):
        page = doc[page_num]  # Get the current page
        print(f"Page {page_num + 1}:")
        
        # Iterate through annotations on the page
        for annot in page.annots():
            # Check if the annotation is a highlight
            if annot.type[0] == 8:  # 8 indicates a highlight annotation
                # Extract the quads (highlighted text coordinates)
                quads = annot.vertices
                text = ""
                for i in range(0, len(quads), 4):  # Each quad has 4 points
                    # Extract the highlighted text within the quad
                    rect = fitz.Rect(quads[i:i + 4])
                    text += page.get_text("text", clip=rect) + " "
                print(f"  Highlighted text: {text.strip()}")
        
        print("\n" + "-" * 50)

    # Close the document
    doc.close()

# Example usage
extract_highlighted_text(os.path.join(os.getcwd(), "page_29.pdf"))
