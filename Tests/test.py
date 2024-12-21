# -*- coding: utf-8 -*-

from typing import List, Tuple
import fitz  # install with 'pip install pymupdf'


def _parse_highlight(annot: fitz.Annot, wordlist: List[Tuple[float, float, float, float, str, int, int, int]]) -> str:
    """
    Parse the highlighted annotation and extract the highlighted text.
    """
    points = annot.vertices
    quad_count = int(len(points) / 4)
    sentences = []
    for i in range(quad_count):
        # Get the rectangle of the highlighted part
        r = fitz.Quad(points[i * 4 : i * 4 + 4]).rect

        # Find words that intersect with the highlight's rectangle
        words = [w for w in wordlist if fitz.Rect(w[:4]).intersects(r)]
        sentences.append(" ".join(w[4] for w in words))
    
    # Join the sentences to form the full text of the highlight
    sentence = " ".join(sentences)
    return sentence


def handle_page(page) -> List[str]:
    """
    Extract all highlighted text from the given page.
    """
    wordlist = page.get_text("words")  # List of words on the page
    wordlist.sort(key=lambda w: (w[3], w[0]))  # Sort words by y, then x coordinates

    highlights = []
    annot = page.first_annot
    while annot:
        if annot.type[0] == 8:  # Check for highlight annotations (type 8)
            highlights.append(_parse_highlight(annot, wordlist))
        annot = annot.next  # Move to the next annotation
    
    return highlights


def save_txt(highlights: list, filepath: str):
    """
    Save the extracted highlighted text to a text file.
    """
    filename = filepath.split("/")[-1]
    lines = highlights
    
    with open(f'{filename}_highlights.txt', 'w') as f:
        for line in lines:
            f.write("- " + line + '\n')


def main(filepath: str, page_num) -> List[str]:
    """
    Main function to process the PDF and extract highlighted text.
    """
    doc = fitz.open(filepath)

    # Ensure the page number is within the document range
    if page_num >= len(doc) or page_num < 0:
        print("Invalid page number!")
        return []

    page = doc.load_page(page_num)  # Load the specific page by page number

    highlights = handle_page(page)
    
    # Optionally save the extracted highlights to a text file
    save_txt(highlights, filepath)
    
    return highlights


# Example usage:
if __name__ == "__main__":
    pdf_path = '/Users/mac/Downloads/OPERATING SYSTEMS.pdf'  # Change this to your PDF path
    page_number = 27  # Change this to the specific page number you want (0-based index)

    highlights = main(pdf_path, page_number)
    # Print the extracted highlighted text
    for highlight in highlights:
        print(highlight)


# # Usage example
# book_path = '/Users/mac/Downloads/OPERATING SYSTEMS.pdf'
# all_text = extract_all_text_from_page(book_path, 26)
# print(all_text)
