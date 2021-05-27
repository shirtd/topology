from topology.complex.simplicial import *
from topology.complex.cellular import *
from topology.complex.geometric import *

from topology.persistence.filtration import *
from topology.persistence.diagram import *

from topology.plot.util import plot_diagrams, plt, pqt, plot_complex

import dionysus as dio
import diode

import pickle as pkl
import numpy as np
import time, os


if __name__ == '__main__':
    np.random.seed(0)
    BOUNDS = np.array([[0, 1], [0, 1], [0, 1]])
    N = (20, 20, 20)
    NOISE = 5e-1


    xs, ys, zs = np.meshgrid(*(np.linspace(a,b,n) for (a,b),n in zip(BOUNDS, N)))
    grid_points = np.vstack((xs.flatten(), ys.flatten(), zs.flatten())).T
    random_noise = diff(BOUNDS.T) * (2*np.random.rand(*grid_points.shape) - 1) * NOISE
    P = grid_points + random_noise


    A = DelaunayComplex(P, verbose=True)
    # B = A.get_boundary()                # (1,2)
    B = A.get_boundary(BOUNDS)          # (3,4)

    F = Filtration(A, 'alpha', False)
    # R = set()                           # (1) primal absolute ~ dual relative
    R = {F.index(s) for s in B}         # (2,3,4) primal relative ~ intr dual relative

    HF = Diagram(A, F, R, verbose=True)


    V = VoronoiComplex(A, verbose=True) # (1,3)
    C = {V.dual(s) for s in B}          # (1)
    # V = VoronoiComplex(A, B, True)      # (2,4)
    # C = V.get_boundary()                # (2)
    # C = V.get_boundary(BOUNDS)          # (3)

    G = Filtration(V, 'alpha', True)
    S = {G.index(s) for s in C}         # (1,2,3)
    # S = set()                           # (4)

    HG = Diagram(V, G, S, coh=True, verbose=True)


    plt.ion()
    fig, ax = plt.subplots(1,2, sharex=True, sharey=True, figsize=(11,5))
    plot_diagrams(ax[0], HF.diagram)
    plot_diagrams(ax[1], HG.diagram)
    plt.tight_layout()

    vfig = pqt.BackgroundPlotter()
    meshes, actors = plot_complex(vfig, A)


    # t0 = time.time()
    # A = DelaunayComplex(P)
    # F = Filtration(A, 'alpha')
    # HF = Diagram(A, F)
    # print('me\t', time.time() - t0)
    #
    #
    # t0 = time.time()
    # dA = diode.fill_alpha_shapes(P, True)
    # dF = dio.Filtration(dA)
    # dHF = dio.homology_persistence(dF)
    # dD = dio.init_diagrams(dHF, dF)
    # print('dio\t', time.time() - t0)
