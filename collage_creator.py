"""
Module: collage_creator

A program to create an Andy Warhol-style collage.

Author:Rodolfo Lopez (rodolfolopez@sandiego.edu)
"""

import math

import comp110_image


def flip_filter(init_img):
    """
    Reflects the image over its horizontal axis.

    Parameters:
    init_img (type: Picture) - The initial image to be flipped.

    Returns:
    Picture - A new image that is flipped across its horizontal axis.
    """

    img = init_img.copy()

    w = img.getWidth()
    h = img.getHeight()

    max_pix = h - 1
    for row in range(h // 2):
        for col in range(w):

            top_pix = img.getPixel(col, row)
            bottom_pix = img.getPixel(col, max_pix - row)

            top_init_red = top_pix.getRed()
            top_pix.setRed(bottom_pix.getRed())
            bottom_pix.setRed(top_init_red)

            top_init_green = top_pix.getGreen()
            top_pix.setGreen(bottom_pix.getGreen())
            bottom_pix.setGreen(top_init_green)

            top_init_blue = top_pix.getBlue()
            top_pix.setBlue(bottom_pix.getBlue())
            bottom_pix.setBlue(top_init_blue)

    return img


def mirror_horizontal(init_img):
    """
    Generates a new image that mirrors the original along the horizontal axis.

    Parameters:
    init_img (type: Picture) - The initial image to be mirrored.

    Returns:
    Picture - A new image that is mirrored across its horizontal axis.
    """

    img = init_img.copy()

    init_w = img.getWidth()
    init_h = img.getHeight()

    for x in range(init_h // 2):
        for y in range(init_w):

            top_pix = img.getPixel(x, y)
            img.setPixel(x, init_h - 1 - y, top_pix)

    return img


def assemble_collage(filter_pics):
    """
    Combines the filtered images to create a unified 3x2 collage.

    Parameters:
    filter_pics (type: List[Picture]) - A list of 6 filtered images.

    Returns:
    Picture - A new image containing the 3x2 collage of filtered images.
    """

    w = filter_pics[0].getWidth()
    h = filter_pics[0].getHeight()

    canvas = comp110_image.Picture(3 * w, 2 * h)

    copy_to(filter_pics[0], canvas, 0, 0)
    copy_to(filter_pics[1], canvas, w, 0)
    copy_to(filter_pics[2], canvas, 2 * w, 0)
    copy_to(filter_pics[3], canvas, 0, h)
    copy_to(filter_pics[4], canvas, w, h)
    copy_to(filter_pics[5], canvas, 2 * w, h)

    return canvas


def copy_to(src_img, dest_img, start_x, start_y):
    """
    Copies one image into another, start at the given starting coordinate.

    DO NOT MODIFY THIS FUNCTION!!!

    Parameters:
    src_img (type: Picture) - The picture to copy.
    dest_img (type: Picture) - The picture to copy into.
    start_x (type: int) - The column where we start copying to dest_img.
    start_y (type: int) - The row where we start copying to dest_img.
    """

    for x in range(src_img.getWidth()):
        for y in range(src_img.getHeight()):
            srcPixel = src_img.getPixel(x, y)
            dest_img.setPixel(x + start_x, y + start_y, srcPixel)


def grayscale_filter(init_img):
    """
    Converts the image to grayscale by applying the 'grayscale' filter.

    Parameters:
    init_img (type: Picture) - The initial image to be converted to grayscale.

    Returns:
    Picture - A new image with the grayscale filter applied.
    """

    img = init_img.copy()
    for y in range(img.getHeight()):
        for x in range(img.getWidth()):
            pix = img.getPixel(x, y)
            intensity_sum = pix.getRed() + pix.getGreen() + pix.getBlue()
            rgb_avg = intensity_sum // 3

            pix.setColor((rgb_avg, rgb_avg, rgb_avg))

    return img


def apply_kernel(img, convolve_img, x, y, kern):
    """
    Applies a 3x3 convolution kernel to an individual pixel within the image.

    Parameters:
    img (type: Picture) - The original image.
    convolve_img (type: Picture) - The image being created by convolution.
    x (type: int) - The x-coordinate of the pixel being processed.
    y (type: int) - The y-coordinate of the pixel being processed.
    kern (type: List[List[float]]) - The 3x3 convolution kernel.

    Returns:
    None
    """

    red_val = 0
    green_val = 0
    blue_val = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            pix = img.getPixel(x + i, y + i)
            kern_val = kern[j + 1][i + 1]
            red_val += pix.getRed() * kern_val
            green_val += pix.getGreen() * kern_val
            blue_val += pix.getBlue() * kern_val

    if red_val > 255:
        red_val = 255
    elif red_val < 0:
        red_val = 0

    if green_val > 255:
        green_val = 255
    elif green_val < 0:
        green_val = 0

    if blue_val > 255:
        blue_val = 255
    elif blue_val < 0:
        blue_val = 0

    convolve_img.setPixel(x, y, (red_val, green_val, blue_val))


def convolution(img, kern):
    """
    Applies the specified convolution kernel to every pixel in the provided image.

    Parameters:
    img (type: Picture) - The image to apply convolution to.
    kern (type: List[List[float]]) - The 3x3 convolution kernel.

    Returns:
    Picture - A new image with the convolution applied.
    """

    convolve_img = img.copy()

    for x in range(1, img.getWidth() - 1):
        for y in range(1, img.getHeight() - 1):
            apply_kernel(img, convolve_img, x, y, kern)

    return convolve_img


def negative_filter(init_img):
    """
    Transforms the image into its negative representation.

    Parameters:
    init_img (type: Picture) - The initial image to be converted to negative.

    Returns:
    Picture - A new image with the negative filter applied.
    """

    img = init_img.copy()
    for y in range(img.getHeight()):
        for x in range(img.getWidth()):
            pix = img.getPixel(x, y)
            pix.setRed(255 - pix.getRed())
            pix.setGreen(255 - pix.getGreen())
            pix.setBlue(255 - pix.getBlue())

    return img


def sunset_filter(init_img):
    """
    Applies a filter that simulates a sunset effect to the image.

    Parameters:
    init_img (type: Picture) - The initial image to have the sunset filter applied.

    Returns:
    Picture - A new image with the sunset filter applied.
    """

    img = init_img.copy()
    for y in range(img.getHeight()):
        for x in range(img.getWidth()):
            pix = img.getPixel(x, y)
            pix.setGreen(0.7 * pix.getGreen())
            pix.setBlue(0.7 * pix.getBlue())

    return img


def unique_filter(init_img):
    """
    Applies a filter that reduces the number of colors in the image, creating a "posterized" effect.

    Parameters:
    init_img (type: Picture) - The initial image to be posterized.

    Returns:
    Picture - A new image with the posterized filter applied.
    """

    img = init_img.copy()

    for x in range(img.getWidth()):
        for y in range(img.getHeight()):
            pix = img.getPixel(x, y)
            init_red = pix.getRed()
            init_green = pix.getGreen()
            init_blue = pix.getBlue()

            if init_red < 63:
                pix.setRed(95)
            elif init_red < 128:
                pix.setRed(159)
            else:
                pix.setRed(223)

            if init_green < 63:
                pix.setGreen(95)
            elif init_green < 128:
                pix.setGreen(159)
            else:
                pix.setGreen(223)

            if init_blue < 63:
                pix.setBlue(95)
            elif init_blue < 128:
                pix.setBlue(159)
            else:
                pix.setBlue(223)

    return img


def create_filtered_pics(img):
    """
    Generates and provides six different filtered variations of the specified image.

    Parameters:
    img (type: Picture) - The original image to create filtered versions from.

    Returns:
    Tuple[Picture, Picture, Picture, Picture, Picture, Picture] - A tuple containing six filtered versions of the image.
    """

    posterize = unique_filter(img)

    sunset = sunset_filter(img)
    sunset = mirror_horizontal(sunset)

    negative = negative_filter(img)

    blur_kern = [
        [1 / 16, 2 / 16, 1 / 16],
        [2 / 16, 4 / 16, 2 / 16],
        [1 / 16, 2 / 16, 1 / 16],
    ]
    blur = convolution(img, blur_kern)
    blur = flip_filter(blur)

    edge_kern = [
        [-1, -1, -1],
        [-1, 8, -1],
        [-1, -1, -1],
    ]
    edge = convolution(img, edge_kern)

    gray = grayscale_filter(img)
    gray = flip_filter(gray)

    return (posterize, sunset, negative, blur, edge, gray)


def shrink(img, fac):
    """
    Reduces the size of the specified image based on the provided factor.

    Parameters:
    img (type: Picture) - The image to be shrunk.
    fac (type: int) - The factor by which to shrink the image.

    Returns:
    Picture - A new image that is shrunk by the given factor.
    """

    shrunk_img = comp110_image.Picture(img.getWidth() // fac, img.getHeight() // fac)

    for x in range(shrunk_img.getWidth()):
        for y in range(shrunk_img.getHeight()):
            init_x = x * fac
            init_y = y * fac
            init_pixel = img.getPixel(init_x, init_y)
            shrunk_img.setPixel(x, y, init_pixel)

    return shrunk_img


def get_shrink_factor(img, targ_w, targ_h):
    """
    Calculates the scaling factor needed to resize the image to the specified width and height.

    Parameters:
    img (type: Picture) - The original image.
    targ_w (type: int) - The target width.
    targ_h (type: int) - The target height.

    Returns:
    int - The factor by which the image should be shrunk.
    """

    fac_w = int(math.ceil(img.getWidth() / targ_w))
    fac_h = int(math.ceil(img.getHeight() / targ_h))

    return max([fac_w, fac_h])


def main():
    """
    The main function that runs the collage creation process.

    Parameters:
    None

    Returns:
    None
    """

    init_img_filename = input("Enter the name of the initial image file: ")
    collage_img_filename = input("Enter the filename you will save the collage to: ")
    max_collage_w = int(input("Enter the maximum collage width: "))
    max_collage_h = int(input("Enter the maximum collage height: "))

    init_img = comp110_image.Picture(filename=init_img_filename)

    shrink_fac = get_shrink_factor(init_img, max_collage_w // 3, max_collage_h // 2)

    shrunk_img = shrink(init_img, shrink_fac)

    filter_pics = create_filtered_pics(shrunk_img)
    collage_canvas = assemble_collage(filter_pics)
    collage_canvas.show()
    collage_canvas.save(collage_img_filename)


if __name__ == "__main__":
    main()
