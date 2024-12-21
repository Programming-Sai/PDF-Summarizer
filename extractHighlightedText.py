from utils import *


# path = '/Users/mac/Desktop/PDF-Summarizer/images/page_29.png'
# path = '/Users/mac/Desktop/PDF-Summarizer/images/page_41.png'
# path = '/Users/mac/Desktop/PDF-Summarizer/images/page_28.png'
path = '/Users/mac/Desktop/PDF-Summarizer/images/page_31.png'
hsv = [0, 65, 59, 255, 0, 255] 

# Step One
img = cv2.imread(path)
# cv2.imshow("Original", img)

# Step Two
imgResult, imgHSV = detectColor(img, hsv)


# Step Three & Four
imgContours, contours = getContours(imgResult, img, showCanny=True, minArea=1000, filter=0, cThr=[100, 150], draw=True)
cv2.imshow("Contours", imgContours)
print(len(contours)) #Contours are not being seen . the results for this operation is always 0. WHY????

# Step Five
roiList = getRoi(img, contours)
roiDisplay(roiList)




# Step Seven
highlightedText = []
for x, roi in enumerate(roiList):
    highlightedText.append(pytesseract.image_to_string(roi))
saveText(highlightedText)
print(highlightedText)

# Step Eight
imgStack = stackImages(0.7, ([img, imgHSV, imgResult, imgContours]))
cv2.imshow("Stacked Images", imgStack)





# def empty(a):
#     pass

# cv2.namedWindow("Trackbars")
# cv2.resizeWindow("Trackbars", 640, 240)
# cv2.createTrackbar("HUE Min", "Trackbars", 0, 179, empty)
# cv2.createTrackbar("HUE Max", "Trackbars", 179, 179, empty)
# cv2.createTrackbar("SAT Min", "Trackbars", 0, 255, empty)
# cv2.createTrackbar("SAT Max", "Trackbars", 255, 255, empty)
# cv2.createTrackbar("VAL Min", "Trackbars", 0, 255, empty)
# cv2.createTrackbar("VAL Max", "Trackbars", 255, 255, empty)

# while True:
#     h_min = cv2.getTrackbarPos("HUE Min", "Trackbars")
#     h_max = cv2.getTrackbarPos("HUE Max", "Trackbars")
#     s_min = cv2.getTrackbarPos("SAT Min", "Trackbars")
#     s_max = cv2.getTrackbarPos("SAT Max", "Trackbars")
#     v_min = cv2.getTrackbarPos("VAL Min", "Trackbars")
#     v_max = cv2.getTrackbarPos("VAL Max", "Trackbars")
#     lower = np.array([h_min, s_min, v_min])
#     upper = np.array([h_max, s_max, v_max])
#     mask = cv2.inRange(imgHSV, lower, upper)
#     cv2.imshow("Mask", mask)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break






# End
cv2.waitKey(0)
