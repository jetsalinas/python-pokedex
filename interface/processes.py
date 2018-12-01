import pyglet as p

#cycles a number
def bind(x, bounds, y=0):
    if min == 0: y = 1
    if   x > bounds[1]: return x - bounds[1] - y
    elif x < bounds[0]: return x + bounds[1] + y
    else: return x


#return x as a string of length 'limit' (i.e. 1 -> 001)
def add0(x, limit=3):
    x = str(x)
    return ('0'*(limit-len(x)))+x


#creates an array of vertices for OpenGL drawing
def vertex_create(stats, x, y, limit=255, size=100):
    dz = size/limit     #stat-to-size ratio
    dy = dz/2           #heights of sides
    dx = dy*(3**0.5)    #width of hexagon

    a1, a2 = x,                 y + stats[0] * dz   #HP   vertex
    b1, b2 = x + stats[1] * dx, y + stats[1] * dy   #Atk  vertex
    c1, c2 = x + stats[2] * dx, y - stats[2] * dy   #Def  verrtex
    d1, d2 = x,                 y - stats[3] * dz   #Spd  vertex
    e1, e2 = x - stats[4] * dx, y - stats[4] * dy   #SAtk vertex
    f1, f2 = x - stats[5] * dx, y + stats[5] * dy   #SDef vertex
    return (a1, a2, b1, b2, c1, c2, d1, d2, e1, e2, f1, f2)


#allows for "transforming" of the polygon (instead of instantly changing shape)
def vertex_change(previous, current):
    previous = list(previous)
    for stat in range(len(previous)):
        if previous[stat] < current[stat]: previous[stat] += int(current[stat]/previous[stat])
        if previous[stat] > current[stat]: previous[stat] -= int(previous[stat]/current[stat])
    return tuple([int(i) for i in previous])
