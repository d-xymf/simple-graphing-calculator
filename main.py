from PIL import Image
import math

# the function that will be graphed
# avoid divisions by 0, return 'undef' instead
# example: f = lambda n : 1 / n if n != 0 else 'undef'
f = lambda n : n*n*n - 2*n

# zoom and pan
zoom = 0.1
offset = (0.5, 0.5)

image = Image.new('RGB', (600, 600), (255, 255, 255))

# colors of graph line and axes
line_color = (255, 0, 0)
axis_color = (150, 150, 150)

width, height = image.size

# draw axes
for x in range(width):
    image.putpixel((x, int(-offset[1] * height)), axis_color)
for y in range(height):
    image.putpixel((int(-offset[0] * width), y), axis_color)

# draw function graph by coloring all pixels the line of the graph runs through
for x in range(width):
    # pixel is not infinitely thin so treat it as a rectangular area with width of one pixel
    # spanning from (x_start, f(x_start)) to (x_end, f(x_end))
    #
    #                        (x_end, f(x_end))
    #                    __|_|__
    #                      |X|
    #                      |X|
    #                      |X|
    #                    __|X|__
    #                      | |
    #  (x_start, f(x_start))
    #
    # every pixel in this area will be colored

    x_start = (x / width - offset[0]) / zoom
    x_end = ((x+1) / width - offset[0]) / zoom

    y_start = f(x_start)
    y_end = f(x_end)

    # skip if start or end is undefined
    if y_start == 'undef' or y_end == 'undef':
        continue

    pixels_to_be_colored = []

    # splitting it into these two cases makes it easier to use the range() function
    if y_end > y_start:
        # standard case
        pixel_start = int((y_start * zoom + offset[1]) * height)
        pixel_end = int((y_end * zoom + offset[1]) * height) + 1
        pixels_to_be_colored = range(pixel_start, pixel_end)
    else:
        # flip y_end and y_start so pixel_end > pixel_start
        pixel_start = int((y_end * zoom + offset[1]) * height)
        pixel_end = int((y_start * zoom + offset[1]) * height) + 1
        pixels_to_be_colored = range(pixel_start, pixel_end)

    # color the pixels which the graph runs through
    for pixel in pixels_to_be_colored:

        # dont try to color the pixel if it is outside of the image
        if pixel > height-1 or pixel < 0:
            continue

        # height - 1 - pixel to flip the image vertically
        # this is needed because putpixel((0, 0), ...)
        # paints the top left pixel
        # however so far in the calculations we assumed that (0, 0)
        # is the bottom left pixel
        image.putpixel((x, height - 1 - pixel), line_color)

image.save('graph.png')

