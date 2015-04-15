"""
Draw a Penrose tiling using de Bruijn's pentagrid method.

Reference: "Algebraic theory of Penrose's non-periodic tilings
of the plane", N.G. de Bruijn.
"""
# Fifth roots of unity.
zs = [(-1)**(.4*i) for i in range(5)]


def rhombus_at_intersection(gamma, r, s, kr, ks):
    """
    Return the rhombus corresponding to a pentagrid intersection point.

    Returns a list of four complex numbers, giving the vertices of the rhombus
    corresponding in the pentagrid described by parameters gamma to the
    intersection of the two lines with equations:

       (z/zs[r]).real + gamma[r] == kr

    and

       (z/zs[s]).real + gamma[s] == ks

    The vertices traverse the perimeter of the rhombus in order (though that
    order may be either clockwise or counterclockwise).
    """
    z0 = 1j * (zs[r]*(ks - gamma[s]) - zs[s]*(kr - gamma[r])) / zs[s-r].imag
    k = [0--((z0/t).real+p)//1 for t, p in zip(zs, gamma)]
    return (sum(x*t for t, x in zip(zs, k)) for k[r] in (kr, kr+1)
            for k[s] in (ks+k[r]%2, ks+~k[r]%2))


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


def to_canvas(zs, scale, center):
    """
    Transform complex values to canvas points.

    Generates an interleaved list (x0, y0, x1, y1, ...), suitable
    for passing to Canvas.create_polygon.
    """
    for z in zs:
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
