from extractHeadings import getHeadings, getImageCaption
from extractHighlightedText import getHighlightedText, getTextFromPDFAsParagraphs
from extractImages import getImages
from utils import *
from thefuzz import fuzz, process
import argparse as ag
import sys



 
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




STATE_FILE = "state.tmp"

def save_state(pdf_path):
    with open(STATE_FILE, "w") as f:
        f.write(pdf_path)

def load_state():
    if not os.path.exists(STATE_FILE):
        raise ValueError("You must run the `init` command first.")
    with open(STATE_FILE, "r") as f:
        return f.read().strip()

def clear_state():
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)
        print("\nCurrent State Cleared\n")





# path = "test_pdfs/pages_28_to_31.pdf"
# path = "test_pdfs/page_28.pdf"
# path = "test_pdfs/page_31.pdf"

# image_folder = "images/images"



# # Example results
# results = get_summary(doc, include_images=True, images_folder=image_folder, print_results=False, show_progress=True, isPDF=True, threshold=60)


# # saveText(results, "FINAL_RESULT.txt")
# save_to_pdf(results, "test_pdfs/OUTPUT.pdf")


parser = ag.ArgumentParser(description='OS PDF Summarizer.')

sub_parser = parser.add_subparsers(dest='command', required=False, parser_class=ag.ArgumentParser)


init_parser = sub_parser.add_parser('init', help='Initialize with a PDF file path.')
init_parser.add_argument('pdf_file', type=str, help='Path to the PDF file.')
init_parser.add_argument('-d','--dont-persist-state', action='store_true', help='Determins if to persist the current state or not.')
init_parser.add_argument('-r','--reset-state', action='store_true', help='Determins if to reset the current state or not.')



summariser_parser = sub_parser.add_parser('summarize', help='Command to execute summarize, split or merge of a pdf.', description='Command to execute summarize, split or merge of a pdf.')


summariser_parser.add_argument('-i', '--include-images', action='store_true', help='Determines If images should be included in the pdf or docx result')
summariser_parser.add_argument('-f', '--images-folder', type=str, help='The path to the folder holding the images.')
summariser_parser.add_argument('-o', '--output-path', type=str, help='The path to save the result of the summarisation, if any')
summariser_parser.add_argument('-p', '--print-results', action='store_true', help='Determins if the result for the entire operation should be displayed or not.')
summariser_parser.add_argument('-s', '--show_progress', action='store_true', help='Determins If the current progress of the entire operations should be shown in the terminal or not.')
summariser_parser.add_argument('--pdf', action='store_true', help='Determins whether to save the work as a pdf or not')
summariser_parser.add_argument('--txt', action='store_true', help='Determins whether to save the work as a text file or not')
summariser_parser.add_argument('--docx', action='store_true', help='Determins whether to save the work as a word file or not')
summariser_parser.add_argument('-t', '--threshold', type=int, default=50, help='(0-100) Accuracy level for text summarization.')


args = parser.parse_args()

persist_state = True


if args.command == 'init':
    pdf_path = args.pdf_file
    if not os.path.exists(pdf_path):
        print(f"Error: File '{pdf_path}' does not exist.", file=sys.stderr)
        sys.exit(1)
    save_state(pdf_path)
    print(f"Initialized with PDF file: {pdf_path}")
    if args.dont_persist_state:
        persist_state = False
        print("Current State would Not be preserved" if not persist_state else "Current State would be preserved")
    elif args.reset_state:
        clear_state()



elif args.command == 'summarize':
        try:
            pdf_path = load_state()
        except ValueError as e:
            print(str(e), file=sys.stderr)
            sys.exit(1)
        include_images=False
        images_folder = "images/images"
        output_path = "test_pdfs/OUTPUT.pdf"
        print_results = False
        show_progress = True
        pdf = True
        txt = False
        docx = False
        threshold = 50
        if args.include_images:
            include_images = True
        if args.images_folder:
            images_folder = args.images_folder
        if args.output_path:
            output_path = args.output_path
        if args.print_results:
            print_results = True
        if args.show_progress:
            show_progress = False

        if args.txt:
            txt = True
            pdf = False  
        if args.docx:
            docx = True
            pdf = False  
        if not (pdf or txt or docx):
            pdf = True 

        # results = get_summary(doc, include_images=include_images, images_folder=images_folder, print_results=print_results, show_progress=show_progress, isPDF=pdf, threshold=threshold)
        doc = fitz.open(pdf_path)

        print(f"\nInput_pdf: {pdf_path}\nInclude Images?: {include_images}\nImages Folder: {images_folder}\nOutput Folder: {output_path}\nPrint Results?: {print_results}\nShow Progress?: {show_progress}\nThreshold: {threshold}\nFile Output Type: {'pdf' if pdf else 'txt' if txt else 'docx' if docx else ''}\n")
        
        doc.close()

        if not persist_state: clear_state()
        

