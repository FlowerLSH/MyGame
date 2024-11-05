import math
import pygame

def get_rect_vertices(rect, angle):
    cx, cy = rect.center
    corners = [
        (-rect.width / 2, -rect.height / 2),
        (rect.width / 2, -rect.height / 2),
        (rect.width / 2, rect.height / 2),
        (-rect.width / 2, rect.height / 2)
    ]
    vertices = []
    for x, y in corners:
        rotated_x = x * math.cos(angle) - y * math.sin(angle)
        rotated_y = x * math.sin(angle) + y * math.cos(angle)
        vertices.append((cx + rotated_x, cy + rotated_y))
    return vertices

def get_axes(vertices):
    axes = []
    for i in range(2):
        p1 = vertices[i]
        p2 = vertices[(i + 1) % len(vertices)]
        edge = (p2[0] - p1[0], p2[1] - p1[1])
        axis = (-edge[1], edge[0])
        length = math.sqrt(axis[0] ** 2 + axis[1] ** 2)
        axes.append((axis[0] / length, axis[1] / length))
    return axes

def dot(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1]

def aabb(rect1, rect2):
    if rect1.right < rect2.left or rect2.right < rect1.left:
        return False
    if rect1.top > rect2.bottom or rect2.top > rect1.bottom:
        return False
    return True

def obb(rect1, rect2, angle1, angle2):
    vertices1 = get_rect_vertices(rect1, angle1)
    vertices2 = get_rect_vertices(rect2, angle2)
    axes1 = get_axes(vertices1)
    axes2 = get_axes(vertices2)
    T = (rect2.centerx - rect1.centerx, rect2.centery - rect1.centery)

    for axis in axes1 + axes2:
        t_proj = abs(dot(T, axis))
        proj1 = sum(abs(dot(vertex, axis)) for vertex in vertices1) / 4
        proj2 = sum(abs(dot(vertex, axis)) for vertex in vertices2) / 4
        if t_proj > proj1 + proj2:
            return False

    return True

def get_intersection_point(u1, u2, v1, v2):
    r1 = (u2[0] - u1[0], u2[1] - u1[1])
    r2 = (v2[0] - v1[0], v2[1] - v1[1])

    det = r1[0] * r2[1] - r1[1] * r[0]
    if det == 0:
        return None
    
    t = ((v1[0] - u1[0]) * r2[1] - (v1[1] - u1[1]) * r2[0]) / det
    intersection = (u1[0] + t * r1[0], u1[1] + t * r1[1])
    return intersection

def distance(u1, u2):
    return math.sqrt((u2[0] - u1[0]) ** 2 + (u2[1] - u1[1]) ** 2)

def segments_intersect(s1, s2):
    u1, u2 = s1
    v1, v2 = s2
    intersection = get_intersection_point(u1, u2, v1, v2)
    if intersection is None:
        return False
    
    else:
        x, y = intersection
        d1, d2 = distance(u1, u2), distance(v1, v2)
        return (distance(u1, (x, y)) <= d1 and
                distance(u2, (x, y)) <= d1 and
                distance(v1, (x, y)) <= d2 and
                distance(v2, (x, y)) <= d2)