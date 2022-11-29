# from numba import vectorize, float64
import numpy
from typing import Optional
from scipy.interpolate import InterpolatedUnivariateSpline

def calculate_eulerian_strain(v0, vs):
    raise NotImplementedError

def from_eulerian_strain(v0, fs):
    raise NotImplementedError

def polynomial_least_square_fitting(xs, ys, new_xs, order: Optional[int] = 3):
    raise NotImplementedError


def get_static_p_of_v(v_sparse, f_sparse, v0 = None, N = 100, order = 3, v_ratio = 1.2) -> callable:
    raise NotImplementedError


def get_static_f_of_v(v_sparse, f_sparse, v0 = None, N = 100, order = 3, v_ratio = 1.2) -> callable:
    raise NotImplementedError


def to_eulerian_strain(v_array, v0):
    return (v0 / v_array) ** (2/3) - 1


def fit_p_of_v(vs, ps, order=3, v0 = None):
    
    if v0 == None: v0 = numpy.min(vs)
    xs = to_eulerian_strain(vs, v0)
    p = numpy.polyfit(xs, ps * vs, deg=order)
    
    def p_of_v(v_array: numpy.array) -> numpy.array:
        x_array = to_eulerian_strain(v_array, v0)
        c_array =  numpy.polyval(p, x_array) / v_array
        return c_array
    
    return p_of_v


def fit_f_of_v(vs, fs, order=3, v0 = None) -> callable:

    v0 = v0 if v0 != None else vs[numpy.argmin(fs)]
    xs = to_eulerian_strain(vs, v0)
    p = numpy.polyfit(xs, fs, deg=order)

    def f_of_v(v_array: numpy.array) -> numpy.array:
        x_array = to_eulerian_strain(v_array, v0)
        f_array = numpy.polyval(p, x_array)
        return f_array

    return f_of_v


def get_p_of_v_from_f(vs, fs, order=3, v0 = None) -> callable:

    v0 = v0 if v0 != None else vs[numpy.argmin(fs)]
    xs = to_eulerian_strain(vs, v0)
    p = numpy.polyfit(xs, fs, deg=order)
    
    def static_p_of_v(v_array: numpy.array) -> numpy.array:
        x_array = to_eulerian_strain(v_array, v0)
        dx_dv = - 2 / 3 * (x_array + 1) / v_array
        df_dx = numpy.polyval(numpy.polyder(p, 1), x_array)
        p_array = - df_dx * dx_dv
        return p_array

    return static_p_of_v