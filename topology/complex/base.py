
class ComplexElement:
    def __init__(self, dim, **data):
        self.dim, self.data = dim, data
    def key(self):
        pass
    def __iter__(self):
        pass
    def __call__(self, key):
        if key in self.data:
            return self.data[key]
    def __eq__(self, other):
        return hash(self) == hash(other)
    def __hash__(self):
        return hash(self.key())
    def __lt__(self, other):
        return self.key() < other.key()

class Complex:
    def __init__(self, dim):
        self.dim = dim
    def __iter__(self):
        pass
    def __call__(self, dim):
        pass
    def faces(self, element):
        pass
    def cofaces(self, element):
        pass
    def closure(self, s):
        return {s}.union({f for t in self.faces(s) for f in self.closure(t)})
    def __repr__(self):
        return ''.join(['%d:\t%d elements\n' % (d, len(self(d))) for d in range(self.dim+1)])
    def get_sequence(self, key, reverse=False):
        r = -1 if reverse else 1
        return sorted(self, key=lambda s: (r * s(key), s))
