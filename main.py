from extractHeadings import getHeadings, getImageCaption
from extractHighlightedText import getHighlightedText, getTextFromPDFAsParagraphs
from extractImages import getImages
from utils import *
from thefuzz import fuzz, process




 
def get_summary(doc, print_results=False, include_images=False, images_folder="images/images", show_progress=True, isPDF=True, threshold=50):
    results = []

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


        

        if include_images:
            while True:
                cv2.imshow('Original Image', img)
                key = cv2.waitKey(1) & 0xFF
                if key == 27 or key in (ord('q'), ord('x')):  # Press ESC to close or click on an option
                    break
            getImages(img, show_contours=False, show_result=False)
            possible_captions = getImageCaption(actual_page_text_for_headings)
            images, paths = load_images_from_folder(images_folder)
            image_path_result = display_images_grid(images, paths, close_image_window=False, pdf_image_path='')
            image_caption_result = display_strings(possible_captions, window_name="Select The Correct Caption: ", close_caption_window = False, pdf_caption_text = '')


        # Match headings with the highlighted text
        headings = getHeadings(actual_page_text_for_headings)
        displayResult("PAGE HEADINGS", headings) if print_results else None

        for index, match in enumerate(highlight_matches):
            for heading in headings:
                if heading in match:
                        highlight_matches[index] = match.replace(match[ match.find(heading) : match.find(heading)+len(heading) ], "") # Replace current Heading Sentence with sentence without heading.
                        highlight_matches.insert(index, f"\n\n\n####### {heading} ##############\n\n\n") # Insert the New Heading
        highlight_matches_count = get_count(highlight_matches, highlight_matches_count)

        # Append page results to the main results list
        results.append(f"Page {page_num}:\n")
        results.extend(highlight_matches)
        if include_images:
            results.append(image_path_result)
            results.append(image_caption_result)

        results.append(f"\n\nOriginal Text Length {original_count}\n'      |      \nHighlighted Text Count: {highlight_matches_count}")
        results.append("\n\n==============================================================\n\n")

        print(f"[INFO] Page {page_num} of {doc.page_count}: Extraction completed with {highlight_matches_count} highlights from {original_count} original text and {len(headings)} headings.\n") if show_progress else None
        displayResult("RESULT", results) if print_results else None
    
    
    
        cv2.destroyAllWindows()
    return results




path = "test_pdfs/pages_28_to_31.pdf"
# path = "test_pdfs/page_28.pdf"
# path = "test_pdfs/page_31.pdf"

image_folder = "images/images"


doc = fitz.open(path)

# Example results
results = get_summary(doc, include_images=True, images_folder=image_folder, print_results=False, show_progress=True, isPDF=True, threshold=60)


# saveText(results, "FINAL_RESULT.txt")
save_to_pdf(results, "test_pdfs/OUTPUT.pdf")







doc.close()