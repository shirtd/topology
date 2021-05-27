from topology.complex.base import ComplexElement, Complex
from topology.util import to_path, in_bounds, stuple
from topology.geometry import tet_circumcenter

import numpy as np

class Cell(ComplexElement):
    def __init__(self, vertices, dim, **data):
        ComplexElement.__init__(self, dim, **data)
        self.vertices = stuple(vertices)
    def __index__(self):
        return list(self.vertices)
    def key(self):
        return (self.dim, self.vertices)
    def __getitem__(self, i):
        return self.vertices[i]
    def __len__(self):
        return len(self.vertices)
    def __iter__(self):
        yield from self.vertices
    def __repr__(self):
        return '{%d; %s}' % (self.dim, ' '.join(map(str, self)))

class CellComplex(Complex):
    def __init__(self, dim):
        Complex.__init__(self, dim)
        self.__elements = {d : [] for d in range(dim+1)}
        self.__map, self.__faces, self.__cofaces = {}, {}, {}
    def add_new(self, c, dim, faces, **data):
        return self.add(Cell(c, dim, **data), faces)
    def add(self, cell, faces):
        k = hash(cell)
        if k in self:
            return cell
        self.__elements[cell.dim].append(cell)
        self.__map[k] = cell
        self.__faces[k] = set()
        self.__cofaces[k] = set()
        for f in faces:
            fk = hash(f)
            self.__faces[k].add(fk)
            self.__cofaces[fk].add(k)
        return cell
    def faces(self, c):
        return [self.__map[f] for f in self.__faces[hash(c)]]
    def cofaces(self, c):
        return [self.__map[f] for f in self.__cofaces[hash(c)]]
    def items(self):
        yield from self.__elements.items()
    def keys(self):
        yield from self.__elements.keys()
    def values(self):
        yield from self.__elements.values()
    def __getitem__(self, key):
        return self.__map[hash(key)]
    def __call__(self, dim):
        if dim in self.__elements:
            return self.__elements[dim]
        return set()
    def __iter__(self):
        yield from self.__map.values()
    def __contains__(self, key):
        return hash(key) in self.__map

class DualComplex(CellComplex):
    def __init__(self, K, B):
        CellComplex.__init__(self, K.dim)
        self.__dmap, self.__pmap = {}, {}
        self.__imap = {t : i for i,t in enumerate(K(K.dim))}
        for dim in reversed(range(self.dim+1)):
            for s in K(dim):
                if not s in B:
                    self.add_dual(K, s)
    def get_vertices(self, K, s):
        if s.dim < 3:
            return {v for f in K.cofaces(s) for v in self.get_vertices(K, f)}
        return {self.__imap[s]}
    def add_dual(self, K, s):
        dim = self.dim - s.dim
        vs = self.get_vertices(K, s)
        faces = [self.dual(f) for f in K.cofaces(s)]
        ds = self.add_new(vs, dim, faces, **s.data)
        self.__dmap[s], self.__pmap[ds] = ds, s
        return ds
    def dual(self, s):
        return self.__dmap[s]
    def primal(self, ds):
        return self.__pmap[ds]
