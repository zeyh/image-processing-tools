# fast natural style transfer ref: https://github.com/misgod/fast-neural-style-keras
# poission blending ref: https://www.learnopencv.com/seamless-cloning-using-opencv-python-cpp/

import cv2
import numpy as np 
from scipy.signal import convolve2d
from skimage import io, color, data, restoration
#https://stackoverflow.com/questions/55009855/iterating-over-square-submatrices-in-multidimensional-numpy-array
from skimage.util import view_as_windows
import matplotlib as plt

def Laplacian_val(img):
    '''
    ref: https://www.jianshu.com/p/b0fa7a8eba78
    '''
    # img = cv2.imread(imgPath, 0)
    laplacian = cv2.Laplacian(img, cv2.CV_64F).var()
    return laplacian


def edgedetecting(img):
    '''
    ref: https://blog.sicara.com/opencv-edge-detection-tutorial-7c3303f10788
    '''
    # Converting the image to grayscale.
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Using the Canny filter to get contours
    edges = cv2.Canny(gray, 20, 30)
    # Using the Canny filter with different parameters
    edges_high_thresh = cv2.Canny(gray, 60, 120)
    # Stacking the images to print them together
    # For comparison
    images = np.hstack((gray, edges, edges_high_thresh))
    cv2.imwrite("images/poisson/mask2.jpg", edges_high_thresh)

    return images

# def findcontour(img):
#     '''
#     ref: https://bytefish.de/blog/extracting_contours_with_opencv/
#     '''
#     img_canny = edgedetecting(img)
#     contours = cv2.findContours(img_canny, contours, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_NONE);


def filledcountour(img, contour):
    img = np.zeros( (img.shape[0],img.shape[1]) ) # create a single channel 200x200 pixel black image 
    mask = cv2.fillPoly(img, pts =[contour], color=(255,255,255))
    cv2.imwrite("images/poisson/countor.jpg", mask)
    return mask

def threshold(img):
    '''
    ref: https://docs.opencv.org/3.4.0/d7/d4d/tutorial_py_thresholding.html
    '''
     # Converting the image to grayscale.
    img = cv2.medianBlur(img,5).astype('uint8')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)
    cv2.imwrite("images/poisson/threshold.jpg", th3)
    

def edgeDetection(file_dir):
    '''
    https://blog.sicara.com/opencv-edge-detection-tutorial-7c3303f10788
    '''
    fgbg = cv2.createBackgroundSubtractorMOG2(
    history=10,
    varThreshold=2,
    detectShadows=False)
    gray = cv2.imread(file_dir, cv2.IMREAD_GRAYSCALE)
    # Extract the foreground
    edges_foreground = cv2.bilateralFilter(gray, 9, 75, 75)
    foreground = fgbg.apply(edges_foreground)
    # Smooth out to get the moving area
    kernel = np.ones((50,50),np.uint8)
    foreground = cv2.morphologyEx(foreground, cv2.MORPH_CLOSE, kernel)
    # Applying static edge extraction
    edges_foreground = cv2.bilateralFilter(gray, 9, 75, 75)
    edges_filtered = cv2.Canny(edges_foreground, 60, 120)
    # Crop off the edges out of the moving area
    cropped = (foreground // 255) * edges_filtered
    # Stacking the images to print them together for comparison
    images = np.hstack((gray, edges_filtered, cropped))
    cv2.imwrite("images/poisson/new_win.jpg", images )


def fillpartial(file_dir):
    S = 4
    ratio = 5
    img = cv2.imread(file_dir, cv2.IMREAD_GRAYSCALE)

    cols, rows = img.shape
    count = 0
    l = []
    new_image = np.zeros([cols, rows], dtype=int)
    print(new_image)
    # new_image = []
    for i in range(0, cols):
        for j in range(0, rows): 
            if(i+S <= cols and j+S <= rows):
                sub = img[i:i+S, j:j+S]
                
                l_val = Laplacian_val(sub)
                l.append(l_val)
                if(l_val >= 120000):
                    #make it white filled with 000
                    temp_matrix = np.full((S, S), 255)
                    # print(temp_matrix)
                    img[i:i+S, j:j+S] = temp_matrix
                    new_image[i:i+S, j:j+S] = temp_matrix
                    print(Laplacian_val(img[i:i+S, j:j+S] ))
                    # new_image = np.concatenate(new_image,temp_matrix)
                # else:
                #     temp_matrix = np.full((S, S), 0)
                #     img[i:i+S, j:j+S] = temp_matrix
                    # pass
                    #keep the same
            j = j+S
        i = i+S

            # else:
            #     new_image.append(img[i][j])
            # count +=1 
    maxelement = np.amax(l)
    print(maxelement)
    counts, bins = np.histogram(l, bins=30, range=(0, int(maxelement)))
    print(counts, bins)
    print(count)

    # new_image = cv2.bitwise_not(new_image) #flip the mask

    #     temp_img = view_as_windows(img, window_shape=(int(rows/ratio), int(cols/ratio)), step=1)
    cv2.imwrite("images/poisson/new_win.jpg", new_image )

    return new_image


def main():
    # Read images
    src = cv2.imread("images/poisson/r2.jpg")
    dst = cv2.imread("images/poisson/r1.jpg")


    #chop image
    top = 200
    height = 190
    left = 5
    width = 600

    src = src[ top:top+height,left:left+width]
    portion = 3
    resized_size = (int((src.shape[1])/portion) , int((src.shape[0])/portion))
    src = cv2.resize(src,resized_size)




    #gaussian bluring
    kernel = np.ones((3,3),np.float32)/9
    src = cv2.filter2D(src,-1,kernel)

    #write to disk
    status = cv2.imwrite("images/poisson/chopped.jpg", src)



    print(Laplacian_val(src), Laplacian_val(dst))
    print(src.shape)
    print(dst.shape)

    #detect edge
    kernel2 = np.ones((5,5),np.float32)/25 #no need to add another blurring filter for this case
    src_blurred = cv2.filter2D(src,-1,kernel2)
    contour = edgedetecting(src)
    threshold(src)


    # filledcountour(src, contour)
    mask_countor_import_dir = "images/poisson/mask2.jpg"
    mask_filled = fillpartial(mask_countor_import_dir)

    # # Create a rough mask around the ship
    src_mask = np.zeros(src.shape, src.dtype)
    mask_countor = [ [0,0], [300,0], [0,800], [0,90]]
    poly = np.array(list(mask_countor), np.int32)
    cv2.fillPoly(src_mask, [poly], (255, 255, 255))

    #sanity check photomask
    cv2.imwrite("images/poisson/mask1.jpg", src_mask)
    cv2.imwrite("images/poisson/mask2.jpg", mask_filled)

    # This is where the CENTER of the airplane will be placed
    center = (410,240)

    
    # Clone seamlessly. #poisson dist
    output = cv2.seamlessClone(src, dst, src_mask, center, cv2.NORMAL_CLONE) #MIXED_CLONE
    output2 = cv2.seamlessClone(src, dst, mask_filled, center, cv2.NORMAL_CLONE)
    
    # Save result
    cv2.imwrite("images/poisson/opencv-seamless-cloning-example.jpg", output)
    cv2.imwrite("images/poisson/opencv-seamless-cloning-example_1.jpg", output2)



main()