from topology.complex.base import Complex
from topology.complex.cellular import DualComplex
from topology.complex.simplicial import SimplicialComplex
from topology.util import in_bounds, stuple, to_path
from topology.geometry import circumcenter, circumradius


import diode


class EmbeddedComplex(Complex):
    def __init__(self, P):
        self.P = P
    def get_boundary(self, bounds):
        out = {s for s in self(self.dim) if not self.in_bounds(s, bounds)}
        return {f for s in out for f in self.closure(s)}
    def in_bounds(self, s, bounds):
        pass

class DelaunayComplex(SimplicialComplex, EmbeddedComplex):
    def __init__(self, P):
        EmbeddedComplex.__init__(self, P)
        SimplicialComplex.__init__(self, P.shape[-1])
        for s,f in diode.fill_alpha_shapes(P, True):
            s = stuple(s)
            self.add_new(s, set(self.face_it(s)), alpha=f)
    def in_bounds(self, s, bounds):
        return in_bounds(circumcenter(self.P[s]), bounds)

class VoronoiComplex(DualComplex, EmbeddedComplex):
    def __init__(self, K, B=set()):
        P = circumcenter(K.P[K(K.dim)])
        EmbeddedComplex.__init__(self, P)
        DualComplex.__init__(self, K, B)
        self.nbrs = {i : set() for i,_ in enumerate(self(0))}
        for e in self(1):
            if len(e) == 2:
                self.nbrs[e[0]].add(e[1])
                self.nbrs[e[1]].add(e[0])
    def orient_face(self, s):
        return to_path({v for v in s}, self.nbrs)
    def in_bounds(self, s, bounds):
        return all(in_bounds(self.P[v], bounds) for v in s)
