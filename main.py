from extractHeadings import getHeadings, getImageCaption
from extractHighlightedText import getHighlightedText, getTextFromPDFAsParagraphs
from extractImages import getImages
from utils import fitz, pdf_page_to_image, saveText
from thefuzz import fuzz, process


def displayResult(title, iterable):
    print(f"\n\n\n\n\n\n\n\n{title}: \n\n")
    for i in iterable: 
        print(i, end="\n\n")

def get_count(iterable, counter):
    for i in iterable:
        counter += len(i)
    return counter


def main(print_results=False, show_progress=True):
    results = []

    # First load the PDF document
    doc = fitz.open("test_pdfs/pages_28_to_31.pdf")
    # doc = fitz.open("test_pdfs/page_28.pdf")

    # Process each page
    for page_num in range(1, doc.page_count+1):
        print(f"\n[INFO] Processing page {page_num} of {doc.page_count}...") if show_progress else None


        highlight_matches = []  # Reset for each page
        original_count = 0
        highlight_matches_count = 0

        # Acquire an image version of the page
        img = pdf_page_to_image(doc, page_num)

        # Get the main text from the given page, for reference
        actual_page_text, actual_page_text_for_headings = getTextFromPDFAsParagraphs(doc, page_num)
        original_count = get_count(actual_page_text, original_count)
        displayResult("ORIGINAL TEXT", actual_page_text) if print_results else None

        # Extract highlighted text on the page
        hText = getHighlightedText(doc, page_num, img, show_result_image=False, save_extracted_text=False)
        displayResult("HIGHLIGHTED TEXT", hText) if print_results else None

        # Perform fuzzy matching between highlights and actual text
        for text in hText:
            highlight_matches.extend(process.extract(text, actual_page_text, scorer=fuzz.token_sort_ratio))

        # Filter and sort matches
        highlight_matches = list(dict.fromkeys([match for match, score in highlight_matches if score >= 36]))
        highlight_matches = sorted(highlight_matches, key=lambda x: actual_page_text.index(x))
        displayResult("HIGHLIGHTED TEXT MATCHES", highlight_matches) if print_results else None

        # Match headings with the highlighted text
        headings = getHeadings(actual_page_text_for_headings)
        displayResult("PAGE HEADINGS", headings) if print_results else None

        for index, match in enumerate(highlight_matches):
            for heading in headings:
                if heading in match:
                    highlight_matches[index] = match.replace(heading, f"\n\n\n####### {heading} ##############\n\n\n")

        highlight_matches_count = get_count(highlight_matches, highlight_matches_count)

        # Append page results to the main results list
        results.append(f"Page {page_num}:\n")
        results.extend(highlight_matches)
        results.append(f"\n\nOriginal Text Length {original_count}\nHighlighted Text Count: {highlight_matches_count}")
        results.append("\n\n==============================================================\n\n")

        print(f"[INFO] Page {page_num} of {doc.page_count}: Extraction completed with {highlight_matches_count} highlights from {original_count} original text and {len(headings)} headings.\n") if show_progress else None

    # Save the final results
    saveText(results, "FINAL_RESULT.txt")
    displayResult("RESULT", results) if print_results else None

    doc.close()



main(print_results=False, show_progress=False)