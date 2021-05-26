
class ComplexElement:
    def __init__(self, dim, *args, **data):
        self.dim, self.data = dim, data
    def __call__(self, key):
        if key in self.data:
            return self.data[key]
    def __eq__(self, other):
        return self.dim == other.dim
    def __lt__(self, other):
        pass
    def __getitem__(self, v):
        pass

class Complex:
    def __init__(self, dim):
        self.dim = dim
    def get_sequence(self, key, reverse=False):
        r = -1 if reverse else 1
        return sorted(self, key=lambda s: (r * s(key), s))
    def __repr__(self):
        return ''.join(['%d:\t%d elements\n' % (d, len(self(d))) for d in range(self.dim+1)])
    def __contains__(self, key):
        pass
    def __getitem__(self, e):
        pass
    def __call__(self, dim):
        pass
    def __iter__(self):
        pass
    def add_new(self, element, *args, **data):
        pass
    def add(self, element, *args):
        pass
    def get_faces(self, element):
        pass
    def get_cofaces(self, element):
        pass
