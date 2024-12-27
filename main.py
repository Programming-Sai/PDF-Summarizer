from extractHeadings import getHeadings, getImageCaption
from extractHighlightedText import getHighlightedText, getTextFromPDFAsParagraphs
from extractImages import getImages
from utils import *
from thefuzz import fuzz, process
import argparse as ag
import sys
import json

# from test2 import save_to_docx, create_header_footer


 
def get_summary(doc, print_results=False, include_images=False, images_folder="images/images", show_progress=True, threshold=50, show_image_process=False):
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
        hText = getHighlightedText(doc, page_num, img, show_result_image=show_image_process, show_process=show_image_process, save_extracted_text=False)
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
            getImages(img, show_contours=show_image_process, show_result=show_image_process)
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




STATE_FILE = "state.json"

def save_state(pdf_path, persist_state):
    state = {
        "pdf_path": pdf_path,
        "persist_state": persist_state
    }
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)  

def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
        pdf_path = state.get("pdf_path")
        persist_state = state.get("persist_state")
        return pdf_path, persist_state
    except FileNotFoundError:
        raise ValueError("State file not found.")
    except json.JSONDecodeError:
        raise ValueError("Error decoding state file.")

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
# init_parser.add_argument('pdf_file', type=str, help='Path to the PDF file.')
init_parser.add_argument('pdf_file', nargs='?', default='', type=str, help='Path to the PDF file.')
init_parser.add_argument('-d','--dont-persist-state', action='store_true', help='Determins if to persist the current state or not.')
init_parser.add_argument('-r','--reset-state', action='store_true', help='Determins if to reset the current state or not.')



summariser_parser = sub_parser.add_parser('summarize', help='Command to summmarize pdf content based on its highlighted text', description='Command to summmarize pdf content based on its highlighted text')


summariser_parser.add_argument('-i', '--include-images', action='store_true', help='Determines If images should be included in the pdf or docx result')
summariser_parser.add_argument('-f', '--images-folder', type=str, help='The path to the folder holding the images.')
summariser_parser.add_argument('-o', '--output-path', type=str, help='The path to save the result of the summarisation, if any')
summariser_parser.add_argument('-u', '--input-path', type=str, help='The path to get the pdf from for summarisation')
summariser_parser.add_argument('-p', '--print-results', action='store_true', help='Determins if the result for the entire operation should be displayed or not.')
summariser_parser.add_argument('-s', '--show-progress', action='store_true', help='Determins If the current progress of the entire operations should be shown in the terminal or not.')
summariser_parser.add_argument('-a', '--show-image-process', action='store_true', help='Determins If All the images are shown as the processing is done. enable this wisely')
summariser_parser.add_argument('--pdf', action='store_true', help='Determins whether to save the work as a pdf or not')
summariser_parser.add_argument('--txt', action='store_true', help='Determins whether to save the work as a text file or not')
summariser_parser.add_argument('--docx', action='store_true', help='Determins whether to save the work as a word file or not')
summariser_parser.add_argument('-v', '--verbose', action='store_true', help='Allows all debug and print statements to be displayed.')
summariser_parser.add_argument('-t', '--threshold', type=int, default=50, help='(0-100) Accuracy level for text summarization.')




split_parser = sub_parser.add_parser('split', help='Command USed to Split A single Pdf into get a single page, or a range of pages.', description='Command USed to Split A single Pdf into get a single page, or a range of pages.')

split_parser.add_argument('input_pdf_file', nargs='?', type=str, help='Path to the PDF file.')
split_parser.add_argument('output_pdf_file', type=str, help='Path to the PDF file.')
split_parser.add_argument('-s', '--start-page', type=int, default=None, help='This determines the starting range for the pdf splitting')
split_parser.add_argument('-e', '--end-page', type=int, default=None, help='This determines the end range for the pdf splitting')




merge_parser = sub_parser.add_parser('merge', help='This would merge multiple pdfs into a single one.', description='This would merge multiple pdfs into a single one.')


merge_parser.add_argument('output_pdf_file', help="Path to the output PDF file")
merge_parser.add_argument('input_pdf_files', nargs='*', help="Paths to the input PDF files for merging")




pdf2img_parser = sub_parser.add_parser('pdf2img', help='Converts a single pdf page to a pdf', description='Converts a single pdf page to a pdf')

pdf2img_parser.add_argument('input_pdf_file', nargs='?', type=str, help='Path to the PDF file for image conversion.')
pdf2img_parser.add_argument('output_pdf_file', type=str, help='Path to the Output PDF file.')
pdf2img_parser.add_argument('page_number', type=int, default=None, help='This determines the end range for the pdf splitting')




args = parser.parse_args()




if args.command == 'init':
    if args.reset_state:
        if not os.path.exists(STATE_FILE):
            print("Error: No saved state to reset.")
            sys.exit(1)
        else:
            clear_state()
            sys.exit(0)

    if not args.pdf_file:
        print("Error: You must specify a PDF file unless using --reset-state/-r.")
        sys.exit(1)

    pdf_path = args.pdf_file
    if not os.path.exists(pdf_path):
        print(f"Error: File '{pdf_path}' does not exist.")
        sys.exit(1)
    print(f"Initialized with PDF file: {pdf_path}")

    if args.dont_persist_state:
        save_state(pdf_path, False)
        print("Current State would Not be preserved.")
    else:
        save_state(pdf_path, True)



elif args.command == 'summarize':
        try:
            pdf_path, persist_state = load_state()
        except ValueError as e:
            if args.input_path:
                pdf_path = args.input_path
                persist_state = False
            else:
                # print(str(e), file=sys.stderr)
                print("No input file stated")
                sys.exit(1)
        include_images=False
        images_folder = "images/images"
        output_path = "test_pdfs/OUTPUT.pdf"
        print_results = False
        show_progress = True
        show_image_process = False
        pdf = True
        txt = False
        docx = False
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
        if args.show_image_process:
            show_image_process = False
        if args.verbose:
            print_results = True
            show_progress = True
            show_image_process = True


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

        print(f"\nInput_pdf: {pdf_path}\nInclude Images?: {include_images}\nImages Folder: {images_folder}\nOutput Folder: {output_path}\nPrint Results?: {print_results}\nShow Progress?: {show_progress}\nThreshold: {args.threshold}\nFile Output Type: {'pdf' if pdf else 'txt' if txt else 'docx' if docx else ''}\n\nState Persistance: {persist_state}\nVerbose Mode: {args.verbose}\n")
        
        doc.close()

        if not persist_state: 
            print("Clearing state...")
            clear_state()
        else:
            print("State is preserved.")



elif args.command == 'split':
    try:
        # Attempt to load the input PDF file path from the saved state
        input_pdf_file, persist_state = load_state()
    except ValueError as e:
        # If the saved state doesn't have the input, check the user-provided input
        if args.input_pdf_file:
            input_pdf_file = args.input_pdf_file
        else:
            print("Error: No input file stated. Please provide an input file.")
            sys.exit(1)
    
    # Validate input PDF file
    if not os.path.isfile(input_pdf_file):
        print(f"Error: {input_pdf_file} doesn't exist")
        sys.exit(1)
    elif not input_pdf_file.lower().endswith('.pdf'):
        print(f"Error: {input_pdf_file} is not a PDF file. It must end with `.pdf`")
        sys.exit(1)
    
    output_pdf_file = args.output_pdf_file
    output_dir = os.path.dirname(output_pdf_file)
    if output_dir and not os.path.exists(output_dir):
        print(f"Error: The directory '{output_dir}' doesn't exist.")
        sys.exit(1)
    if not output_pdf_file.lower().endswith('.pdf'):
        print("Error: The output file must have a `.pdf` extension.")
        sys.exit(1)
    if args.start_page:
        start_page_str = str(args.start_page)  # Ensure it's treated as a string
        if not start_page_str.isdigit():
            print(f"Error: {args.start_page} must be an integer.")
            sys.exit(1)
        start_page = int(args.start_page)  # Convert to integer
        if start_page < 1:
            print(f"Error: {args.start_page} must be an integer greater than 0.")
            sys.exit(1)
    if args.end_page:
        end_page_str = str(args.end_page)  # Ensure it's treated as a string
        if not end_page_str.isdigit():
            print(f"Error: {args.end_page} must be an integer.")
            sys.exit(1)
        end_page = int(args.end_page)  # Convert to integer
        if end_page < 1:
            print(f"Error: {args.end_page} must be an integer greater than 0.")
            sys.exit(1)
        
        if args.start_page and end_page < start_page:
            print(f"Error: End page must be greater than or equal to start page.")
            sys.exit(1)
    if not args.start_page and not args.end_page:
        print("Both Start and End Page Cannot be Empty")
        sys.exit(1)

    print(f"\nInput PDF: {input_pdf_file}\nOutput PDF: {output_pdf_file}\nStart Page: {args.start_page}\nEnd Page: {args.end_page}\n")




elif args.command == 'merge':
    if len(args.input_pdf_files) < 2:
        print("Error: At least two input PDFs must be provided to merge.")
        sys.exit(1)

    # Validate input PDF files
    for input_pdf in args.input_pdf_files:
        if not os.path.isfile(input_pdf):
            print(f"Error: {input_pdf} doesn't exist")
            sys.exit(1)
        elif not input_pdf.lower().endswith('.pdf'):
            print(f"Error: {input_pdf} is not a PDF file. It must end with `.pdf`")
            sys.exit(1)

    output_pdf_file = args.output_pdf_file
    output_dir = os.path.dirname(output_pdf_file)
    if output_dir and not os.path.exists(output_dir):
        print(f"Error: The directory '{output_dir}' doesn't exist.")
        sys.exit(1)
    if not output_pdf_file.lower().endswith('.pdf'):
        print("Error: The output file must have a `.pdf` extension.")
        sys.exit(1)
    
    print(f"Output Pdf Path: {output_pdf_file}\nInput Pdf Paths: {args.input_pdf_files}")




elif args.command == 'pdf2img':
    try:
        # Attempt to load the input PDF file path from the saved state
        input_pdf_file, persist_state = load_state()
    except ValueError as e:
        # If the saved state doesn't have the input, check the user-provided input
        if args.input_pdf_file:
            input_pdf_file = args.input_pdf_file
        else:
            print("Error: No input file stated. Please provide an input file.")
            sys.exit(1)
    
    output_pdf_folder = args.output_pdf_file
    if not os.path.isdir(output_pdf_folder):
        # Check if the directory exists, if not create it
        try:
            os.makedirs(output_pdf_folder)
            print(f"Directory '{output_pdf_folder}' created.")
        except Exception as e:
            print(f"Error: Failed to create directory '{output_pdf_folder}'. {e}")
            sys.exit(1)
    
    page_number = None  # Set default value to None

    if args.page_number:
        page_number_str = str(args.page_number)
        if not page_number_str.isdigit():
            print(f"Error: {args.page_number} must be an integer.")
            sys.exit(1)
        page_number = int(args.page_number)
        if page_number < 1:
            print(f"Error: {args.page_number} must be an integer greater than 0.")
            sys.exit(1)
    if not page_number:
        print("Page Number must be greater than 1")
        sys.exit(1)

    # Print input PDF, output folder, and page number (if provided)
    print(f"\nInput PDF: {input_pdf_file}\nOutput Folder: {output_pdf_folder}\nPage Number: {page_number}\n")
