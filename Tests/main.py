from PyPDF2 import PdfReader
import fitz


# book_path = "test_pdfs/OPERATING SYSTEMS.pdf"
book_path  = '/Users/mac/Downloads/OPERATING SYSTEMS.pdf'

page_number = 26



doc = fitz.open(book_path)

page = doc[page_number]

text_instances = page.get_text("dict")["blocks"]

def getHeadingsOnly(page_number):
    text_output = ''

    for block in text_instances:
        if "lines" in block:  # Check if the block contains lines
            for line in block["lines"]:
                for span in line["spans"]:
                    font_size = span.get("size", 0)  # Font size
                    color = span["color"]  # Font color
                    text = span["text"].strip()  # Extract text
                    
                    # Example heuristic: Identify headings by larger font size or distinct color
                    if font_size > 12 or color == -16732689:  # Adjust thresholds based on PDF structure
                        # print(f"Heading: {text} (Font size: {font_size}, Color: {color})")
                        text_output += text + '\n'
    return text_output


def getTextOnly (page_number):
    reader = PdfReader(book_path)

    if page_number < len(reader.pages):
        page = reader.pages[page_number]
        text = page.extract_text()
        return ('\n\n\n', text, '\n\n\n')
    else:
        return (f"Page {page_number + 1} doesn't exist")
    




def extract_highlighted_text_pymupdf(page_number):
    book_path = "test_pdfs/OPERATING SYSTEMS.pdf"
    doc = fitz.open(book_path)
    page = doc[page_number]
    highlights = []
    
    if page.annots():  # Check if there are any annotations
        for annot in page.annots():
            annot_type = annot.type[0]  # Get annotation type
            if annot_type == 8:  # Highlight type
                try:
                    # Extract quadpoints and the associated text
                    quadpoints = annot.vertices
                    rect = fitz.Quad(quadpoints).rect
                    text = page.get_text("text", clip=rect)
                    highlights.append(text.strip())
                except Exception as e:
                    print(f"Error extracting highlighted text on page {page_number + 1}: {e}")
    else:
        print(f"No highlights found on page {page_number + 1}.")
    
    return highlights

# Example usage:
highlights = extract_highlighted_text_pymupdf(page_number)
print(highlights)
