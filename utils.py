import cv2
import numpy as np
from pytesseract import pytesseract
import re
import fitz
from PIL import Image
import io




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
    caption_pattern = r".*\bFigure \d+\.\d+(\.\d+)?\b.*"  # Matches figure references like "Figure 1.1"
    general_pattern = r"^\s*\d+\.\d+(\.\d+)?\b.*"  # Matches valid headings (e.g., "1.1 Introduction")

    string = string.replace("\n", " ")  # Normalize string for pattern matching

    if caption:
        # Check for caption pattern
        return bool(re.match(caption_pattern, string))

    # Exclude figure references
    if not re.search(caption_pattern, string):
        # Check for general heading pattern
        return bool(re.match(general_pattern, string))

    return False


def getTextFromPDFAsParagraphs(doc, page_number):
    text = doc.load_page(page_number-1).get_text()
    paragraphsForNormal = [i.replace("\n", " ").strip() for i in text.split('. ') if i.replace("\n", " ").strip()]
    paragraphsForHeadings = [i.strip() for i in text.split('. ') if i.strip()]
    return paragraphsForNormal, paragraphsForHeadings


def getRoi(contours):
    roiList = []
    for con in contours:
        x, y, w, h = con[3]
        roiList.append((x, y, x+w, y+h))
    return roiList


def get_text_from_bbox(doc, page_number, bbox):
    # Load the specified page (note: page_number is 1-based)
    page = doc.load_page(page_number - 1)
    
    # Get text from the specified bounding box area
    text = page.get_text("text", clip=fitz.Rect(bbox))
    return text


def roiDisplay(roiList, show_process=False):
    for x, roi in enumerate(roiList):
        roi = cv2.resize(roi, (0, 0), None, 2, 2)
        cv2.imshow(f"Cropped Image {x}", roi) if show_process else ""


def saveText(highlightedText, result_name):
    with open(result_name or "Result.txt", 'w') as f:
        for text in highlightedText:
            f.writelines(f'\n{text}')


def preprocess_image(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to enhance text
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Denoise the image
    denoised = cv2.medianBlur(thresh, 3)

    return denoised


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


def split_pdf(input_pdf, output_folder, start_page=None, end_page=None):
    # Open the input PDF
    doc = fitz.open(input_pdf)

    # Handle single page extraction
    if start_page is not None and end_page is None:
        end_page = start_page  # If only start_page is provided, treat it as a single page
        # Create a new PDF for the single page
        new_doc = fitz.open()
        new_doc.insert_pdf(doc, from_page=start_page - 1, to_page=start_page - 1)
        
        # Save the new PDF with the page number
        new_doc.save(f"{output_folder}/page_{start_page}.pdf")
        new_doc.close()
        doc.close()
        return 

    # If both start_page and end_page are provided, extract the range of pages
    if start_page is not None and end_page is not None:
        # Ensure page numbers are within the valid range
        start_page = max(start_page - 1, 0)  # fitz uses zero-indexed pages
        end_page = min(end_page - 1, doc.page_count - 1)

        # Create a new PDF for the range of pages
        new_doc = fitz.open()
        
        # Insert pages in the specified range
        new_doc.insert_pdf(doc, from_page=start_page, to_page=end_page)

        # Save the new PDF with the page range
        new_doc.save(f"{output_folder}/pages_{start_page + 1}_to_{end_page + 1}.pdf")
        new_doc.close()
        doc.close()
        return 


def pdf_page_to_image(doc, page_number):    
    # Ensure the page number is valid
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

    return bgr_image


def save_image(image, output_image_path):
    """
    Save a PIL Image object to a file.
    
    :param image: The PIL Image object to save.
    :param output_image_path: The file path where the image should be saved.
    """
    if image:
        image.save(output_image_path)
        print(f"Image saved to {output_image_path}")
    else:
        print("No image to save.")

