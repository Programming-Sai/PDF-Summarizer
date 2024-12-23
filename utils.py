import cv2
import numpy as np
from pytesseract import pytesseract



def detectColor(img, hsv):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # cv2.imshow("HSV", imgHSV)
    lower = np.array([hsv[0], hsv[2], hsv[4]])
    upper = np.array([hsv[1], hsv[3], hsv[5]])
    mask = cv2.inRange(imgHSV, lower, upper)
    imgResult = cv2.bitwise_and(img, img, mask=mask)
    # cv2.imshow("Result", imgResult)
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
            # approx = cv2.approxPolyDP(i, 0.82*peri, True)
            bbox = cv2.boundingRect(approx)
            if filter > 0: 
                if len(approx) == filter:
                    finalContours.append([len(approx), area, approx, bbox, i])
            else:
                finalContours.append([len(approx), area, approx, bbox, i])

    finalContours = sorted(finalContours, key=lambda x: x[1], reverse=True)

    if draw:
        for con in finalContours:
            x, y, w, h = con[3]
            cv2.rectangle(imgDraw, (x, y), (x+w, y+h), (255, 0, 255), 3)
            # cv2.drawContours(imgDraw, con[4], -1, (0, 0, 255), 2)
    return imgDraw, finalContours




def getContoursOne(img, imgDraw, showCanny=False, minArea=1000, filter=0, cThr=[100, 150], draw=True):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
    imgCanny = cv2.Canny(imgBlur, cThr[0], cThr[1])
    kernel = np.ones((10, 10), np.uint8)
    imgDial = cv2.dilate(imgCanny, kernel, iterations=1)
    imgClose = cv2.morphologyEx(imgDial, cv2.MORPH_CLOSE, kernel)

    if showCanny: cv2.imshow("Canny", imgClose)

    contours, hierarchy = cv2.findContours(imgClose, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    finalContours = []
    for i in contours:
        area = cv2.contourArea(i)
        if area > minArea:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            bbox = cv2.boundingRect(approx)
            if filter > 0:
                if len(approx) == filter:
                    finalContours.append([len(approx), area, approx, bbox, i])
            else:
                finalContours.append([len(approx), area, approx, bbox, i])

    finalContours = sorted(finalContours, key=lambda x: x[1], reverse=True)

    if draw:
        for con in finalContours:
            x, y, w, h = con[3]
            cv2.rectangle(imgDraw, (x, y), (x + w, y + h), (255, 0, 255), 3)
    return imgDraw, finalContours



def getRoi(img, contours):
    roiList = []
    for con in contours:
        x, y, w, h = con[3]
        roiList.append(img[y:y+h, x:x+w])
    return roiList


def roiDisplay(roiList):
    for x, roi in enumerate(roiList):
        roi = cv2.resize(roi, (0, 0), None, 2, 2)
        cv2.imshow(f"Cropped Image {x}", roi)


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

