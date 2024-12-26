from extractHeadings import getHeadings, getImageCaption
from extractHighlightedText import getHighlightedText, getTextFromPDFAsParagraphs
from extractImages import getImages
from utils import fitz, pdf_page_to_image, saveText, re
from thefuzz import fuzz, process
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.pagesizes import letter





def displayResult(title, iterable):
    print(f"\n\n\n\n\n\n\n\n{title}: \n\n")
    for i in iterable: 
        print(i, end="\n\n")

def get_count(iterable, counter):
    for i in iterable:
        counter += len(i)
    return counter


def text_save(print_results=False, show_progress=True, save_as_text=True, threshold=50):
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
        highlight_matches = list(dict.fromkeys([match for match, score in highlight_matches if score >= threshold]))
        highlight_matches = sorted(highlight_matches, key=lambda x: actual_page_text.index(x))
        displayResult("HIGHLIGHTED TEXT MATCHES", highlight_matches) if print_results else None

        # Match headings with the highlighted text
        headings = getHeadings(actual_page_text_for_headings)
        displayResult("PAGE HEADINGS", headings) if print_results else None

        for index, match in enumerate(highlight_matches):
            seen_headings = []
            for heading in headings:
                if heading in match:
                    if heading not in seen_headings:
                        highlight_matches[index] = match.replace(match[ match.find(heading) : match.find(heading)+len(heading) ], "") # Replace current Heading Sentence with sentence without heading.
                        highlight_matches.insert(index, f"\n\n\n####### {heading} ##############\n\n\n") # Insert the New Heading

                        seen_headings.append(heading)


                    # Get that heading
                    # heading_acquired  = 

        highlight_matches_count = get_count(highlight_matches, highlight_matches_count)

        # Append page results to the main results list
        results.append(f"Page {page_num}:\n")
        results.extend(highlight_matches)
        results.append(f"\n\nOriginal Text Length {original_count}\n{'      |     ' if not save_as_text else ''}Highlighted Text Count: {highlight_matches_count}")
        results.append("\n\n==============================================================\n\n")

        print(f"[INFO] Page {page_num} of {doc.page_count}: Extraction completed with {highlight_matches_count} highlights from {original_count} original text and {len(headings)} headings.\n") if show_progress else None

    # Save the final results
    if save_as_text:
        saveText(results, "FINAL_RESULT.txt")
        displayResult("RESULT", results) if print_results else None
        doc.close()
    else:
        doc.close()
        return results




def create_header_footer(elements, item, is_footer=False, page_width=letter[0], page_height=letter[1]):
    # If it's a header or a footer
    header_style = ParagraphStyle(
        name="Header",
        fontName="Helvetica",
        fontSize=10,
        textColor=colors.grey,
        spaceAfter=6,
        alignment=0
    )

    footer_style = ParagraphStyle(
        name="Footer",
        fontName="Helvetica",
        fontSize=10,
        textColor=colors.grey,
        spaceBefore=6,
        alignment=2
    )
    
    if is_footer:
        # Add footer with page number or other footer text
        elements.append(Spacer(1, 12))  # Spacer before footer
        elements.append(Paragraph(item, footer_style))  
        elements.append(Spacer(1, 12))  

    else:
        # Add header
        elements.append(Spacer(1, 12))  
        elements.append(Paragraph(item, header_style))  
        elements.append(Spacer(1, 12))  





def save_to_pdf(results, filename):
    # Create the PDF document
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []

    # Get default styles
    styles = getSampleStyleSheet()

    # Custom Heading style (using a large font and bold)
    heading_style = ParagraphStyle(
        name="Heading1",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=15,
        textColor=colors.darkblue,
        spaceAfter=12,
        # alignment=1,  # Centered
        alignment=0,  # Left Centered ?
    )

    # Custom normal text style
    normal_style = ParagraphStyle(
        name="Normal",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        textColor=colors.black,
        spaceAfter=6,
    )

    bullet_style = ParagraphStyle(
        name="Bullet",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        textColor=colors.black,
        spaceAfter=10,
        bulletFontName="Helvetica",
        bulletFontSize=50,
        bulletColor=colors.black,
        leftIndent=25,
        bulletSymbol="◉",
    )

    # Iterate over the results and add them as paragraphs
    for item in results:
        # Check if the item is a heading or normal text
        if "#######" in item:
            heading = item.split("#######")[1].split("##############")[0].strip()
            # Add heading with custom style
            elements.append(Paragraph(heading, heading_style))
        else:
            # Add normal text with the normal style
            # elements.append(Paragraph(item, normal_style))

            if item == "\n\n==============================================================\n\n":
                elements.append(Spacer(1, 12))  # Adds space before the line

                # Add a horizontal line
                line = HRFlowable(width="100%", color=colors.black, thickness=1)
                elements.append(line)
                # Add some space after the horizontal line
                elements.append(Spacer(1, 12)) 
                continue
            elif re.match(r"^Page \d+:$", item):
                create_header_footer(elements, item)
                continue

            elif re.match(r"\n\nOriginal Text Length \d+\n      |     Highlighted Text Count: \d+", item):
                create_header_footer(elements, item, is_footer=True)
                continue

            elements.append(Paragraph(f"◉   {item}", bullet_style))


    # Build the PDF
    doc.build(elements)

# Example results
results = text_save(print_results=False, show_progress=False, save_as_text=False)


# Save to PDF
save_to_pdf(results, "test_pdfs/OUTPUT.pdf")




# TODO Fix spaces here             elif re.match(r"\n\nOriginal Text Length \d+\n      |     Highlighted Text Count: \d+", item):
# TODO Fix headings so that only headings are added at the top and the rest is placed at the bottom.