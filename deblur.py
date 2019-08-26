#code ref: https://stackoverflow.com/questions/41019222/deblur-an-image-using-scikit-image

#csdn blog: https://blog.csdn.net/weixin_41923961/article/details/80113849
#papers: https://www.sciencedirect.com/science/article/pii/S2213020916301823#aep-article-footnote-id4

# import cv2
import numpy as np
from skimage import io, color, data, restoration
from scipy.signal import convolve2d
import numpy as np

def matlab_style_gauss2D(shape=(3,3),sigma=0.5):
    """
    2D gaussian mask - should give the same result as MATLAB's
    fspecial('gaussian',[shape],[sigma])
    """
    m,n = [(ss-1.)/2. for ss in shape]
    y,x = np.ogrid[-m:m+1,-n:n+1]
    h = np.exp( -(x*x + y*y) / (2.*sigma*sigma) )
    h[ h < np.finfo(h.dtype).eps*h.max() ] = 0
    sumh = h.sum()
    if sumh != 0:
        h /= sumh
    return h

# I = cv2.imread('test3_deblur.jpg')
psf = matlab_style_gauss2D((5,5),1)
print(psf)
psf_v2 = np.ones((5, 5)) / 25
print(psf_v2)
noise_mean = 0
noise_var = 0.00001


filename = "test_denoised_1.jpg"
img = io.imread(filename)
img = color.rgb2gray(img)
# io.imsave('test_denoised_check.jpg', img)

img_blurred = convolve2d(img, psf, 'same')
img_blurred_v2 = convolve2d(img, psf_v2, 'same')
# print("-----------")
# print(img.shape, img)
# print("-----------")
# print(img_blurred.shape, img_blurred)
# print("-----------")
# print(img_blurred_v2.shape, img_blurred_v2)
# # io.imsave('test_denoised_check_1.jpg', img)
print(img.std())
img += 0.1 * img.std() * np.random.standard_normal(img.shape)

deconvolved_img = restoration.wiener(img, psf, 0.1)
io.imsave('test_denoised_check_1.jpg', deconvolved_img)
# img = cv2.deconvreg(I,PSF)
# img2 = cv2.deconvblind(I, PSF, 100)
# img3 = cv2.deconvlucy(I, PSF, 100)
print('fin.')

