from topology.complex.base import ComplexElement, Complex
from topology.geometry import tet_circumcenter
from topology.util import to_path, in_bounds

import numpy as np


class Cell(ComplexElement):
    def __init__(self, vertices, dim, **data):
        ComplexElement.__init__(self, dim, **data)
        self.vertices = tuple(sorted(vertices))
    def astuple(self):
        return (self.dim, self.vertices)
    def __eq__(self, other):
        if not isinstance(other, tuple):
            other = other.astuple()
        return self.astuple() == other
    def __hash__(self):
        return hash(self.astuple())
    def __getitem__(self, i):
        return self.vertices[i]
    def __len__(self):
        return len(self.vertices)
    def __lt__(self, other):
        if not isinstance(other, tuple):
            other = other.astuple()
        return self.astuple() < other
    def __iter__(self):
        yield from self.vertices
    def __repr__(self):
        return '{%d; %s}' % (self.dim, ' '.join(map(str, self)))

class CellComplex(Complex):
    def __init__(self, dim):
        Complex.__init__(self, dim)
        self.elements = {d : [] for d in range(dim+1)}
        self.map, self.faces, self.cofaces = {}, {}, {}
    def add_new(self, c, dim, faces, **data):
        return self.add(Cell(c, dim, **data), faces)
    def add(self, cell, faces):
        c = cell.astuple()
        if c in self:
            return cell
        self.map[c] = cell
        self.elements[cell.dim].append(cell)
        self.faces[c] = faces
        self.cofaces[c] = set()
        for f in faces:
            self.cofaces[f].add(c)
        return cell
    def get_faces(self, c):
        return [self[f] for f in self.faces[c]]
    def get_cofaces(self, c):
        return [self[f] for f in self.cofaces[c]]
    def items(self):
        yield from self.elements.items()
    def keys(self):
        yield from self.elements.keys()
    def values(self):
        yield from self.elements.values()
    def __getitem__(self, key):
        return self.map[key]
    def __call__(self, dim):
        if dim in self.elements:
            return self.elements[dim]
        return set()
    def __iter__(self):
        yield from self.map.values()
    def __contains__(self, key):
        return key in self.map
    def closure(self, s):
        return {s}.union({f for t in self.get_faces(s) for f in self.closure(t)})
    # def get_boundary(self):
    #     outfaces = {s for s in self(2) if len(self.get_cofaces(s)) < 2}
    #     return {f for s in outfaces for f in self.closure(s)}
    def get_boundary(self, bounds=None):
        if bounds is None:
            out = {s for s in self(2) if len(self.get_cofaces(s)) < 2}
        else:
            out = {s for s in self(3) if not self.in_bounds(s, bounds)}
        return {f for s in out for f in self.closure(s)}
    def in_bounds(self, s, bounds):
        pass

class DualComplex(CellComplex):
    def __init__(self, K, B):
        CellComplex.__init__(self, K.dim)
        self.dmap, self.pmap = {}, {}
        self.imap = {t : i for i,t in enumerate(K(K.dim))}
        for dim in reversed(range(self.dim+1)):
            for s in K(dim):
                if not s in B:
                    self.add_dual(K, s)
    def get_vertices(self, K, s):
        if s.dim < 3:
            return {v for f in K.get_cofaces(s) for v in self.get_vertices(K, f)}
        return {self.imap[s]}
    def add_dual(self, K, s):
        dim = self.dim - s.dim
        vs = self.get_vertices(K, s)
        faces = [self.dual(f) for f in K.get_cofaces(s)]
        ds = self.add_new(vs, dim, faces, **s.data)
        self.dmap[s], self.pmap[ds] = ds, s
        return ds
    def dual(self, s):
        return self.dmap[s]
    def primal(self, ds):
        return self.pmap[ds]

class VoronoiComplex(DualComplex):
    def __init__(self, K, B=set()):
        DualComplex.__init__(self, K, B)
        self.P = np.vstack([tet_circumcenter(K.P[list(t)]) for t in K(K.dim)])
        self.nbrs = {i : set() for i,_ in enumerate(self(0))}
        for e in self(1):
            if len(e) == 2:
                self.nbrs[e[0]].add(e[1])
                self.nbrs[e[1]].add(e[0])
    def in_bounds(self, s, bounds):
        return all(in_bounds(self.P[v], bounds) for v in s)
    def orient_face(self, s):
        return to_path({v for v in s}, self.nbrs)
