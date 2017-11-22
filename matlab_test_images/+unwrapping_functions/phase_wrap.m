function image_wrapped = phase_wrap(image_unwrapped)
    %wrap the 2D image using atan2 which takes into account the signs of both x
    %and y arguemnts
    image_wrapped = atan2(sin(image_unwrapped), cos(image_unwrapped));
end