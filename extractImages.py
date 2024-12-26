from utils import *



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


