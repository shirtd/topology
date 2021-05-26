from topology.util import diff

from itertools import combinations
import numpy.linalg as la
import numpy as np


def tet_circumcenter(T):
    alpha = np.array([[a[0], a[1], a[2], 1] for a in T])
    Dx = np.array([[a[0]*a[0] + a[1]*a[1] + a[2]*a[2], a[1], a[2], 1] for a in T])
    Dy = np.array([[a[0]*a[0] + a[1]*a[1] + a[2]*a[2], a[0], a[2], 1] for a in T])
    Dz = np.array([[a[0]*a[0] + a[1]*a[1] + a[2]*a[2], a[0], a[1], 1] for a in T])
    return np.array([la.det(Dx), -1*la.det(Dy), la.det(Dz)]) / (2 * la.det(alpha))

def tri_circumcenter(T):
    ca, ba = T[2] - T[0], T[1] - T[0]
    xca = la.norm(ca) ** 2 * np.cross(np.cross(ba, ca), ba)
    xba = la.norm(ba) ** 2 * np.cross(np.cross(ca, ba), ca)
    return T[0] + (xca + xba) / (2 * la.norm(np.cross(ba, ca)) ** 2)

def tri_circumradius_l(a, b, c):
    return a*b*c / np.sqrt((a+b+c)*(b+c-a)*(c+a-b)*(a+b-c))

def tri_circumradius(T):
    return tri_circumradius_l(*map(la.norm, map(diff, combinations(T, 2))))

def tet_circumradius(T):
    return la.norm(T[0] - tet_circumcenter(T))

def torus(r1=0.5, r2=1, n=64):
    r1, r2 = 0.5, 1
    phi, theta = np.linspace(-np.pi, np.pi, n), np.linspace(-np.pi, np.pi, n)
    x = (r1 * np.cos(phi) + r2) * np.cos(theta)
    y = (r1 * np.cos(phi) + r2) * np.sin(theta)
    z = r1 * np.sin(phi)
    return np.vstack((x,y,z)).T

def ripple(x, y, f=1, l=1, w=1):
    t = la.norm(np.stack((x, y), axis=2), axis=2) + 1/12
    t[t > 1] = 1.
    return (1 - t) - np.exp(-t / l) * np.cos(2*np.pi*f*(1-t) * np.sin(2*np.pi*w*t))
