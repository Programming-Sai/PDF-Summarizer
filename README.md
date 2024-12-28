# PDF Summarizer (ospdf)

![Platform](https://img.shields.io/badge/platform-%20Windows%2C%20Linux%2C%20macOS-blue) ![Language](https://img.shields.io/badge/language-Python-blue) ![Last Commit](https://img.shields.io/github/last-commit/Programming-Sai/PDF-Summarizer) ![Code Size](https://img.shields.io/github/languages/code-size/Programming-Sai/PDF-Summarizer) ![Python](https://img.shields.io/badge/python-%3E%3D%203.6-green) ![Documentation](https://img.shields.io/badge/Docs-%20Yes-brightgreen)

The **PDF Summarizer** tool allows you to manage and summarize PDF files effectively through various commands. This README provides detailed instructions on how to install, use, and uninstall the tool.

---

## Installation

1. Clone the repository:

   ```bash
    git clone --branch ospdf https://github.com/Programming-Sai/PDF-Summarizer.git
   ```

2. Navigate to the project directory:

   ```bash
   cd PDF-Summarizer
   ```

3. Run the installation script:

   ```bash
   python install.py
   ```

   **What this does:**

   - Creates a standalone executable using PyInstaller.
   - Moves the executable to a globally accessible location (e.g., `/usr/local/bin/ospdf` on Unix/Linux).

4. Confirm the installation by checking the tool's availability:

   ```bash
   ospdf

   # OR

   ospdf -v

   # OR

   ospdf -h
   ```

   You should see the help menu for the tool, version number or this:

   ![Home](/Home.png)

---

Here is the updated and more accurate **Usage** section based on the parameters you provided:

---

## Usage

The **ospdf** command provides the following functionality:

### General Syntax

```bash
ospdf <command> [command options]
```

### Available Commands

- **`init`**: Set up the tool with a specific PDF file or clear the initialization.

  ```bash
  ospdf init <path_to_pdf> -d
  # OR
  ospdf init -r
  ```

  - `<path_to_pdf>`: Path to the PDF file to be used. If not provided, the current state will be used.
  - `-d`, `--dont-persist-state`: Prevents saving the current state. By default, the state will persist.
  - `-r`, `--reset-state`: Resets the saved state, starting fresh with the specified or default PDF file.

- **`summarize`**: Summarize highlighted text in a PDF file.

  ```bash
  ospdf summarize -u <path_to_input_pdf_file> -o <path_to_output_file> -i -p -a -s --pdf --docx --txt -v -t
  ```

  - `-i`, `--include-images`: Include images from the PDF in the summary output (PDF or DOCX formats).
  - `-o`, `--output-path`: Path to save the summary file. Supports PDF, DOCX, or TXT formats based on selected options.
  - `-u`, `--input-path`: Path to the input PDF file for summarization. Overrides any saved state.
  - `-p`, `--print-results`: Display the summarization results directly in the terminal.
  - `-s`, `--show-progress`: Show progress updates in the terminal during summarization.
  - `-a`, `--show-image-process`: Preview each image during processing. Use cautiously as it may slow down operations and clutter the screen.
  - `--pdf`: Save the summary as a PDF file.
  - `--txt`: Save the summary as a plain text file.
  - `--docx`: Save the summary as a Word document.
  - `-v`, `--verbose`: Enable verbose mode to display all debug and status messages.
  - `-t`, `--threshold`: Set the summarization accuracy threshold (0-100). Higher values prioritize precision.

- **`split`**: Extract a single page or range of pages from a PDF.

  ```bash
  ospdf split <path_to_pdf> <path_to_output_file> -s
  ```

  - `input_pdf_file`: Path to the input PDF file. Overrides any saved state if provided.
  - `output_pdf_file`: Path to save the extracted pages as a new PDF file.
  - `-s`, `--start-page`: An integer value greater than 0 that specifies the starting page number for extraction. Defaults to the first page.
  - `-e`, `--end-page`: An integer value greater than 0 that specifies the ending page number for extraction. Defaults to the last page.

- **`merge`**: Merge multiple PDF files into a single PDF.

  ```bash
  ospdf merge <output_pdf_file> <input_pdf_1> <input_pdf_2> [...]
  ```

  - `output_pdf_file`: Path to save the merged PDF file.
  - `input_pdf_files`: Paths to the input PDF files to be merged. Provide two or more PDF file paths.

- **`pdf2img`**: Convert a single PDF page to an image.

  ```bash
  ospdf pdf2img <path_to_pdf> <output_path> <page_number>
  ```

  - `input_pdf_file`: Path to the input PDF file for page-to-image conversion. Overrides saved state if provided.
  - `output_img_path`: Path to save the converted image file.
  - `page_number`: The page number to extract and convert to an image.

### Options

- **`-h` / `--help`**: Display help information.
- **`-v` / `--version`**: Show the tool's version.

---

## Uninstallation

1. Run the uninstallation script:

   ```bash
   python uninstall.py
   ```

   **What this does:**

   - Removes the executable from the system's global path.
   - Cleans up installation traces.

2. Verify the tool is uninstalled:
   ```bash
   which ospdf
   ```
   If the command returns nothing, the tool has been successfully removed.

---

## Notes

- Ensure you have Python 3.10+ installed.
- For Windows users, installation and uninstallation scripts automatically handle the `APPDATA` location.
- For Unix/Linux users, the executable is placed in `/usr/local/bin` by default.

---

## Troubleshooting

If you encounter any issues during installation or execution:

- Ensure PyInstaller and other dependencies are installed.
- Check your Python environment and system paths.
- Review error messages for specific details.

Feel free to open an issue in the repository for further assistance.
