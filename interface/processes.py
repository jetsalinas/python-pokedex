"""
Module containing utility functions for python-pokedex

:Author:    Daniel Montecastro
:Version:   20181204
"""

import pyglet as p


def bind(x, bounds, y=0):
    """
    Checks if a number is above or below a range and cycles it back into range

    Args:
        x(int): the number to be checked
        bounds(iterable): the upper and lower bounds
    Returns:
        int: the cycled number
    """
    if min == 0:
        y = 1
    if x > bounds[1]:
        return x - bounds[1] - y
    elif x < bounds[0]:
        return x + bounds[1] + y
    else:
        return x


def add0(x, limit=3):
    """
    Adds left-trailing 0's to a number

    Args:
        x(int): the number to be formatted
        limit(int): the maximum length of the string
    Returns:
        str: the formatted string
    """
    x = str(x)
    return ('0'*(limit-len(x)))+x


def vertex_create(stats, x, y, limit=255, size=100):
    """
    Makes a new hexagon based on pokemon stats

    Args:
        stats(list): The list of pokemon stats
        x(int): The x position of the lower-left part of the hexagon to be drawn
        y(int): The y position of the lower-left part of the hexagon to be drawn
        limit: The radius of the hexagon
        size: I don't fucking know what you mean by this daniel
    Returns:
        list: The list of vertices of the hexagon
    """
    dz = size/limit  # stat-to-size ratio
    dy = dz/2  # heights of sides
    dx = dy*(3**0.5)  # width of hexagon

    a1, a2 = x,                 y + stats[0] * dz  # HP   vertex
    b1, b2 = x + stats[1] * dx, y + stats[1] * dy  # Atk  vertex
    c1, c2 = x + stats[2] * dx, y - stats[2] * dy  # Def  verrtex
    d1, d2 = x,                 y - stats[3] * dz  # Spd  vertex
    e1, e2 = x - stats[4] * dx, y - stats[4] * dy  # SAtk vertex
    f1, f2 = x - stats[5] * dx, y + stats[5] * dy  # SDef vertex
    return [a1, a2, b1, b2, c1, c2, d1, d2, e1, e2, f1, f2]


def vertex_change(previous, current):
    """
    Updates the position of a list of vertices

    Args:
        previous(list): The current position of vertices to be updated
        current(list): The new position of vertices
    Returns:
        list: The updated list of vertices
    """
    for stat in range(len(previous)):
        if previous[stat] < current[stat]:
            previous[stat] += int(current[stat]/previous[stat])
        if previous[stat] > current[stat]:
            previous[stat] -= int(previous[stat]/current[stat])
    return [int(i) for i in previous]
