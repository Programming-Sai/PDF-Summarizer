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








   


def getImages(image, show_contours=True, show_result=True, save_result=True):

    # Load the image
    if isinstance(image, bytes):
        # If it's a byte stream, decode using cv2.imdecode
        image = np.frombuffer(image, np.uint8)
        img = cv2.imdecode(image, cv2.IMREAD_COLOR)
    elif isinstance(image, np.ndarray):
        # If it's already a NumPy array, assume it's an OpenCV image
        img = image
    else:
        raise ValueError("Unsupported image format. Provide bytes or a NumPy array.")


    # Detect images
    imgContours, images = detectImages(img) 

    # Display contours on the original image
    cv2.imshow("Detected Images", imgContours) if show_contours else None

    # Save or display each detected image region
    for i, croppedImage in enumerate(images):
        cv2.imshow(f"Image {i+1}", croppedImage) if show_result else ""
        cv2.imwrite(f"images/images/extracted_image_{i+1}-{int(time.time())}.png", croppedImage)  if save_result else ""

    cv2.waitKey(0) if show_contours else None
    cv2.destroyAllWindows()


