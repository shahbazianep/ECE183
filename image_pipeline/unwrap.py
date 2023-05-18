import cv2
import numpy as np
from unwrap_labels import LabelUnwrapper

DEBUG = 1
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
YELLOW_COLOR = (0, 255, 255)
RED_COLOR = (0, 0, 255)

def unwrap(IMAGE_NAME):
    # Load the image
    image = cv2.imread(IMAGE_NAME)
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #cv2.imshow('image', image)
    if DEBUG:
        cv2.imwrite("./processed/image_gray.jpg", image_gray)

    blur = cv2.GaussianBlur(image_gray, ksize=(13,13), sigmaX=0)
    ret, thresh1 = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)

    edged = cv2.Canny(blur, 10, 250)
    #cv2.imshow('Edged', edged)
    if DEBUG:
        cv2.imwrite("./processed/edged_test.jpg", edged)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    #cv2.imshow('closed', closed)
    if DEBUG:
        cv2.imwrite("./processed/closed_test.jpg", closed)

    contours, _ = cv2.findContours(closed.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    total = 0

    # contours_image = cv2.drawContours(image, contours, -1, (0,255,0), 3)
    # cv2.imwrite("contours_image.jpg", contours_image)

    contours_xy = np.array(contours)
    contours_xy.shape

    x_min, x_max = 0,0
    value = list()
    for i in range(len(contours_xy)):
        for j in range(len(contours_xy[i])):
            value.append(contours_xy[i][j][0][0]) #네번째 괄호가 0일때 x의 값
            x_min = min(value)
            x_max = max(value)
    if DEBUG:
        print("x_min:", x_min)
        print("x_max:", x_max)
    
    # y의 min과 max 찾기
    y_min, y_max = 0,0
    value = list()
    for i in range(len(contours_xy)):
        for j in range(len(contours_xy[i])):
            value.append(contours_xy[i][j][0][1]) #네번째 괄호가 0일때 x의 값
            y_min = min(value)
            y_max = max(value)
    if DEBUG:
        print("y_min:", y_min)
        print("y_min:", y_max)
        print("\n")

    x = x_min
    y = y_min
    w = x_max-x_min
    h = y_max-y_min

    height, _, _ = image.shape 

    # img_trim = image[0:height, x:x+w]
    img_trim = image[y-30:height-50, x:x+w]
    
    if DEBUG:
        cv2.imwrite("./processed./trimmed.jpg", img_trim)
    
    shape = {"tag": "label", "shape": [{"x": 0.012232142857142842+0.05, "y": 0.2219140625+0.03},
                                        {"x": 0.48655701811449864, "y": 0.14404355243445227+0.12},
                                        {"x": 0.9632539682539681-0.05, "y": 0.2171875+0.03},
                                        {"x": 0.9466567460317459-0.05, "y": 0.7276953125+0.07},
                                        {"x": 0.48447501824501454, "y": 0.7952298867391453+0.12},
                                        {"x": 0.023134920634920626+0.05, "y": 0.7258984375+0.07}]}

    points = []
    for point in shape['shape']:
        points.append([point['x'], point['y']])

    # imcv = cv2.imread('org_trim.jpg', cv2.IMREAD_UNCHANGED)

    unwrapper = LabelUnwrapper(src_image=img_trim, percent_points=points)

    dst_image = unwrapper.unwrap()
    for point in unwrapper.points:
        cv2.line(unwrapper.src_image, tuple(point), tuple(point), color=YELLOW_COLOR, thickness=3)

    if DEBUG:
        unwrapper.draw_mesh()
        unwrapper.draw_mask()
        cv2.imwrite("./processed/image_with_mask.png", img_trim)
        cv2.imwrite("./processed/unwrapped.jpg", dst_image)

    # h_d, w_d, _ = dst_image.shape 
    w_crop = 270
    dst_image_cropped = dst_image[0:dst_image.shape[0], w_crop:dst_image.shape[1]-w_crop]

    return dst_image_cropped

    # # Perform OCR
    # text = pytesseract.image_to_string(image2)

    # # Display the output
    # print(text)