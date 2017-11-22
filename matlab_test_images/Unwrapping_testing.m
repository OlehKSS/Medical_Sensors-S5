close all
clear variables
clc

import unwrapping_functions.*;

imgdata = double(imread('607_0008.jpg'));
imgdata = (imgdata - 128.)*pi/128;

imgdata_unwrapped = phase_unwrap(imgdata);
%figure, subplot(1,2,1), colormap(gray(256)), imagesc(imgdata)
%subplot(1,2,2), colormap(gray(256)), imagesc(imgdata_unwrapped,[-3.14,3.14])


%Generate an image that is lighter in the center and darker on the outside
%and wrap the image. The phase_wrap function produces an image whose 
%pixels are in the range (-pi,pi) so stretch the values linerly so they
%match those used in the python algorithm (0,4096)
N = 256;
tx = linspace(-3,3,N);
ty = linspace(-3,3,N);
[x,y]=meshgrid(tx,ty);
bullseye = 24 * exp(-0.5*(x.^2 + y.^2));
bullseye_wrapped = 4095./2./pi * (pi + (phase_wrap(bullseye)));
%figure, subplot(1,2,1), colormap(gray(256)), imagesc(bullseye)
%subplot(1,2,2), colormap(gray(256)), imagesc(bullseye_wrapped)

%Generate an image with some darker peaks and lighter areas, wrap the
%image, and stretch the range again
[x,y]=meshgrid(1:N);
swirls = 2*peaks(N) + 0.1*x + 0.01*y;
swirls_wrapped = 4095./2./pi * (pi + phase_wrap(swirls));
%figure, subplot(1,2,1), colormap(gray(256)), imagesc(swirls)
%subplot(1,2,2), colormap(gray(256)), imagesc(swirls_wrapped)

%Stretch the test images original images to the range (0,255) to be
%displayed easily
bullseye = 255. / (max(max(bullseye))) * (bullseye - min(min(bullseye)));
swirls = 255. / (max(max(swirls))) * (swirls - min(min(swirls)));

swirls = uint8(swirls);
bullseye = uint8(bullseye);

%Save the images in the same folder they originally came from
%in the 16 bit unsigned format (for wrapped) and 8 bit (for
%original)
swirls_wrapped = uint16(swirls_wrapped);
bullseye_wrapped = uint16(bullseye_wrapped);

imwrite(swirls, 'swirls.jpg');
imwrite(swirls_wrapped, 'swirls_wrapped.jpg','BitDepth',12);
imwrite(bullseye, 'bullseye.jpg');
imwrite(bullseye_wrapped, 'bullseye_wrapped.jpg','BitDepth',12);