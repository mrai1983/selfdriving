from PIL import Image
import select
import v4l2capture
import cv2
import numpy

cv2.namedWindow('test')
# Open the video device.
video = v4l2capture.Video_device("/dev/video1")

# Suggest an image size to the device. The device may choose and
# return another size if it doesn't support the suggested one.
size_x, size_y = video.set_format(1280, 1024)

# Create a buffer to store image data in. This must be done before
# calling 'start' if v4l2capture is compiled with libv4l2. Otherwise
# raises IOError.
video.create_buffers(30)

# Send the buffer to the device. Some devices require this to be done
# before calling 'start'.
video.queue_all_buffers()

# Start the device. This lights the LED if it's a camera that has one.
video.start()

while (1):
    # Wait for the device to fill the buffer.
    select.select((video,), (), ())

    # The rest is easy :-)
    image_data = video.read()

    image = Image.frombytes("RGB", (size_x, size_y), image_data)


    open_cv_image = numpy.array(image)
    open_cv_image = open_cv_image[:, :, ::-1].copy()

    cv2.imshow('test', open_cv_image)

    #image.save("image.jpg")

    cv2.waitKey(1)

video.close()

print "Saved image.jpg (Size: " + str(size_x) + " x " + str(size_y) + ")"