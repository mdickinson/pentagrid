"""
Draw a Penrose tiling using de Bruijn's pentagrid method.

Reference: "Algebraic theory of Penrose's non-periodic tilings
of the plane", N.G. de Bruijn.
"""
zs = [(-1)**(2*i/5) for i in range(5)]


def rhombus(ps, r, s, kr, ks):
    z = 2*(zs[r]*(ks - ps[s]) - zs[s]*(kr - ps[r])) / (zs[r-s] - zs[s-r])
    k = [-((p + (z*zs[-i]).real)//-1) for i, p in enumerate(ps)]
    return [sum(x*zs[i] for i, x in enumerate(k))
            for k[r] in (kr, kr+1) for k[s] in (ks, ks+1)]


def tiling(params, size):
    return (rhombus(params, r, s, i, j)
            for r in range(5) for s in range(5) if r != s
            for i in range(-size, size+1) for j in range(-size, size+1))


def main():
    from tkinter import Tk, Canvas, mainloop

    params = [0.3, 0.2, -0.1, -0.4, 0.0]
    size = 10
    width, height, scale = 800, 800, 40.0
    center = 0.5*width+0.5j*height

    def to_canvas(zs):
        return [coord for z in [center + scale*zs[i^i>>1] for i in range(4)]
                for coord in (z.real, z.imag)]

    w = Canvas(Tk(), width=width, height=height)
    w.pack()
    for r in tiling(params, size):
        w.create_polygon(*to_canvas(r), fill="white", outline="black")

    mainloop()


if __name__ == '__main__':
    main()
