

### Extracting text as  sentences
import fitz  # PyMuPDF

# Open the PDF
pdf_document = fitz.open("test_pdfs/page_28.pdf")

# Initialize an empty string to collect all the text
text = ""

# Loop through all the pages in the PDF
for page_num in range(pdf_document.page_count):
    page = pdf_document.load_page(page_num)
    text += page.get_text()

# Split the text into paragraphs by newlines
paragraphs = text.split('. ')

# Optionally, you can further process paragraphs if needed
paragraphs = [p.strip() for p in paragraphs if p.strip()]

# Now, 'paragraphs' is a list of text paragraphs from the PDF


# print(paragraphs, len(paragraphs))

def getHeadingPrefixes():
    two_prefixes = []
    three_prefixes = []
    for i in range(1,10):
        for j in range(10):
            two_prefixes.append(f"{i}.{j}")

    for i in range(1, 10):
        for j in range(10):
            for k in range(10):
                three_prefixes.append(f"{i}.{j}.{k}")
    return two_prefixes, three_prefixes
        



def getHaedings(paragraphs):
    headings = []
    two_prefixes, three_prefixes = getHeadingPrefixes()
    for paragraph in paragraphs:
        new_line_split = paragraph.split("\n")
        for i in range(len(new_line_split)):
            if new_line_split[i] in two_prefixes or new_line_split[i] in three_prefixes:
                if i+1 <= len(new_line_split):
                    headings.append(new_line_split[i+1])
    return set(headings)

print(getHaedings(paragraphs))
# print(getHeadingPrefixes())