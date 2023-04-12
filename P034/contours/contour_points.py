import numpy as np

from contours.fit_lines import fit_func_line, fit_func_square
from softest_exceptions.bad_shape_side import BadShapeSide


def mask_img_color(img, color):
    # 0 - left_blue, 1 - left_green, 2 - left_red, 3 - clear_all
    h, w, _ = img.shape

    for i in range(h):
        for j in range(w):
            if color == 0:
                img[i][j][1] = 0
                img[i][j][2] = 0
            elif color == 1:
                img[i][j][0] = 0
                img[i][j][2] = 0
            elif color == 2:
                img[i][j][0] = 0
                img[i][j][1] = 0
            elif color == 3:
                img[i][j][0] = 0
                img[i][j][1] = 0
                img[i][j][2] = 0
            else:
                print("bad color selected")
    return img


def get_corner_coordinates(hor, vert):
    y = (hor[0] * vert[1] + hor[1]) / (1 - hor[0] * vert[0])
    x = vert[0] * y + vert[1]
    return x, y


def fit_lines_at_corner(xdata, ydata):
    line_1 = fit_func_line(xdata[:20], ydata[:20])
    line_2 = fit_func_line(xdata[-20:], ydata[-20:])
    return line_1, line_2


def calculate_parabola(x, a, b, c):
    return a * x ** 2 + b * x + c


def calculate_parabola_factor(top_factor, bottom_factor, screen_line, max_screen_lines):
    return top_factor * ((max_screen_lines - screen_line) / max_screen_lines) + bottom_factor * (
            screen_line / max_screen_lines)


def get_screen_line_values(img, left_end, right_end, a, b, c, color):
    # 0 - blue, 1 - green, 2 - red
    screen_line_xs = []
    screen_line_ys = []
    screen_line_xy_values = []
    for x in range(left_end, right_end):
        y = round(calculate_parabola(x, a, b, c))
        screen_line_xs.append(x)
        screen_line_ys.append(y)
        screen_line_xy_values.append(img[y][x][color])
    return screen_line_xs, screen_line_ys, screen_line_xy_values


class ContourPoints:
    xdata = []
    ydata = []
    xdata_temp = []
    ydata_temp = []

    def __init__(self, img):
        self.right_screen_lines = None
        self.left_screen_lines = None
        self.max_screen_lines = None
        self.c_right = None
        self.b_right = None
        self.a_right = None
        self.c_left = None
        self.b_left = None
        self.a_left = None
        self.c_bottom = None
        self.b_bottom = None
        self.a_bottom = None
        self.c_top = None
        self.b_top = None
        self.a_top = None
        self.y_bottom_right = None
        self.x_bottom_right = None
        self.y_bottom_left = None
        self.x_bottom_left = None
        self.y_top_right = None
        self.x_top_right = None
        self.y_top_left = None
        self.x_top_left = None
        self.right_bottom = None
        self.right_top = None
        self.left_bottom = None
        self.left_top = None
        self.bottom_right = None
        self.bottom_left = None
        self.top_right = None
        self.top_left = None
        self.img = img
        self.xdata_top = []
        self.ydata_top = []
        self.xdata_bottom = []
        self.ydata_bottom = []
        self.xdata_left = []
        self.ydata_left = []
        self.xdata_right = []
        self.ydata_right = []

    @staticmethod
    def rotate_list(list_, n):
        return list_[n:] + list_[:n]

    @staticmethod
    def take_img_point_for_analyse(side, i, j, h, w):
        if side == "bottom":
            return j, i
        elif side == "top":
            return h - j - 1, w - i - 1
        elif side == "left":
            return i, j
        elif side == "right":
            return h - i - 1, w - j - 1
        else:
            raise BadShapeSide("bad side of shape")

    @classmethod
    def take_contour_points(cls, img, side):
        h, w, _ = img.shape
        cls.xdata = []
        cls.ydata = []

        for i in range(w if (side == "top" or side == "bottom") else h):
            for j in range(h if (side == "top" or side == "bottom") else w):
                k, l = ContourPoints.take_img_point_for_analyse(side, i, j, h, w)
                if img[k][l][2] > 127:
                    cls.xdata.append(l)
                    cls.ydata.append(k)
                    # img[k][l][2] = 255
                    break

    @classmethod
    def reverse_top_and_right_side_contour_points(cls, side):
        if side == "top" or side == "right":
            cls.xdata.reverse()
            cls.ydata.reverse()

    @classmethod
    def remove_discontinues(cls, side="top"):
        if side == "left" or side == "right":
            temp_data = cls.xdata
            cls.xdata = cls.ydata
            cls.ydata = temp_data
        ydata_roll = ContourPoints.rotate_list(cls.ydata, 1)
        cls.xdata_temp = []
        cls.ydata_temp = []
        for i in range(0, len(cls.ydata) - 1):
            if abs(ydata_roll[i] - cls.ydata[i]) < 3:
                cls.xdata_temp.append(cls.xdata[i])
                cls.ydata_temp.append(cls.ydata[i])
        if abs(cls.ydata[len(cls.ydata) - 1] - cls.ydata[len(cls.ydata) - 2]) < 3:
            cls.xdata_temp.append(cls.xdata[len(cls.ydata) - 1])
            cls.ydata_temp.append(cls.ydata[len(cls.ydata) - 1])
        if side == "left" or side == "right":
            cls.ydata = cls.xdata_temp
            cls.xdata = cls.ydata_temp
        else:
            cls.xdata = cls.xdata_temp
            cls.ydata = cls.ydata_temp

    @classmethod
    def perform_discontinuity_remove(cls, side):
        length_xdata = 0
        while length_xdata != len(cls.xdata):
            length_xdata = len(cls.xdata)
            ContourPoints.remove_discontinues(side)
        return cls.xdata, cls.ydata

    @staticmethod
    def take_roll_input_values_from(side):
        if side == "left":
            return -1, 1
        elif side == "right":
            return 1, 1
        elif side == "top":
            return -1, 0
        elif side == "bottom":
            return 1, 0
        else:
            raise BadShapeSide("bad side of shape")

    @classmethod
    def seek_edge(cls, img, side):
        variant, polarization = ContourPoints.take_roll_input_values_from(side)
        img_2 = np.roll(img, variant, polarization)
        img_diff = img_2 - img

        ContourPoints.take_contour_points(img_diff, side)
        ContourPoints.reverse_top_and_right_side_contour_points(side)
        ContourPoints.perform_discontinuity_remove(side)

        print(f"side {side} done")
        return cls.xdata, cls.ydata

    def seek_edges(self):
        self.xdata_top, self.ydata_top = ContourPoints.seek_edge(self.img, "top")
        self.xdata_bottom, self.ydata_bottom = ContourPoints.seek_edge(self.img, "bottom")
        self.xdata_left, self.ydata_left = ContourPoints.seek_edge(self.img, "left")
        self.xdata_right, self.ydata_right = ContourPoints.seek_edge(self.img, "right")

    def print_edges_coordinates(self, enable=False):
        if enable:
            print(len(self.xdata_top), self.xdata_top)
            print(len(self.ydata_top), self.ydata_top)
            print(len(self.xdata_bottom), self.xdata_bottom)
            print(len(self.ydata_bottom), self.ydata_bottom)
            print(len(self.xdata_left), self.xdata_left)
            print(len(self.ydata_left), self.ydata_left)
            print(len(self.xdata_right), self.xdata_right)
            print(len(self.ydata_right), self.ydata_right)

    def fit_lines_at_corners(self):
        self.top_left, self.top_right = fit_lines_at_corner(self.xdata_top, self.ydata_top)
        self.bottom_left, self.bottom_right = fit_lines_at_corner(self.xdata_bottom, self.ydata_bottom)
        self.left_top, self.left_bottom = fit_lines_at_corner(self.ydata_left, self.xdata_left)
        self.right_top, self.right_bottom = fit_lines_at_corner(self.ydata_right, self.xdata_right)

    def get_corners_coordinates(self):
        self.x_top_left, self.y_top_left = get_corner_coordinates(self.top_left, self.left_top)
        self.x_top_right, self.y_top_right = get_corner_coordinates(self.top_right, self.right_top)
        self.x_bottom_left, self.y_bottom_left = get_corner_coordinates(self.bottom_left, self.left_bottom)
        self.x_bottom_right, self.y_bottom_right = get_corner_coordinates(self.bottom_right, self.right_bottom)

    def print_corners_coordinates(self, enable=False):
        if enable:
            print(self.x_top_left, self.y_top_left)
            print(self.x_top_right, self.y_top_right)
            print(self.x_bottom_left, self.y_bottom_left)
            print(self.x_bottom_right, self.y_bottom_right)

    def fit_edges(self):
        self.a_top, self.b_top, self.c_top = fit_func_square(self.xdata_top, self.ydata_top)
        self.a_bottom, self.b_bottom, self.c_bottom = fit_func_square(self.xdata_bottom, self.ydata_bottom)
        self.a_left, self.b_left, self.c_left = fit_func_square(self.ydata_left, self.xdata_left)
        self.a_right, self.b_right, self.c_right = fit_func_square(self.ydata_right, self.xdata_right)

    def get_edges_length(self):
        self.max_screen_lines = max(self.y_bottom_left - self.y_top_left, self.y_bottom_right - self.y_top_right) + 1
        self.left_screen_lines = (self.y_bottom_left - self.y_top_left) / self.max_screen_lines
        self.right_screen_lines = (self.y_bottom_right - self.y_top_right) / self.max_screen_lines

    def get_screen_line_definition(self, screen_line):
        a = calculate_parabola_factor(self.a_top, self.a_bottom, screen_line, self.max_screen_lines)
        b = calculate_parabola_factor(self.b_top, self.b_bottom, screen_line, self.max_screen_lines)
        c = calculate_parabola_factor(self.c_top, self.c_bottom, screen_line, self.max_screen_lines)

        y_left = screen_line * self.left_screen_lines + self.y_top_left
        y_right = screen_line * self.right_screen_lines + self.y_top_right

        left_end = round(calculate_parabola(y_left, self.a_left, self.b_left, self.c_left))
        right_end = round(calculate_parabola(y_right, self.a_right, self.b_right, self.c_right))

        return left_end, right_end, a, b, c

    def obtain_contour_pixels(self, /, print_log=False):
        self.seek_edges()
        self.print_edges_coordinates(print_log)
        self.fit_lines_at_corners()
        self.get_corners_coordinates()
        self.print_corners_coordinates(print_log)
        self.fit_edges()
        self.get_edges_length()

    def get_screen_lines(self, img):
        screen_lines_xs = []
        screen_lines_ys = []
        screen_lines_xy_values = []
        for screen_line in range(0, round(self.max_screen_lines)):
            left_end, right_end, a, b, c = self.get_screen_line_definition(screen_line)
            screen_line_xs, screen_line_ys, screen_line_xy_values = get_screen_line_values(img, left_end, right_end, a,
                                                                                           b, c, color=2)
            screen_lines_xs.append(screen_line_xs)
            screen_lines_ys.append(screen_line_ys)
            screen_lines_xy_values.append(screen_line_xy_values)

        return screen_lines_xs, screen_lines_ys, screen_lines_xy_values

    @staticmethod
    def draw_curve_on_picture(img_src, img_curve):
        h, w, _ = img_src.shape
        for i in range(h):
            for j in range(w):
                for k in range(0, 3):
                    if img_curve[i][j][k] == 255:
                        img_src[i][j][k] = 255
        return img_src
