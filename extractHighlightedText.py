from utils import *





def getHighlightedText(doc, page_number, image, show_process=False, show_result_image=True, save_extracted_text=True):
    hsv = [0, 65, 59, 255, 0, 255] 

    # Step One
    if isinstance(image, bytes):
        # If it's a byte stream, decode using cv2.imdecode
        image = np.frombuffer(image, np.uint8)
        img = cv2.imdecode(image, cv2.IMREAD_COLOR)
    elif isinstance(image, np.ndarray):
        # If it's already a NumPy array, assume it's an OpenCV image
        img = image
    else:
        raise ValueError("Unsupported image format. Provide bytes or a NumPy array.")

    cv2.imshow("Original", img) if show_process else ""

    # Step Two
    imgResult, imgHSV = detectColor(img, hsv, show_process=show_process)


    # Step Three & Four
    imgContours, contours = getContours(imgResult, img, showCanny=show_process, minArea=1000, filter=0, cThr=[100, 150], draw=True)
    cv2.imshow("Contours", imgContours) if show_process else ""

    # Step Five
    roiList = getRoi(contours)
    roiDisplay(roiList, show_process=show_process)


    # Step Six
    highlightedText = []
    for x, roi in enumerate(roiList):
        highlightedText.append(get_text_from_bbox(doc, page_number, roi))
    saveText(highlightedText) if save_extracted_text else ""

    # Step Seven
    if show_result_image:
        imgStack = stackImages(0.7, ([img, imgHSV, imgResult, imgContours]))
        cv2.imshow("Stacked Images", imgStack) 

     # End
    cv2.waitKey(0) if show_result_image else None


    return highlightedText








   