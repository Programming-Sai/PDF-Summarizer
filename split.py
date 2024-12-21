import fitz  # PyMuPDF

def split_pdf(input_pdf, output_folder):
    # Open the input PDF
    doc = fitz.open(input_pdf)
    
    # for page_num in range(doc.page_count):
    page_num = 30
    # Create a new PDF for each page
    new_doc = fitz.open()
    new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
    
    # Save the new PDF with the page
    new_doc.save(f"{output_folder}/page_{page_num + 1}.pdf")
    new_doc.close()

    doc.close()

# Example usage
split_pdf("test_pdfs/OPERATING SYSTEMS.pdf", "test_pdfs")
