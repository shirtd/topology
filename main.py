from topology.complex.simplicial import *
from topology.complex.cellular import *

from topology.persistence.filtration import *
from topology.persistence.diagram import *

from topology.plot.util import plot_diagrams, plt, pqt, plot_complex


import pickle as pkl
import numpy as np
import time, os


plt.ion()
fig, ax = plt.subplots(1,2, sharex=True, sharey=True, figsize=(11,5))


if __name__ == '__main__':
    np.random.seed(0)
    # P = np.random.rand(100,3)
    t = np.linspace(0,1,10)
    xs, ys, zs = np.meshgrid(t, t, t)
    P = np.vstack((xs.flatten(), ys.flatten(), zs.flatten())).T
    P += (2*np.random.rand(*P.shape) - 1) * 5e-3

    bounds = np.array([[0, 1], [0, 1], [0, 1]])

    A = DelaunayComplex(P)
    # B = A.get_boundary()        # (1,2)
    B = A.get_boundary(bounds)  # (3,4)

    F = Filtration(A, 'alpha', False)
    # R = set()                   # (1) primal absolute ~ dual relative
    R = {F.index(s) for s in B} # (2,3,4) primal relative ~ intr dual relative

    HF = Diagram(A, F, R, verbose=True)

    V = VoronoiComplex(A)       # (1,3)
    C = {V.dual(s) for s in B}  # (1)
    # V = VoronoiComplex(A, B)    # (2,4)
    # C = V.get_boundary()        # (2)
    # C = V.get_boundary(bounds)  # (3)

    G = Filtration(V, 'alpha', True)
    S = {G.index(s) for s in C} # (1,2,3)
    # S = set()                   # (4)

    HG = Diagram(V, G, S, coh=True, verbose=True)

    plot_diagrams(ax[0], HF.diagram)
    plot_diagrams(ax[1], HG.diagram)
    plt.tight_layout()

    vfig = pqt.BackgroundPlotter()
    meshes, actors = plot_complex(vfig, A)
