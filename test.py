import aspose.words as aw
from docx import Document
import os

def convert_pdf_to_docx(pdf_path, output_path):
    # Load the PDF file
    doc = aw.Document(pdf_path)
    
    # Save it as a DOCX file
    doc.save(output_path, aw.SaveFormat.DOCX)


def extract_images_from_docx(docx_path, output_dir):
    # Load the document
    doc = Document(docx_path)

    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    image_index = 0
    for rel in doc.part.rels.values():
        if "image" in rel.target_ref:
            image_index += 1
            image_data = rel.target_part.blob
            image_filename = os.path.join(output_dir, f"image_{image_index}.png")
            with open(image_filename, 'wb') as img_file:
                img_file.write(image_data)
            print(f"Image saved: {image_filename}")

# Example usage
extract_images_from_docx("test_docx/page_31.docx", "images/images")


# Example usage
# convert_pdf_to_docx("test_pdfs/page_31.pdf", "test_docx/page_31.docx")
