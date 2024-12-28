from utils import *
from extractors import *
from thefuzz import fuzz, process
import argparse as ag
import sys
import pkg_resources





 
def get_summary(doc, print_results=False, include_images=False, images_folder="tmp-images", show_progress=True, threshold=50, show_image_process=False):
    """
    Extracts a summarized view of a PDF document, including text highlights, headings, and optionally images.

    Arguments:
    + doc -- The PDF document object to process.
    + print_results (bool) -- Whether to print intermediate results for debugging (default: False).
    + include_images (bool) -- Whether to include images from the PDF pages (default: False).
    + images_folder (str) -- The folder to save extracted images (default: "tmp-images").
    + show_progress (bool) -- Whether to display progress messages for each page (default: True).
    + threshold (int) -- Minimum similarity score for fuzzy matching between highlights and actual text (default: 50).
    + show_image_process (bool) -- Whether to display intermediate image processing results (default: False).

    Functionality:
    1. **Text Processing:**
    - Extracts the text from each page of the PDF.
    - Identifies and extracts highlighted text from the page.
    - Performs fuzzy matching to align the highlights with the main text, filtering matches based on a similarity threshold.

    2. **Headings Processing:**
    - Extracts potential headings from the page.
    - Matches headings to the highlighted text to structure the results, inserting them at appropriate positions.

    3. **Image Processing (Optional):**
    - Converts the page into an image and displays it.
    - Extracts images from the page, saves them in the specified folder, and optionally displays contours and captions.
    - Allows user interaction for selecting captions and managing images.

    4. **Results Compilation:**
    - Constructs a structured summary for each page, including:
        - Page number
        - Highlighted text matches
        - Original text and highlight counts
        - Extracted headings
        - Extracted images and captions (if enabled)
    - Appends all results into a single list for the entire document.

    5. **Progress and Debugging:**
    - Prints progress messages and intermediate results (optional).

    Returns:
    + results -- A list containing the summarized text, headings, and images (if included) for the entire document.

    Notes:
    - Image and text extraction relies on helper functions such as `pdf_page_to_image`, `getTextFromPDFAsParagraphs`, `getHighlightedText`, `getImages`, `getHeadings`, and others.
    - Requires the `cv2` library for image processing and the `fuzzywuzzy` library for text similarity scoring.
    - Handles multi-page documents and includes functionality for user interaction in the image processing phase.
    """

    results = []

    # Processing each page
    for page_num in range(1, doc.page_count+1):
        print(f"\n[INFO] Processing page {page_num} of {doc.page_count}...") if show_progress else None


        highlight_matches = []  # Reset for each page
        original_count = 0
        highlight_matches_count = 0

        # Acquiring an image version of the page
        img = pdf_page_to_image(doc, page_num)

        # Geting the main text from the given page, for reference
        actual_page_text, actual_page_text_for_headings = getTextFromPDFAsParagraphs(doc, page_num)
        original_count = get_count(actual_page_text, original_count)
        displayResult("ORIGINAL TEXT", actual_page_text) if print_results else None

        # Extracting highlighted text on the page
        hText = getHighlightedText(doc, page_num, img, show_result_image=show_image_process, show_process=show_image_process)
        displayResult("HIGHLIGHTED TEXT", hText) if print_results else None

        # Performing fuzzy matching between highlights and actual text
        for text in hText:
            highlight_matches.extend(process.extract(text, actual_page_text, scorer=fuzz.token_sort_ratio))

        # Filter and sort matches to allow the main txt to appear in order
        highlight_matches = list(dict.fromkeys([match for match, score in highlight_matches if score >= threshold]))
        highlight_matches = sorted(highlight_matches, key=lambda x: actual_page_text.index(x))
        displayResult("HIGHLIGHTED TEXT MATCHES", highlight_matches) if print_results else None


        

        if include_images:
            while True:
                cv2.imshow('Original Image', img)
                key = cv2.waitKey(1) & 0xFF
                if key == 27 or key in (ord('q'), ord('x')):  # Press ESC to close or click on an option
                    break
            getImages(img, images_folder, show_contours=show_image_process, show_result=show_image_process)
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







def home_screen():
    """
    Display the home screen of the OSPDF application, including a gradient ASCII 
    title and a welcome message with an overview of the application's features.

    The home screen displays:
    - A gradient-colored ASCII title.
    - A brief welcome message with the version and usage tips.
    
    This function will call `gradient_text` to apply a color gradient to both 
    the ASCII art title and the welcome message text.

    Example:
    >>> home_screen()
    Welcome to OSPDF!
    Version: 0.0.1
    OSPDF helps you manage and work with PDFs...
    """
    
    title = r'''
 _____                             _____ 
( ___ )---------------------------( ___ )
 |   |                             |   | 
 |   |                      _  __  |   | 
 |   |   ___  ___ _ __   __| |/ _| |   | 
 |   |  / _ \/ __| '_ \ / _` | |_  |   | 
 |   | | (_) \__ \ |_) | (_| |  _| |   | 
 |   |  \___/|___/ .__/ \__,_|_|   |   | 
 |   |           |_|               |   | 
 |___|                             |___| 
(_____)---------------------------(_____)
'''
    
    # Apply the gradient to the ASCII art
    gradient_title = gradient_text(title, [196, 214, 226])
    title_lines = gradient_title.splitlines()
    for line in title_lines:
        print(line)

    welcome_message = '''
Welcome to OSPDF!

Version: 0.0.1

OSPDF helps you manage and work with PDFs. Here are some of the things you can do:
- Summarize PDF content based on highlighted text.
- Split a PDF into individual pages or ranges.
- Merge multiple PDFs into one.
- Convert a PDF page into an image.

Tips
------
- Use `init` so that you would not need to state the input file every time you want to do an operation.
- You can reset or clear you session by running `ospdf init -r | --reset-state`.
- Use the -h | --help when in doubt or confused.
    '''

    gradient_title = gradient_text(welcome_message, [211, 220, 228])
    title_lines = gradient_title.splitlines()
    for line in title_lines:
        print(line)





def main():

    check_and_create_folder(".ospdf-tmp-images")

    parser = ag.ArgumentParser(prog='ospdf', description='Manage and summarize PDF files effectively with custom commands.')

    # parser.add_argument('-v', '--version', action='version', version=f"%{parser.prog}s {pkg_resources.get_distribution('ospdf').version}")0.0.1'
    parser.add_argument('-v', '--version', action='version', version=f"{parser.prog} {'0.0.1'}")


    sub_parser = parser.add_subparsers(dest='command', required=False, parser_class=ag.ArgumentParser)


    init_parser = sub_parser.add_parser('init', help='Set up the tool with a specific PDF file and optionally adjust its state.')

    init_parser.add_argument('pdf_file', nargs='?', default='', type=str, help='Path to the target PDF file to be used. Leave empty to use the current state.')
    init_parser.add_argument('-d','--dont-persist-state', action='store_true', help='Specify if the current state should not be saved. By default, the state will persist.')
    init_parser.add_argument('-r','--reset-state', action='store_true', help='Reset the saved state to start fresh with the specified or default PDF file.')


    summariser_parser = sub_parser.add_parser('summarize', help='Summarize PDF content based on highlighted text.', description='Use this command to generate summaries from highlighted sections of a PDF. You can include images, customize the output format, and control various processing options.')

    summariser_parser.add_argument('-i', '--include-images', action='store_true', help='Include images from the PDF in the summary output (PDF or DOCX formats).')
    summariser_parser.add_argument('-o', '--output-path', type=str, help='Path to save the summary file. Supports PDF, DOCX, or TXT formats based on selected options.')
    summariser_parser.add_argument('-u', '--input-path', type=str, help='Path to the input PDF file for summarization. Overrides any saved state.')
    summariser_parser.add_argument('-p', '--print-results', action='store_true', help='Display the summarization results directly in the terminal.')
    summariser_parser.add_argument('-s', '--show-progress', action='store_true', help='Display progress updates in the terminal during summarization.')
    summariser_parser.add_argument('-a', '--show-image-process', action='store_true', help='Preview each image during processing. Use cautiously as it may slow down operations and clutter the screen.')
    summariser_parser.add_argument('--pdf', action='store_true', help='Save the summary as a PDF file.')
    summariser_parser.add_argument('--txt', action='store_true', help='Save the summary as a plain text file.')
    summariser_parser.add_argument('--docx', action='store_true', help='Save the summary as a Word document.')
    summariser_parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode to display all debug and status messages.')
    summariser_parser.add_argument('-t', '--threshold', type=int, default=50, help='Set the summarization accuracy threshold (0-100). Higher values prioritize precision.')


    split_parser = sub_parser.add_parser('split', help='Split a PDF to extract a single page or a range of pages.', description='Use this command to split a PDF file, extracting either a single page or a specified range of pages into a new file.')

    split_parser.add_argument('input_pdf_file', nargs='?', type=str, help='Path to the input PDF file. Overrides any saved state if provided.')
    split_parser.add_argument('output_pdf_file', type=str, help='Path to save the extracted pages as a new PDF file.')
    split_parser.add_argument('-s', '--start-page', type=int, default=None, help='Specify the starting page number for extraction. Defaults to the first page.')
    split_parser.add_argument('-e', '--end-page', type=int, default=None, help='Specify the ending page number for extraction. Defaults to the last page.')


    merge_parser = sub_parser.add_parser('merge', help='Merge multiple PDF files into a single PDF.', description='Combine multiple PDF files into one. Specify the output file and input files to merge.')

    merge_parser.add_argument('output_pdf_file', help="Path to save the merged PDF file.")
    merge_parser.add_argument('input_pdf_files', nargs='*', help="Paths to the input PDF files to be merged. Provide two or more PDF file paths.")


    pdf2img_parser = sub_parser.add_parser('pdf2img', help='Convert a single PDF page to an image.', description='Extract a specific page from a PDF and convert it into an image file.')
  
    pdf2img_parser.add_argument('input_pdf_file', nargs='?', type=str, help='Path to the input PDF file for page-to-image conversion. Overrides saved state if provided.')
    pdf2img_parser.add_argument('output_img_path', type=str, help='Path to save the converted image file.')
    pdf2img_parser.add_argument('page_number', type=int, default=None, help='The page number to extract and convert to an image.')



    parser.set_defaults(func=home_screen)


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
            output_path = "OS_PDF_SUMMARIZATION_OUTPUT.pdf"
            print_results = False
            show_progress = True
            show_image_process = False
            pdf = True
            txt = False
            docx = False
            if args.input_path:
                pdf_path = args.input_path
            if args.include_images:
                include_images = True

            output_path = args.output_path or output_path
            output_dir = os.path.dirname(output_path) 
            if output_dir and not os.path.exists(output_dir):
                print(f"Error: The directory '{output_dir}' doesn't exist.")
                sys.exit(1)
            if not output_path.lower().endswith('.pdf') and args.pdf:
                print("Error: The output file must have a `.pdf` extension.")
                sys.exit(1)
            if not output_path.lower().endswith('.docx') and args.docx:
                print("Error: The output file must have a `.docx` extension.")
                sys.exit(1)
            if not output_path.lower().endswith('.txt') and args.txt:
                print("Error: The output file must have a `.txt` extension.")
                sys.exit(1)
            if args.print_results:
                print_results = True
            if args.show_progress:
                show_progress = False
            if args.show_image_process:
                show_image_process = True
            if args.verbose:
                print_results = True
                show_progress = True
                show_image_process = True
            if args.threshold is not None:
                if not  0<= args.threshold <= 100:
                    print(f"Error: {args.threshold} is invalid. Threshold must be between 0 and 100.")
                    sys.exit(1)

            if args.txt:
                txt = True
                pdf = False  
            if args.docx:
                docx = True
                pdf = False  
            if not (pdf or txt or docx):
                pdf = True



            doc = fitz.open(pdf_path)
            print(pdf, txt, docx)
            
            results = get_summary(doc, include_images=include_images, images_folder=".ospdf-tmp-images", print_results=print_results, show_progress=show_progress, threshold=args.threshold, show_image_process=show_image_process)
            if docx:
                save_to_docx(results, output_path)
            elif txt:
                save_to_txt(results, output_path)
            else:
                save_to_pdf(results, output_path) 
            
            doc.close()

            if not persist_state: 
                print("Clearing state...")
                clear_state()





    elif args.command == 'split':
        start_page = None
        end_page = None
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

        if args.input_pdf_file:
            input_pdf_file = args.input_pdf_file
        
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
        if args.end_page and not args.start_page:
            print("If you want to split only one page, then set the start page only, else you would need both start and end pages set.")
            sys.exit(1)
        if not args.start_page and not args.end_page:
            print("Both Start and End Page Cannot be Empty")
            sys.exit(1)
        
        split_pdf(input_pdf_file, output_pdf_file, start_page=start_page, end_page=end_page)
        print(f"Successfully Split {input_pdf_file} and is saved at {output_pdf_file}")


        if not persist_state: 
            print("Clearing state...")
            clear_state()




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


        merge_pdfs(output_pdf_file, *args.input_pdf_files)


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
        
        if args.input_pdf_file:
            input_pdf_file = args.input_pdf_file
        
        if not os.path.isfile(input_pdf_file):
            print(f"Error: {input_pdf_file} doesn't exist")
            sys.exit(1)
        elif not input_pdf_file.lower().endswith('.pdf'):
            print(f"Error: {input_pdf_file} is not a PDF file. It must end with `.pdf`")
            sys.exit(1)
        
        output_pdf_path = args.output_img_path
        if os.path.isdir(output_pdf_path):
            # If the path is a directory and does not have a file name, ask for a valid file name
            print(f"Error: '{output_pdf_path}' is a directory. Please provide a full file path including the file name and extension (e.g., 'output_image.png').")
            sys.exit(1)

        if os.path.basename(output_pdf_path) == output_pdf_path:  # No directory provided, only a file name
            output_pdf_path = os.path.join(os.getcwd(), output_pdf_path)
            print(f"Saving image to the current directory: {output_pdf_path}")

        # Check if the file path ends with a valid image extension
        valid_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif']
        if not any(output_pdf_path.lower().endswith(ext) for ext in valid_extensions):
            print("Error: Please provide a valid file name with a supported image extension (e.g., .png, .jpg).")
            sys.exit(1)

        # If the directory doesn't exist, create it
        directory = os.path.dirname(output_pdf_path)
        if not os.path.isdir(directory):
            try:
                os.makedirs(directory)
                print(f"Directory '{directory}' created.")
            except Exception as e:
                print(f"Error: Failed to create directory '{directory}'. {e}")
                sys.exit(1)
        
        page_number = None  

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

        save_image(pdf_page_to_image(fitz.open(input_pdf_file), page_number), output_pdf_path)
        

        if not persist_state: 
            print("Clearing state...")
            clear_state()


    else:
        args.func()



if __name__ == '__main__':
    main()