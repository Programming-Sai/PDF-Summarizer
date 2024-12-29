# PROBLEMS.md

## Project Issues and Solutions

This document captures the problems encountered during the development of the project and their solutions, providing a comprehensive log of challenges and improvements.

### 1. **Environment Setup Issues**

#### Problem

- Missing required dependencies, causing import errors when running the project.
- Virtual environment not being activated consistently across systems.

#### Solution

- Added a `requirements.txt` file listing all required libraries.
  ```bash
  pip install -r requirements.txt
  ```
- Provided detailed instructions on creating and activating a virtual environment:
  ```bash
  python -m venv pdf-summarizer
  source pdf-summarizer/bin/activate  # Linux/Mac
  pdf-summarizer\Scripts\activate   # Windows
  ```

---

### 2. **Temporary Folder Management**

#### Problem

- The application creates a temporary folder `.ospdf-tmp-images` but doesn’t clean up properly after execution.

#### Solution

- Added logic to delete the temporary folder at the end of the application’s execution.
  ```python
  import shutil
  shutil.rmtree('.ospdf-tmp-images', ignore_errors=True)
  ```

---

### 3. **PDF File Not Found Error**

#### Problem

- Users frequently provided incorrect file paths, resulting in a "File not found" error.

#### Solution

- Implemented a file existence check before processing:
  ```python
  import os
  if not os.path.exists(file_path):
      print(f"Error: File '{file_path}' not found.")
      exit(1)
  ```
- Provided clear error messages to guide the user.

---

### 4. **Summarization Accuracy**

#### Problem

- Summarized content often missed important details, leading to inaccurate outputs.

#### Solution

- Added an adjustable threshold parameter to control summarization accuracy:
  ```bash
  python main.py summarize --threshold 75
  ```
- Explained the impact of the threshold in the README file.

---

### 5. **Inconsistent Page Splitting**

#### Problem

- Splitting PDFs by page range didn’t handle invalid input well, causing crashes.

#### Solution

- Added validation for page numbers:
  ```python
  if start_page < 1 or end_page > total_pages:
      print("Error: Invalid page range.")
      exit(1)
  ```
- Defaulted to the first and last pages if no range was provided.

---

### 6. **Merge File Order**

#### Problem

- Merged PDFs were often in the wrong order due to unsorted input files.

#### Solution

- Sorted input files before merging:
  ```python
  input_files = sorted(input_files)
  ```

---

### 10. **Output Format Compatibility**

#### Problem

- Summarization output didn’t support saving in multiple formats (PDF, DOCX, TXT).

#### Solution

- Integrated libraries for generating different output formats:
  - PDF: `fpdf`
  - DOCX: `python-docx`
  - TXT: Built-in file handling.
  ```python
  if docx:
    save_to_docx(results, output_path)
  elif txt:
    save_to_txt(results, output_path)
  else:
    save_to_pdf(results, output_path)
  ```

---

### 12. **User Input Validation**

#### Problem

- Invalid input (e.g., unsupported commands or missing arguments) caused crashes.

#### Solution

- Implemented input validation and provided fallback messages:
  ```python
  if command not in ['summarize', 'split', 'merge', 'pdf2img']:
      print("Error: Unsupported command. Use --help for available commands.")
  ```

---

### 15. **Documentation Gaps**

#### Problem

- Initial documentation lacked details on advanced functionalities.

#### Solution

- Expanded the README and added example commands.
- Created `PROBLEMS.md` for issue tracking and solutions.

---

Here’s a list of the issues you selected during the start of this project, formatted as requested:

---

### 1. **Highlight Removal in Images**

#### Problem

- The images had highlighted text, requiring the removal of highlights while retaining the original text clarity.

#### Solution

- Used OpenCV to apply color masks for removing highlights.
- Converted the background to white and the text to black for better visibility.

---

### 2. **Sharpening Blurred Text**

#### Problem

- Extracted images often had blurry or unclear text, making it difficult to process.

#### Solution

- Applied an image-sharpening function using OpenCV’s kernel filters to enhance the clarity of text.

---

### 3. **Converting PDF Pages to Images**

#### Problem

- There was a need to convert PDF pages into individual images for processing.

#### Solution

- Used the inbuilt functionality of Pymupdf

```python
if page_number < 1 or page_number > doc.page_count:
    print("Invalid page number!")
    return None

# Get the specified page (0-indexed, so subtract 1)
page = doc.load_page(page_number - 1)

# Convert the page to a pixmap (image)
pix = page.get_pixmap()

# Convert the pixmap to a PIL image
pil_image = Image.open(io.BytesIO(pix.tobytes()))
rgb_array = np.array(pil_image)

# Convert RGB to BGR (OpenCV uses BGR format)
bgr_image = cv2.cvtColor(rgb_array, cv2.COLOR_RGB2BGR)

```

---

### 4. **Manual Highlight Extraction Challenges**

#### Problem

- Extracting manually highlighted text required special processing due to irregularities like uneven colors and strokes.

#### Solution

- Implemented thresholding and segmentation techniques to isolate text from manually added highlights all this using OpenCV.

---

### 5. **Text Extraction from Images**

#### Problem

- Extracting text from processed images was inconsistent and prone to errors.

#### Solution

- Used OpenCV to get the bounding boxes of the highlighted text, and then used Pymupdf to get the texts within those bounding boxes.
- Since that lead to a lot of cut off texts I used sentence matching with `thefuzz` to get the sentences that contained highlighted texts.

---

### 5. **Image Extraction From Images (PDF)**

#### Problem

- Extracting images from the pages was an issue, using PymuPDF and hence i resulted to OpenCV again.

#### Solution

- Used OpenCV to get the bounding boxes of the images.
- Since OpenCV can't differenciate between images of text and images of images, i provided all extracted images for the user to select the correct ones.

---
