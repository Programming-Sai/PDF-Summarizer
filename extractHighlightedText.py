from utils import *


# path = '/Users/mac/Desktop/PDF-Summarizer/images/page_29.png'
# path = '/Users/mac/Desktop/PDF-Summarizer/images/page_41.png'
# path = '/Users/mac/Desktop/PDF-Summarizer/images/page_28.png'
path = '/Users/mac/Desktop/PDF-Summarizer/images/page_31.png'


def getHighlightesText(img_path, show_process=False, show_result_image=True, save_extracted_text=True):
    hsv = [0, 65, 59, 255, 0, 255] 

    # Step One
    img = cv2.imread(img_path) 
    cv2.imshow("Original", img) if show_process else ""

    # Step Two
    imgResult, imgHSV = detectColor(img, hsv, show_process=show_process)


    # Step Three & Four
    imgContours, contours = getContours(imgResult, img, showCanny=show_process, minArea=1000, filter=0, cThr=[100, 150], draw=True)
    cv2.imshow("Contours", imgContours) if show_process else ""
    print(len(contours)) 

    # Step Five
    roiList = getRoi(img, contours)
    roiDisplay(roiList, show_process=show_process)


    # Step Six
    highlightedText = []
    for x, roi in enumerate(roiList):
        highlightedText.append(pytesseract.image_to_string(roi))
    saveText(highlightedText) if save_extracted_text else ""

    # Step Seven
    imgStack = stackImages(0.7, ([img, imgHSV, imgResult, imgContours]))
    cv2.imshow("Stacked Images", imgStack) if show_result_image else ""

     # End
    cv2.waitKey(0)


    return highlightedText, "\n\n\n" #,roiList






   
print(getHighlightesText(path))