"""
Draw a Penrose tiling using de Bruijn's pentagrid method.

Reference: "Algebraic theory of Penrose's non-periodic tilings
of the plane", N.G. de Bruijn.
"""
# Fifth roots of unity.
zeta = [(-1)**(.4*i) for i in range(5)]


def rhombus_at_intersection(gamma, r, s, kr, ks):
    """
    Find the rhombus corresponding to a pentagrid intersection point.

    Generates four complex numbers, giving the vertices of the rhombus
    corresponding in the pentagrid described by parameters gamma to the
    intersection of the two lines with equations:

       (z/zeta[r]).real + gamma[r] == kr

    and

       (z/zeta[s]).real + gamma[s] == ks

    The vertices traverse the perimeter of the rhombus in order (though that
    order may be either clockwise or counterclockwise).
    """
    z0 = 1j*(zeta[r]*(ks-gamma[s]) - zeta[s]*(kr-gamma[r])) / zeta[s-r].imag
    k = [0--((z0/t).real+p)//1 for t, p in zip(zeta, gamma)]
    for k[r], k[s] in [(kr, ks), (kr+1, ks), (kr+1, ks+1), (kr, ks+1)]:
        yield sum(x*t for t, x in zip(zeta, k))


def tiling(gamma, size):
    """
    Find all rhombuses corresponding to a limited set of intersections.
    """
    for r in range(5):
        for s in range(r+1, 5):
            for kr in range(-size, size+1):
                for ks in range(-size, size+1):
                    color = "cyan" if (r-s)**2%5==1 else "green"
                    yield rhombus_at_intersection(gamma, r, s, kr, ks), color


def to_canvas(vertices, scale, center):
    """
    Transform complex values to canvas points.

    Generates an interleaved list (x0, y0, x1, y1, ...), suitable
    for passing to Canvas.create_polygon.
    """
    for z in vertices:
        w = center + scale*z
        yield from (w.real, w.imag)


def main():
    from tkinter import Canvas, mainloop, Tk
    gamma, size = [0.3, 0.2, -0.1, -0.4, 0.0], 11
    width, height, scale, center = 800, 800, 20, 400+400j
    w = Canvas(Tk(), width=width, height=height)
    w.pack()
    for rhombus, color in tiling(gamma, size):
        coords = to_canvas(rhombus, scale, center)
        w.create_polygon(*coords, fill=color, outline="black")
    mainloop()


if __name__ == '__main__':
    main()
