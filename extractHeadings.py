from utils import *


doc = fitz.open("test_pdfs/page_28.pdf")




def getHeadings(paragraphs):
    headings = []
    for paragraph in paragraphs:
        splits = paragraph.split("\n")
        for i in range(len(splits)-1):
            if contains_number_pattern(splits[i]):
                headings.append(splits[i]+ " " + splits[i+1])
    return list(set(headings))


def getImageCaption(paragraphs):
    captions = []
    for paragraph in paragraphs:
       
        splits = paragraph.split("\n")
        # print(splits)
        for i in range(len(splits)-1):
            if contains_number_pattern(splits[i], caption=True):
                captions.append(splits[i][splits[i].index("Figure"):].replace("\n", " ") + " " + splits[i+1])
    return captions




paragraphs = getTextFromPDFAsParagraphs(doc)


# print([paragraphs[0]])
print(getImageCaption(paragraphs))
print("\n\n")
print(getHeadings(paragraphs))
