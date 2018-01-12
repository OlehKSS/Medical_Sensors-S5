#Create test images, wrap them to match the given images, and save the originals

import os, sys
import numpy
from matplotlib import pyplot, cm
from math import pi
from skimage import util, io
from PIL import Image

#Function which accepts an image and a file name (in quotes) and saves the image
#as uint8 jpg for easy viewing.
#def save_image_as_jpg (imgdata,name):
#    imgdata = imgdata/numpy.amax(imgdata);
#    imgdata_uint8 = util.img_as_ubyte(imgdata);
#    imgdata_uint8 = Image.fromarray(imgdata_uint8)
#    imgdata_uint8.save(name + 'jpeg')

#Function which accepts an unwrapped image and wraps it to (-pi,pi). Returns an image
#with values between (0,4095) like the given images.
def wrap_image (unwrapped_image):
    wrapped_image = numpy.arctan2(numpy.sin(unwrapped_image), numpy.cos(unwrapped_image));
    wrapped_image =  4095./2./pi * (pi + wrapped_image);
    wrapped_image = wrapped_image.astype(int);
    return (wrapped_image)

#Function which accepts an image and variance, converts the image to floating numbers between 0 and 1 and applies gaussian noise a the specified variance. Outputs the noisy image.
#Input/output image uint12 format
def add_gaussian_noise (image, variance):
    image = image/4095.
    noisy_image = util.random_noise(image, mode = 'gaussian', var = variance)
    noisy_image = noisy_image *4095;
    noisy_image = noisy_image.astype(int);
    return (noisy_image)


#Define an image that is 256x256 pixels, use linespace to define N equally spaced samples
#in the interval (-3,3). Then use the bullseye function to fill the image with values between
# (0, 24).
N = 256;
tx = numpy.linspace(-3,3,N);
ty = numpy.linspace(-3,3,N);
x,y = numpy.meshgrid(tx,ty);
bullseye = 24 * numpy.exp(-0.5*(x**2 + y**2));

#pyplot.imshow(bullseye, cmap = cm.Greys_r)
#pyplot.show()

#Save the original image as uint8 for easy viewing later
#save_image_as_jpg (bullseye, 'bullseye')

#Wrap the bullseye image to wrap the image like we have been given and
#convert the image to 12 bit unsigned integer values.
bullseye_wrapped = wrap_image(bullseye)

#pyplot.imshow(bullseye_wrapped, cmap = cm.Greys_r)
#pyplot.show()

#Add gaussian random noise to the image, with SD varying from 0.62 rd to 1.52 rd, as
#in the paper
bullseye_wrapped_noise1 = add_gaussian_noise(bullseye_wrapped, 0.0001)
bullseye_wrapped_noise2 = add_gaussian_noise(bullseye_wrapped, 0.001)
bullseye_wrapped_noise3 = add_gaussian_noise(bullseye_wrapped, 0.03)
bullseye_wrapped_noise4 = add_gaussian_noise(bullseye_wrapped, 0.04)
pyplot.imshow(bullseye_wrapped_noise1, cmap = cm.Greys_r)
pyplot.imshow(bullseye_wrapped_noise2, cmap = cm.Greys_r)
pyplot.show()
pyplot.imshow(bullseye_wrapped_noise3, cmap = cm.Greys_r)
pyplot.imshow(bullseye_wrapped_noise4, cmap = cm.Greys_r)


#Define another test image, this time using linspace
x, y = numpy.meshgrid(tx, ty);
swirls =  0.1*x + 0.01*y;

pyplot.imshow(swirls, cmap = cm.Greys_r)
pyplot.show()


