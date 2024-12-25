import cv2
import numpy as np
from pytesseract import pytesseract
import re
import fitz




def detectColor(img, hsv, show_process=False):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    cv2.imshow("HSV", imgHSV) if show_process else ""
    lower = np.array([hsv[0], hsv[2], hsv[4]])
    upper = np.array([hsv[1], hsv[3], hsv[5]])
    mask = cv2.inRange(imgHSV, lower, upper)
    imgResult = cv2.bitwise_and(img, img, mask=mask)
    cv2.imshow("Result", imgResult) if show_process else ""
    return imgResult, imgHSV


def getContours(img, imgDraw, showCanny=False, minArea=1000, filter=0, cThr=[100, 100], draw=True):
    imgDraw = imgDraw.copy()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, cThr[0], cThr[1])
    kernel = np.ones((10, 10), np.uint8)
    imgDial = cv2.dilate(imgCanny, kernel, iterations=1)
    imgClose = cv2.morphologyEx(imgDial, cv2.MORPH_CLOSE, kernel)

    if showCanny: cv2.imshow("Canny", imgClose)

    contours, hierarchy = cv2.findContours(imgClose, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    finalContours = []
    for i in contours:
        area = cv2.contourArea(i)
        if area > minArea:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02*peri, True)
            bbox = cv2.boundingRect(approx)
            if filter > 0: 
                if len(approx) == filter:
                    finalContours.append([len(approx), area, approx, bbox, i])
            else:
                finalContours.append([len(approx), area, approx, bbox, i])

    finalContours = sorted(finalContours, key=lambda x: x[3][1])

    if draw:
        for con in finalContours:
            x, y, w, h = con[3]
            cv2.rectangle(imgDraw, (x, y), (x+w, y+h), (255, 0, 255), 3)
    return imgDraw, finalContours



def detectImages(img):
    # Convert to grayscale
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply edge detection
    edges = cv2.Canny(imgGray, 50, 150)

    # Dilate edges to connect nearby components
    kernel = np.ones((5, 5), np.uint8)
    imgDilated = cv2.dilate(edges, kernel, iterations=1)

    # Find contours
    contours, _ = cv2.findContours(imgDilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    imgContours = img.copy()
    imageRegions = []

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:  # Adjust the area threshold based on your use case
            x, y, w, h = cv2.boundingRect(contour)
            aspectRatio = w / float(h)

            # Filter based on aspect ratio or size if needed
            if 0.5 < aspectRatio < 3:  # Adjust aspect ratio range
                cv2.rectangle(imgContours, (x, y), (x + w, y + h), (255, 0, 255), 2)
                imageRegions.append(img[y:y+h, x:x+w])  # Crop image regions

    return imgContours, imageRegions


def contains_number_pattern(string, caption=False):
    # Pattern for captions: "Some things_Figure *.* Some other things"
    caption_pattern = r".*Figure \d+\.\d+(\.\d+)?(.*)"
    
    # Pattern for non-captions: "___*.*___" or "___*.*.*___"
    general_pattern = r".*\d+\.\d+(\.\d+)?.*"
    
    if caption:
        # Check if the string matches the pattern "Some things_Figure *.* Some other things"
        if re.match(caption_pattern, string.replace("\n", " ")):  # Replace newlines with spaces for easier matching
            return True
        else:
            return False
    if not re.search(r".* Figure \d+\.\d+(\.\d+)?", string):
        # Check for non-captions that have format "___*.*___" or "___*.*.*___"
        if re.search(general_pattern, string.replace("\n", " ")):  # Replace newlines with spaces for easier matching
            return True
    return False


def getTextFromPDFAsParagraphs(doc):
    text = ""

    # Loop through all the pages in the PDF
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text()

    # Split the text into paragraphs by newlines
    paragraphs = text.split('. ')

    # Optionally, you can further process paragraphs if needed
    paragraphs = [p.strip() for p in paragraphs if p.strip()]
    return paragraphs


def getRoi(img, contours):
    roiList = []
    for con in contours:
        x, y, w, h = con[3]
        roiList.append(img[y:y+h, x:x+w])
    return roiList


def roiDisplay(roiList, show_process=False):
    for x, roi in enumerate(roiList):
        roi = cv2.resize(roi, (0, 0), None, 2, 2)
        cv2.imshow(f"Cropped Image {x}", roi) if show_process else ""


def saveText(highlightedText):
    with open("Result.txt", 'w') as f:
        for text in highlightedText:
            f.writelines(f'\n{text}')


def stackImages(scale, imgArray):
    rows, cols = len(imgArray), len(imgArray[0])

    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else: imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)

                if len(imgArray[x][y].shape) == 2:
                    imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_BGR2RGB)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        hor_copy = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale, scale)
            if len(imgArray[x].shape) == 2:
                imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_BGR2BGRA)
        hor = np.hstack(imgArray)
        ver = hor
    return ver

