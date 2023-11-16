import math
import numpy as np
import pygame

class Color:
    WHITE = (255, 255, 255)
    LIGHTGREY = (130, 130, 130)
    GREY = (70, 70, 70)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    GREY2 = (50, 50, 50)
    PURPLE = (199, 21, 133)
    BROWN = (210, 105, 30)
    LIGHT_BLUE = (176, 196, 250)
    LIGHT_PURPLE = (102,102,255)


def dist_to_node(n1, n2):
    return dist(n1.get_coords(), n2.get_coords())


def dist_to_point(n, p):
    return dist(n.get_coords(), p)


def dist(p1, p2):
    x, y = p1[0], p1[1]
    xx, yy = p2[0], p2[1]
    return math.hypot(x - xx, y - yy)


def add_edge(n1, n2):
    n1.add_neighbour(n2)
    n2.add_neighbour(n1)


def remove_edge(n1, n2):
    del n1.adj[n2]
    del n1.edge[n2]
    del n2.adj[n1]
    del n2.edge[n1]


# the following functions two are taken from https://github.com/jlehett/Pytential-Fields
def drawArrow(surface, startCoord, endCoord, LINE_WIDTH=3):
    """
        Draw an arrow via pygame.
    """
    A = startCoord
    B = endCoord
    dir_ = (B[0] - A[0], B[1] - A[1])
    dir_mag = math.sqrt(dir_[0] ** 2 + dir_[1] ** 2)
    H = dir_mag / 4.0
    W = H * 2.0
    if dir_mag == 0:
        dir_mag = 0.00001
    dir_ = (dir_[0] / dir_mag, dir_[1] / dir_mag)

    q = (dir_[1], -dir_[0])

    C = (
        B[0] - (H * dir_[0]) + (W * q[0] / 2.0),
        B[1] - (H * dir_[1]) + (W * q[1] / 2.0)
    )

    D = (
        B[0] - (H * dir_[0]) - (W * q[0] / 2.0),
        B[1] - (H * dir_[1]) - (W * q[1] / 2.0)
    )

    pygame.draw.line(
        surface, Color.GREY, A, B, LINE_WIDTH
    )
    pygame.draw.line(
        surface, Color.GREY, B, C, LINE_WIDTH
    )
    pygame.draw.line(
        surface, Color.GREY, B, D, LINE_WIDTH
    )


@np.vectorize
def cvtRange(x, in_min, in_max, out_min, out_max):
    """
        Convert a value, x, from its old range of
        (in_min to in_max) to the new range of
        (out_min to out_max)
    """
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

