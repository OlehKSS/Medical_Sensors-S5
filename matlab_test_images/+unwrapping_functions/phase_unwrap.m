
function image_unwrapped = phase_unwrap(image_wrapped)
    [N,M] = size(image_wrapped);
    image_unwrapped = image_wrapped;
    %Unwrap all the rows of the image
    for i=1:N
        image_unwrapped(i,:) = unwrap(image_unwrapped(i,:));
    end
    %Then sequentially unwrap all the columns one at a time
    for i=1:M
        image_unwrapped(:,i) = unwrap(image_unwrapped(:,i));
    end
end