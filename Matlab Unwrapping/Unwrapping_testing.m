close all
clear variables
clc

import unwrapping_functions.*;

imgdata = imread('608_0001_echo1_coro.jpg');

%Generate an image that is lighter in the center and darker on the outside
N = 256;
tx = linspace(-3,3,N);
ty = linspace(-3,3,N);
[x,y]=meshgrid(tx,ty);
bullseye = 40*exp(-0.5*(x.^2 + y.^2));
figure, subplot(1,2,1), colormap(gray(256)), imagesc(bullseye)
bullseye_wrapped = phase_wrap(bullseye);
subplot(1,2,2), colormap(gray(256)), imagesc(bullseye_wrapped)

[x,y]=meshgrid(1:N);
swirls = 2*peaks(N) + 0.1*x + 0.01*y;
swirls_wrapped = phase_wrap(swirls);
figure, subplot(1,2,1), colormap(gray(256)), imagesc(swirls)
subplot(1,2,2), colormap(gray(256)), imagesc(swirls_wrapped)

%Add gaussian noise to the wrapped phase images
bullseye_noise = imnoise(bullseye_wrapped, 'gaussian',0, (0.62)^2/(255)^2);
figure, subplot(1,2,1), colormap(gray(256)), imagesc(bullseye_noise)
subplot(1,2,2), colormap(gray(256)), imagesc(bullseye_wrapped)

%Unwrap the image using the Itoh algorithm: the first method is performed
%by first sequentially unwrapping the all rows, one at a time.
image1_unwrapped = phase_unwrap(bullseye_wrapped);
%subplot(1,3,3), colormap(gray(256)), imagesc(image1_unwrapped)
%title('Unwrapped phase image using the Itoh algorithm: the first method')
%xlabel('Pixels'), ylabel('Pixels')
