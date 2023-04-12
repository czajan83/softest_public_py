from math import floor, ceil

import cv2
from matplotlib import pyplot as plt

from contours.contour_points import ContourPoints, calculate_parabola, mask_img_color
from contours.fit_lines import fit_func_square


def wait_for_cv2_windows():
    k = cv2.waitKey(0)
    if k == 27 or k == ord("q"):
        cv2.destroyAllWindows()


def save_images_for_development():
    img_single_color = cv2.imread(f"imgs\\masked_lowsize_2.jpg")

    for i in range(0, 255):
        if i % 5 == 0:
            j = 255 - i
            ret, img_bin_color = cv2.threshold(img_single_color, j, 255, cv2.THRESH_BINARY)
            cv2.imwrite(f"imgs\\binary_threshold_{j}.bmp", img_bin_color)
            print(j)


def save_image_with_screen_line(img_name, img, screen_line, x_coords, y_coords):
    img_screen_line = img.copy()
    mask_img_color(img_screen_line, 3)
    for test_x in range(0, len(x_coords[screen_line]) - 1):
        img_screen_line[y_coords[screen_line][test_x]][x_coords[screen_line][test_x]][0] = 255
        img_screen_line[y_coords[screen_line][test_x]][x_coords[screen_line][test_x]][1] = 255

    cv2.imwrite(f"contours\\{img_name}.jpg", ContourPoints.draw_curve_on_picture(img, img_screen_line))


def plot_screen_line_values_with_parabola_fit(screen_line, x_coords, xy_values):
    a, b, c = fit_func_square(x_coords[screen_line], xy_values[screen_line])
    ydata = []
    for xdata in x_coords[screen_line]:
        ydata.append(calculate_parabola(xdata, a, b, c))
    plt.plot(x_coords[screen_line], xy_values[screen_line])
    plt.plot(x_coords[screen_line], ydata, 'b-', label='data')
    plt.show()


def plot_single_line_with_parabola_fit(x_coords, xy_values):
    a, b, c = fit_func_square(x_coords, xy_values)
    ydata = []
    validation_data = []
    for xdata in x_coords:
        ydata.append(calculate_parabola(xdata, a, b, c))
        validation_data.append(calculate_parabola(xdata, a, b, c - 30))
    plt.plot(x_coords, xy_values)
    plt.plot(x_coords, ydata, 'b-', label='data')
    plt.plot(x_coords, validation_data, 'g-', label='validation_data')
    plt.show()


def print_request_1(test_xs):
    return input(f"Please provide the line to analyze (between 0 and {len(test_xs) - 1}) or press X to terminate\n")


def manual_analysis(img, test_xs, test_ys, test_xy_values, type="img"):
    screen_line_input = print_request_1(test_xs)
    while screen_line_input != f"X":
        if not screen_line_input.isnumeric():
            print(f"Numeric value not recognized, please try again")
        else:
            screen_line = int(screen_line_input)
            if screen_line < 0 or screen_line > len(test_xs) - 1:
                print(f"Value out of range detected, please try again")
            else:
                if type == "img":
                    img_masked = cv2.imread(img)
                    save_image_with_screen_line(f"screen_line_{screen_line}", img_masked, screen_line, test_xs, test_ys)
                    plot_screen_line_values_with_parabola_fit(screen_line, test_xs, test_xy_values)
                else:
                    plot_single_line_with_parabola_fit(test_xs[screen_line], test_xy_values[screen_line])
        screen_line_input = print_request_1(test_xs)


def retrieve_single_pixel(step, pixel_no, img_pixel_values):
    screen_x = 0
    for j in range(ceil(step * pixel_no), floor(step * (pixel_no + 1))):
        screen_x += img_pixel_values[j]
    if ceil(step * pixel_no) - step * pixel_no > 0.0:
        screen_x += img_pixel_values[ceil(step * pixel_no) - 1] * (ceil(step * pixel_no) - step * pixel_no)
    if step * (pixel_no + 1) - floor(step * (pixel_no + 1)) > 0.0:
        screen_x += img_pixel_values[ceil(step * pixel_no) + 1] * \
                    (step * (pixel_no + 1) - floor(step * (pixel_no + 1)))
    return screen_x / step


def retrieve_pixel_values_horizontally(test_xs, test_xy_values):
    screen_lines_nos = []
    screen_lines_values = []
    for line in range(0, len(test_xs)):
        bad_pixel_coords = []
        del test_xs[line][0]
        del test_xy_values[line][0]
        step = len(test_xs[line]) / 320
        screen_line_no = []
        screen_line_values = []
        for i in range(0, 320):
            screen_pixel_in_line = retrieve_single_pixel(step, i, test_xy_values[line])
            screen_line_no.append(i)
            screen_line_values.append(screen_pixel_in_line)
        # a, b, c = fit_func_square(screen_line_no, screen_line_values)
        # for pixel_no in screen_line_no:
        #     if screen_line_values[pixel_no] < calculate_parabola(pixel_no, a, b, c - 30):
        #         bad_pixel_coords.append(pixel_no)
        # print(line, bad_pixel_coords)
        screen_lines_nos.append(screen_line_no)
        screen_lines_values.append(screen_line_values)
    return screen_lines_nos, screen_lines_values


def retrieve_pixel_values_vertically(test_xy_values):
    screen_lines_values_transp = []
    test_xy_values_transp = [[test_xy_values[j][i] for j in range(len(test_xy_values))] for i in
                             range(len(test_xy_values[0]))]
    for line in range(0, len(test_xy_values_transp)):
        step = len(test_xy_values_transp[line]) / 240
        screen_line_values = []
        for i in range(0, 240):
            screen_pixel_in_line = retrieve_single_pixel(step, i, test_xy_values_transp[line])
            screen_line_values.append(screen_pixel_in_line)
        screen_lines_values_transp.append(screen_line_values)
    screen_lines_values = [[screen_lines_values_transp[j][i] for j in range(len(screen_lines_values_transp))] for i in
                           range(len(screen_lines_values_transp[0]))]
    return screen_lines_values


def retrieve_bad_pixels(pixel_lines):
    x_points = range(0, 320)
    i = 1
    for pixel_line in pixel_lines:
        bad_pixel_coords = []
        a, b, c = fit_func_square(x_points, pixel_line)
        for x_point in x_points:
            if pixel_line[x_point] < calculate_parabola(x_point, a, b, c - 30):
                bad_pixel_coords.append(x_point)
        print(i, bad_pixel_coords)
        i = i + 1


def test_bad_pixels():
    masked_image_filename = f"imgs\\masked_lowsize_2.jpg"
    img = cv2.imread(f"imgs\\binary_threshold_125.bmp")
    img_masked = cv2.imread(masked_image_filename)

    test = ContourPoints(img)
    test.obtain_contour_pixels(print_log=False)
    test_xs, test_ys, test_xy_values = test.get_screen_lines(img_masked)

    # manual_analysis(masked_image_filename, test_xs, test_ys, test_xy_values, type="img")
    screen_lines_nos, screen_lines_values = retrieve_pixel_values_horizontally(test_xs, test_xy_values)

    screen_lines_values_2 = screen_lines_values[3:-1]
    pure_screen_lines_values = retrieve_pixel_values_vertically(screen_lines_values_2)
    print(len(pure_screen_lines_values))
    print(len(pure_screen_lines_values[0]))
    retrieve_bad_pixels(pure_screen_lines_values)

    # manual_analysis(masked_image_filename, screen_lines_nos, test_ys, screen_lines_values, type="screen")
