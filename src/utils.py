#
# Created by MC着火的冰块(zhdbk3) on 2025/2/3
#

from manim import *
import numpy as np
from numpy import sin, cos


# 以下两个函数来自
# https://github.com/BengbuGuards/StarLocator/blob/main/prototype/core/positioning/top_point/utils/plane.py
def two_line_intersection_point(l1, l2):
    p1 = np.array(l1[0])
    p2 = np.array(l1[1])
    p3 = np.array(l2[0])
    p4 = np.array(l2[1])

    v1 = p2 - p1
    v2 = p4 - p3
    v3 = p3 - p1

    det = v1[0] * v2[1] - v1[1] * v2[0]
    if det == 0:
        return False, np.array([0, 0])

    t = (v3[0] * v2[1] - v3[1] * v2[0]) / det
    res = p1 + t * v1
    return True, res


def all_points_of_lines_intersection(lines):
    points = []
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            has_intersection, intersection_point = two_line_intersection_point(
                lines[i], lines[j]
            )
            if has_intersection:
                points.append(intersection_point)

    return points


def get_circle(lat: float, lon: float, zenith_angle: float, color: ParsableManimColor) -> Circle:
    """
    根据 GP 和天顶角给出它的圆
    :param lat: GP 纬度，即 phi
    :param lon: GP 经度，即 lambda
    :param zenith_angle: 天顶角，即 theta
    :param color: 圆的颜色
    :return: 一个 Circle 对象
    """
    R = 2
    r = R * np.sin(zenith_angle)
    circle = Circle(r, color=color)
    # rotate 遵循右手螺旋定则
    # 先转到 (0°, 0°) 的位置
    circle.shift(OUT * R * np.cos(zenith_angle)).rotate(PI / 2, UP, ORIGIN)
    # 旋转纬度
    circle.rotate(lat, DOWN, ORIGIN)
    # 旋转经度
    circle.rotate(lon, OUT, ORIGIN)
    # 我要精神分裂了，为什么 MC 的坐标系和通常的不一样啊
    return circle


def get_gp_dot(lat: float, lon: float, color: ParsableManimColor) -> Dot:
    """
    根据 GP 经纬度给出它在三维空间中的 Dot 对象
    :param lat: GP 纬度，即 phi
    :param lon: GP 经度，即 lambda
    :param color: 圆的颜色
    :return: 一个 Dot 对象
    """
    R = 2
    return Dot(R * np.array((
        cos(lat) * cos(lon), cos(lat) * sin(lon), sin(lat)
    )), color=color)
