from tkinter import *

"""
Let zeta be exp(2*i*pi/5).

For integers i and k with 0 <= i < 5, let L(i, k) be the line in the complex
plane defined by equation

   Re(z / zeta^i) = k

So L(0, k) is the vertical line that passes through the real axis at position
k, L(1, k) is obtained by rotating L(0, k) by 2*pi/5 around the origin, and so
on.

Finding the intersection between L(i, k) and L(j, l) (i != j):

Wlog, i = 0 (rotate).  So we want:

   Re(z) = k
   Re(z / zeta^j) = l

So z = k + iy, and

   k * (zeta^-j + zeta^j) + iy * (zeta^-j - zeta^j) = 2*l

from which we get:

   iy = (2l - k*(zeta^-j + zeta^j)) / (zeta^-j - zeta^j)

Substiting back into the expression for z, and simplifying, gives:

   z = 2l / (zeta^-j - zeta^j) - 2*k*zeta^j / (zeta^-j - zeta^j)

In the general case, (i not necessarily equal to 0), the intersection is:

   z = (zeta^i l - zeta^j k) * 2 / (zeta**(i-j) - zeta**(j-i))

"""
import cmath
import math
import unittest

# A primitive 5th root of unity.
zeta = cmath.exp(2j*cmath.pi/5)


def vec_to_z(vec):
    return sum(x*zeta**i for i, x in enumerate(vec))


class Line(object):
    """
    The line in the complex plane given by equation

        Re(z / zeta^i) == k.

    """
    def __init__(self, i, k):
        self.i = i % 5
        self.k = k

    def contains(self, z, eps=1e-7):
        i, k = self.i, self.k
        return abs((z / zeta**i).real - k) < eps


def intersection(line1, line2):
    i, k = line1.i, line1.k
    j, l = line2.i, line2.k
    return (zeta**i*l - zeta**j*k) * 2 / (zeta**(i-j) - zeta**(j-i))


class Pentagrid(object):
    def __init__(self, params):
        self.params = params

    def k_coords(self, z):
        # K_0(z), K_1(z), ..., K_4(z), as in (4.3) of de Bruijn's paper.
        return [math.ceil((z * zeta**-j).real + param)
                for j, param in enumerate(self.params)]

    def intersection(self, r, s, kr, ks):
        if not (0 <= r < 5) and (0 <= s < 5) and (r != s):
            raise ValueError("Bad r and s: {}, {}".format(r, s))
        line1 = Line(r, kr - self.params[r])
        line2 = Line(s, ks - self.params[s])
        z0 = intersection(line1, line2)

        k_values = self.k_coords(z0)

        # Now k_values[r] should be kr, and k_values[s] should be ks,
        # but values may be kr+1, ks+1.
        assert k_values[r] in (kr, kr+1)
        assert k_values[s] in (ks, ks+1)

        corners = []
        for k_values[r] in (kr, kr+1):
            for k_values[s] in (ks, ks+1):
                corner = k_values.copy()
                corners.append(corner)
        # order 0 -> 1 -> 3 -> 2, so reverse the last two.
        corners[2], corners[3] = corners[3], corners[2]
        z_corners = list(map(vec_to_z, corners))
        # Coords for the rhombus.
        return [
            coord
            for z in map(vec_to_z, corners)
            for coord in [z.real, z.imag]
        ]


class TestIntersection(unittest.TestCase):
    def test_an_intersection(self):
        line1 = Line(0, 5)
        line2 = Line(1, 13)
        z = intersection(line1, line2)
        self.assertTrue(line1.contains(z))
        self.assertTrue(line2.contains(z))

    def test_another_intersection(self):
        line1 = Line(0, 5)
        line2 = Line(2, -3)
        z = intersection(line1, line2)
        self.assertTrue(line1.contains(z))
        self.assertTrue(line2.contains(z))

    def test_another_intersection_backwards(self):
        line1 = Line(2, -3)
        line2 = Line(0, 5)
        z = intersection(line1, line2)
        self.assertTrue(line1.contains(z))
        self.assertTrue(line2.contains(z))

    def test_yet_another_intersection(self):
        line1 = Line(1, 5)
        line2 = Line(3, -3)
        z = intersection(line1, line2)
        self.assertTrue(line1.contains(z))
        self.assertTrue(line2.contains(z))




def main():
    master = Tk()

    width = height = 800
    scale = 40.0

    w = Canvas(master, width=width, height=height)
    w.pack()

    def transform_to_canvas(args):
        xs = args[::2]
        ys = args[1::2]
        new_xs = [0.5*width + scale*x for x in xs]
        new_ys = [0.5*height + scale*y for y in ys]
        return [
            coord
            for pt in zip(new_xs, new_ys)
            for coord in pt
        ]

    params = [0.3, 0.2, -0.1, -0.4, 0.0]
    grid = Pentagrid(params)

    for r in range(5):
        for s in range(5):
            if r == s:
                continue
            for i in range(-10, 10):
                for j in range(-10, 10):
                    rhombus = grid.intersection(r, s, i, j)
                    rhombus = transform_to_canvas(rhombus)
                    w.create_polygon(*rhombus, fill="white", outline="black")

    mainloop()


if __name__ == '__main__':
    main()
