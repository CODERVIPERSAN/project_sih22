

import cv2 as cv
import numpy as np


def edge_detection(img, th1, th2):
    img = cv.GaussianBlur(img,(3,3),1)
    canny_image = cv.Canny(img, th1, th2, cv.LINE_AA)
    return canny_image


def find_threshold_value(img):
    gray_scale = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret, threshold_image = cv.threshold(gray_scale, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    return ret


def contour_edge(img):
    # thresh_val = find_threshold_value(img)
    # gray_image = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    # threshold_image = cv.threshold(img,thresh_val-10,thresh_val+10)
    contours, hierarchy = cv.findContours(img,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    result_image = img.copy()
    # print(len(contours))
    cv.drawContours(result_image,contours,-1,(0,0,0),1,cv.LINE_8)
    return result_image


def increase_edge_thickness(img):
    # kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
    # img = cv.bitwise_not(img)
    kernel = np.ones((3,3),np.uint8)
    result_image = cv.erode(img,kernel=kernel,iterations=1)
    # result_image = cv.bitwise_not(result_image)
    return result_image


def add_color(orginal_image,border_image):
    # for i in range(border_image.shape[0]):
    #     for j in range(border_image.shape[1]):
    #         if border_image[i][j] != 255:
    #             orginal_image[i][j] = [border_image[i][j],border_image[i][j],border_image[i][j]]

    # border_image = np.float64(border_image)
    # border_image = (border_image/255)
    # for i in range(border_image.shape[0]):
    #     for j in range(border_image.shape[1]):
    #         orginal_image[i][j] = orginal_image[i,j,:] * border_image[i][j]

    border_image = cv.cvtColor(border_image,cv.COLOR_GRAY2BGR)
    border_image = np.float64(border_image) / 255
    result = np.uint8(orginal_image * border_image)
    return result


def convert(filename):
    image = cv.imread(filename, cv.IMREAD_COLOR)
    # image = cv.resize(image,(300,300))
    image= cv.cvtColor(image,cv.COLOR_RGB2BGR)
    result_value = find_threshold_value(image)
    result_image = edge_detection(image, result_value-25, result_value+25)
    result_image = cv.bitwise_not(result_image)
    result_image = contour_edge(result_image)
    # result_image = add_color(image,result_image)
    # result_image = increase_edge_thickness(result_image)
    # print(filename)
    cv.imwrite(f"static/tactile/result.jpg",result_image)
    # cv.imshow('result', result_image)
    # while True:
    #     if cv.waitKey(1) & 0xFF == ord('q'):
    #         break
    # cv.destroyAllWindows()
    # sult_image = cv.dilate(img, kernel,iterations=1)