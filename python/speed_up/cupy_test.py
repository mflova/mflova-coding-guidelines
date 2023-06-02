import math
import timeit

import cupy as cp
import numba
import numpy as np
from numba import float64

# Crear un arreglo en la CPU
N = 100000000

cp_array = cp.arange(N)
np_array = np.arange(N)


def cp_sin(cp_data):
    return cp.sin(cp_data)


def cp_sin_all(np_data):
    data = cp.sin(cp.array(np_data))
    return data.get()


def np_sin(np_data):
    return np.sin(np_data)


@numba.jit(nopython=True)
def jit_sin(data):
    return np.sin(data)


@numba.vectorize([float64(float64)], nopython=True)
def vectorized_sin(data):
    return math.sin(data)


n = 3
t = timeit.timeit(lambda: np_sin(np_array), number=n)
print(f"Array with {N} elems")
print(f"Time with numpy: \t{t/n}")
t = timeit.timeit(lambda: cp_sin(cp_array), number=n)
print(f"Time with cupy: \t{t/n}")
t = timeit.timeit(lambda: cp_sin_all(np_array), number=n)
print(f"Time cupy + memory: \t{t/n}")
t = timeit.timeit(lambda: jit_sin(np_array), number=n)
print(f"Time jit: \t\t{t/n}")
t = timeit.timeit(lambda: vectorized_sin(np_array), number=n)
print(f"Time vectorized: \t{t/n}")
