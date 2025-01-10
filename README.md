# PDF Summarizer

![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![Platform](https://img.shields.io/badge/Platform-Mac%20%7C%20Windows%20%7C%20Linux-lightgrey) ![Repo Size](https://img.shields.io/github/repo-size/Programming-Sai/PDF-Summarizer) ![Last Commit](https://img.shields.io/github/last-commit/Programming-Sai/PDF-Summarizer) ![Tech Stack](https://img.shields.io/badge/Built%20with-Python%20%7C%20Argparse%20%7C%20OpenCV%7C%20PymuPdf%7C%20Numpy%7C%20Pillow-brightgreen) ![Coverage](https://img.shields.io/badge/Coverage-80%25-yellowgreen)

The **PDF Summarizer** is a command-line tool designed to help users manage and perform various operations on PDF files. This README provides a clear overview of how to use the tool, highlighting its key functionalities and their implementations.

---

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Programming-Sai/PDF-Summarizer.git
   ```

2. Navigate to the project directory

   ```bash
   cd PDF-Summarizer
   ```

3. Create a Virtual Environment and activate it.

   ```bash
   python -m venv .ospdf-venv

   .ospdf-venv\Scripts\activate  # Windows

   OR

   source .ospdf-venv/bin/activate  # MacOS/Linux

   ```

   <br>

   > **💡 Note:** Make sure to select the new virtual environment `.ospdf-venv` as your interpreter in VS Code. Use the shortcut **`Ctrl + Shift + P`** (Windows/Linux) or **`Cmd + Shift + P`** (Mac), then type and select **"Python: Select Interpreter"**. Choose the interpreter option marked **`Recommended`** or **`Python 3.x.x ('.ospdf-venv':venv)`**.

   <br>

4. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Run the application:

   ```bash
   python -u main.py
   ```

   On running the application, you should see an output similar to this:

   ```plaintext

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

   Welcome to PDF Summarizer!

   Version: 0.0.1

   PDF Summarizer helps you manage and work with PDFs. Here are some of the things you can do:
   - Summarize PDF content based on highlighted text.
   - Split a PDF into individual pages or ranges.
   - Merge multiple PDFs into one.
   - Convert a PDF page into an image.

   Tips
   ------
   - Use `init` to set the input file once and avoid specifying it repeatedly.
   - Reset your session with `init -r` to start fresh.
   - Use `-h` or `--help` when in doubt.
   ```

---

## Functionalities

### 1. Summarize Highlighted Text

**Description:** Extract and summarize highlighted text from a PDF file.

- **Implementation:**
  - Parses the PDF for annotations.
  - Extracts the highlighted content.
  - Optionally includes images from the PDF in the output.
- **What it does:**
  - Produces a summary as plain text, a PDF, or a Word document.

**Usage:**

```bash
python main.py summarize --input-path <path_to_pdf> --output-path <output_path>
```

### 2. Split PDF

**Description:** Extract specific pages or ranges of pages from a PDF.

- **Implementation:**
  - Uses a PDF parser to split the document based on page indices.
  - Saves the extracted pages as a new PDF.
- **What it does:**
  - Enables breaking large PDFs into smaller, more manageable files.

**Usage:**

```bash
python main.py split <path_to_pdf> <output_pdf> --start-page <start> --end-page <end>
```

### 3. Merge PDFs

**Description:** Combine multiple PDF files into one.

- **Implementation:**
  - Reads the input PDFs.
  - Concatenates their pages in the specified order.
  - Outputs a single, merged PDF.
- **What it does:**
  - Consolidates multiple related documents into a single file.

**Usage:**

```bash
python main.py merge <output_pdf> <input_pdf_1> <input_pdf_2> ...
```

### 4. Convert PDF to Image

**Description:** Convert a single page of a PDF into an image.

- **Implementation:**
  - Extracts the specified page from the PDF.
  - Renders the page as an image.
  - Saves the image in the desired format (e.g., PNG, JPEG).
- **What it does:**
  - Enables visual representation of PDF content for use in presentations or web pages.

**Usage:**

```bash
python main.py pdf2img  <path_to_pdf> <output_image> <page_number>
```

---

## Tips

- **Initialization:** Use the `init` command to set a default PDF file for your session, eliminating the need to specify the file repeatedly for each operation.
- **Help:** Add `-h` or `--help` to any command for detailed usage instructions.
- **Reset:** Start fresh by resetting the session with the `init -r` command.

---

## Troubleshooting

- Ensure you have Python 3.10+ installed.
- Verify dependencies are correctly installed using:

  ```bash
  pip list
  ```

- If a command fails, check the help menu for correct syntax.

---

```

```
