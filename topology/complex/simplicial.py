from topology.complex.cellular import Cell, CellComplex
from topology.util import stuple, diff, in_bounds
from topology.geometry import *

from scipy.spatial import Delaunay
import numpy.linalg as la
import numpy as np
import diode


class Simplex(Cell):
    def __init__(self, vertices, **data):
        Cell.__init__(self, vertices, len(vertices)-1, **data)
    def astuple(self):
        return self.vertices
    def __lt__(self, other):
        if not isinstance(other, tuple):
            other = (other.dim, other.astuple())
        else:
            other = (len(other)-1, other)
        return (self.dim, self.astuple()) < other
    def __repr__(self):
        return '[%s]' % ' '.join(map(str, self))

class SimplicialComplex(CellComplex):
    def __init__(self, dim):
        CellComplex.__init__(self, dim)
    def face_it(cls, s):
        dim = len(s)-1
        if dim:
            for i in range(dim+1):
                yield s[:i]+s[i+1:]
    def add_new(self, s, faces, **data):
        return self.add(Simplex(s, **data), faces)

class DelaunayComplex(SimplicialComplex):
    def __init__(self, P):
        SimplicialComplex.__init__(self, P.shape[-1])
        self.P = P
        for s,f in diode.fill_alpha_shapes(P, True):
            s = stuple(s)
            self.add_new(s, set(self.face_it(s)), alpha=f)
    def in_bounds(self, s, bounds):
        return in_bounds(tet_circumcenter(self.P[list(s)]), bounds)
    # def get_alpha(self, s):
    #     dim, p = len(s)-1, self.P[list(s)]
    #     return (tet_circumradius(p) if dim == 3
    #         else tri_circumradius(p) if dim == 2
    #         else la.norm(diff(p))if dim == 1
    #         else 0) / 4

# class DelaunayComplex(SimplicialComplex):
#     def __init__(self, P):
#         SimplicialComplex.__init__(self, P.shape[-1])
#         self.P = P
#         self.circumcenters = {}
#         delaunay = Delaunay(P)
#         for s in delaunay.simplices:
#             self.add_closure(stuple(s))
#     def add_closure(self, s):
#         if len(s) == 1:
#             return self.add_new(s, [], alpha=0)
#         c = self.get_circumcenter(s)
#         self.circumcenters[s] = c
#         alpha = la.norm(self.P[s[0]] - c) ** 2
#         faces = list(self.face_it(s))
#         for i,f in enumerate(faces):
#             if not f in self:
#                 self.add_closure(f)
#             if len(f) > 1:
#                 fc = self.circumcenters[f]
#                 if (la.norm(self.P[i] - fc) ** 2 < self[f]('alpha')
#                         and alpha < self[f]('alpha')):
#                     self[f].data['alpha'] = alpha
#         return self.add_new(s, faces, alpha=alpha)
#     def get_circumcenter(self, s):
#         dim, p = len(s)-1, self.P[list(s)]
#         return (tet_circumcenter(p) if dim == 3
#             else tri_circumcenter(p) if dim == 2
#             else p.sum(0) / 2 if dim == 1 else None)
#     # def get_alpha(self, s):
#     #     dim, p = len(s)-1, self.P[list(s)]
#     #     return (tet_circumradius(p) if dim == 3
#     #         else tri_circumradius(p) if dim == 2
#     #         else la.norm(diff(p)) if dim == 1
#     #         else 0) ** 2 / 4
