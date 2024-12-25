from utils import *


# path = '/Users/mac/Desktop/PDF-Summarizer/images/page_29.png'
# path = '/Users/mac/Desktop/PDF-Summarizer/images/page_41.png'
# path = '/Users/mac/Desktop/PDF-Summarizer/images/page_28.png'
path = '/Users/mac/Desktop/PDF-Summarizer/images/page_31.png'



def getImages(img_path, show_result=True, save_result=True):

    # Load the image
    img = cv2.imread(img_path)

    # Detect images
    imgContours, images = detectImages(img)

    # Display contours on the original image
    cv2.imshow("Detected Images", imgContours)

    # Save or display each detected image region
    for i, croppedImage in enumerate(images):
        cv2.imshow(f"Image {i+1}", croppedImage) if show_result else ""
        cv2.imwrite(f"images/images/extracted_image_{i+1}.png", croppedImage)  if save_result else ""

    cv2.waitKey(0)
    cv2.destroyAllWindows()


getImages(path)