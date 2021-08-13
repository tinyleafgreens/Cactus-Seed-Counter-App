import cv2
import numpy
import matplotlib.pyplot as plt

def count_photo(filepath):
    image = cv2.imread(filepath)
    original_path = '/storage/emulated/0/DCIM/Camera/cactusseedcounter_original.png'
    original_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.imwrite(original_path, image)
    #image = cv2.resize(img, dim)

    copy = original_image.copy()

    # Finding the contour of the paper

    gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    #plt.imshow(original_image, cmap='gray')
    #plt.show()

    ret, th = cv2.threshold(blurred,
                            172, #Threshold Value
                            255, # max value assigned to pixel exceeding threshold (black)
                            cv2.THRESH_BINARY + cv2.ADAPTIVE_THRESH_GAUSSIAN_C + cv2.THRESH_OTSU)


    #plt.imshow(th - 255, cmap='gray')
    #plt.show()

    #dilated = cv2.dilate(th-255, (5, 5), iterations=1)

    (cnts, _) = cv2.findContours(th - 255, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    max_area = max(cnts, key=cv2.contourArea)
    #cv2.drawContours(copy, max_area, -1, (255, 0, 0), 5)
    #plt.imshow(copy)
    #plt.show()

    # Removing anything that is NOT the contour
    '''
        stencil = numpy.zeros(copy.shape).astype(copy.dtype)
        contours = [max_area]
        color = [255, 255, 255]
        cv2.fillPoly(stencil, contours, color)
        result = cv2.bitwise_and(copy, stencil)
        plt.imshow(result, cmap='gray')
        #plt.show()
    '''
    fill_color = [255, 255, 255] # any BGR color value to fill with
    mask_value = 255
    stencil = numpy.zeros(copy.shape[:-1]).astype(numpy.uint8)
    contours = [max_area]
    cv2.fillPoly(stencil, contours, mask_value)

    sel = stencil != mask_value  # select everything that is not mask_value
    copy[sel] = fill_color  # and fill it with fill_color
    #plt.imshow(copy, cmap='gray')
    #plt.show()


# This is the portion which counts the seeds

    gray_image = cv2.cvtColor(copy, cv2.COLOR_BGR2GRAY)
    #plt.imshow(gray_image, cmap='gray')
    #plt.show()


    kernel_window_size = (5, 5)
    #blur = cv2.GaussianBlur(gray_image, kernel_window_size, 3)
    #plt.imshow(blur, cmap='gray')



    _, threshold_image = cv2.threshold(gray_image, 60, 255, cv2.THRESH_BINARY_INV + cv2.ADAPTIVE_THRESH_GAUSSIAN_C)
    #threshold_image = cv2.adaptiveThreshold(gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 18)
    #plt.imshow(threshold_image, cmap='gray')
    #plt.show()
    '''
    kernel_window_size = (5, 5)
    blur = cv2.GaussianBlur(threshold_image, kernel_window_size, 3)
    plt.imshow(blur, cmap='gray')
    #plt.show()
    '''
    
    min_edge_threshold = 255/3
    max_edge_threshold = 255
    kernel_size_of_sobel_filter = 3
    canny = cv2.Canny(threshold_image, min_edge_threshold, max_edge_threshold, kernel_size_of_sobel_filter)
    #plt.imshow(canny, cmap='gray')
    #plt.show()

    iterations = 1
    kernel_size_dilate = (5, 5)
    dilated = cv2.dilate(canny, kernel_size_dilate, iterations=iterations)
    #cv2.imwrite(contour_path, dilated)
    #plt.imshow(dilated, cmap='gray')
    #plt.show()

    (cnt, heirarchy) = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    #RETR_EXTERNAL says we'll be considering external contours only, and not internal ones
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    number_contours_to_draw = -1
    color_of_contours = (255, 0, 255)
    contour_thickness = 2

    cv2.drawContours(copy, cnt, number_contours_to_draw, color_of_contours, contour_thickness)
    #plt.imshow(copy)
    #plt.show()
    seed_count = len(cnt)
    contour_path = '/storage/emulated/0/DCIM/Camera/cactusseedcounter_contours.png'
    copy2 = cv2.cvtColor(copy, cv2.COLOR_BGR2RGB)
    cv2.imwrite(contour_path, copy2)
    uncropped_image_used = False
    return seed_count, uncropped_image_used, contour_path, original_path

