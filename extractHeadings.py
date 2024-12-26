from utils import *






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



