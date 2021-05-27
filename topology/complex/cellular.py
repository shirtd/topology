from topology.complex.base import Element, Complex

from tqdm import tqdm


class Cell(Element):
    def __repr__(self):
        return '{%d; %s}' % (self.dim, ' '.join(map(str, self)))

class CellComplex(Complex):
    def add_new(self, c, dim, faces, **data):
        return self.add(Cell(c, dim, **data), faces)

class DualComplex(CellComplex):
    def __init__(self, K, B):
        CellComplex.__init__(self, K.dim)
        self.__dmap, self.__pmap = {}, {}
        self.__imap = {t : i for i,t in enumerate(K(K.dim))}
        tq = tqdm(total=len(K), desc='[ voronoi')
        for dim in reversed(range(self.dim+1)):
            for s in K(dim):
                if not s in B:
                    self.add_dual(K, s)
                tq.update(1)
        tq.close()
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
