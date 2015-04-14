"""
Draw a Penrose tiling using de Bruijn's pentagrid method.

Reference: "Algebraic theory of Penrose's non-periodic tilings
of the plane", N.G. de Bruijn.
"""
# 5th roots of unity.
zs = [(-1)**(i/5) for i in range(0, 10, 2)]


def rhombus(ps, r, s, kr, ks):
    z = (zs[r]*(ks - ps[s]) - zs[s]*(kr - ps[r])) / (0.5*(zs[r-s] - zs[s-r]))
    k = [-((p + (z*zs[-i]).real)//-1) for i, p in enumerate(ps)]
    return [sum(x*zs[i] for i, x in enumerate(k))
            for k[r] in (kr, kr+1) for k[s] in (ks, ks+1)]


def rhombuses(params):
    return [rhombus(params, r, s, i, j)
            for r in range(5) for s in range(5) if r != s
            for i in range(-10, 10) for j in range(-10, 10)]


def main():
    from tkinter import Tk, Canvas, mainloop

    # de Bruijn parameters for the tiling; must sum to 0.0.
    params = [0.3, 0.2, -0.1, -0.4, 0.0]

    # Canvas parameters.
    width, height, scale = 800, 800, 40.0

    def transform_to_canvas(zs):
        zs = [0.5*width+0.5j*height + scale*zs[i] for i in [0, 1, 3, 2]]
        return [coord for z in zs for coord in [z.real, z.imag]]

    master = Tk()
    w = Canvas(master, width=width, height=height)
    w.pack()
    for r in rhombuses(params):
        w.create_polygon(*transform_to_canvas(r),
                         fill="white", outline="black")
    mainloop()


if __name__ == '__main__':
    main()
