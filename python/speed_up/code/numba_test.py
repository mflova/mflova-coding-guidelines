"""
Conclusions

Usually, this is the speed up order:
    1) For loops
    2) Numpy vectorized operations
    3) Numba jit with pre-compiled function
    4) Numba vectorization. First call does not take extra time.
    5) Numba vectorization with target parallel (if heavy enough)
    6) Numba with cuda vectorization (if operation is heavy enough that compensates memory transfers)
"""
import math
from numba import vectorize, jit, float32, float64
import numpy as np
import timeit
from numpy.typing import NDArray
from typing import Union


FloatArray = NDArray[Union[np.float64, np.float32]]


@vectorize([float32(float32, float32, float32), float64(float64, float64, float64)], target="cuda")
def cu_operation(a: float, b: float, c: float) -> float:
    return math.sqrt(b**2 - 4 * a * c)


@vectorize([float32(float32, float32, float32), float64(float64, float64, float64)], nopython=True)
def vec_operation(a: float, b: float, c: float) -> float:
    return math.sqrt(b**2 - 4 * a * c)


@jit(nopython=True)
def jit_operation(a: FloatArray, b: FloatArray, c: FloatArray) -> FloatArray:
    results = np.zeros((len(a)))
    for idx, (a_value, b_value, c_value) in enumerate(zip(a, b, c)):
        results[idx] = math.sqrt(b_value**2 - 4 * a_value * c_value)
    return results


def np_operation(a: FloatArray, b: FloatArray, c: FloatArray) -> FloatArray:
    return np.sqrt(b**2 - 4 * a * c)


def operation(a: FloatArray, b: FloatArray, c: FloatArray) -> FloatArray:
    results = np.zeros((len(a)))
    for idx, (a_value, b_value, c_value) in enumerate(zip(a, b, c)):
        results[idx] = math.sqrt(b_value**2 - 4 * a_value * c_value)
    return results


N = 1_000_000
dtype = np.float64

# prepare the input
A = np.array(np.random.sample(N), dtype=dtype)
B = np.array(np.random.sample(N) + 10, dtype=dtype)
C = np.array(np.random.sample(N), dtype=dtype)

# Results
n = 5
print(f"Total size: {N}")
t = timeit.timeit(lambda: operation(A, B, C), number=n)
print(f" - Time with for loop: \t\t\t{t/n:.4}")
t = timeit.timeit(lambda: np_operation(A, B, C), number=n)
print(f" - Time with np: \t\t\t{t/n:.4}")
t = timeit.timeit(lambda: jit_operation(A, B, C), number=1)
print(f" - Time with jit (first call): \t\t{t/1:.4}")
t = timeit.timeit(lambda: jit_operation(A, B, C), number=n)
print(f" - Time with jit (pre-compiled): \t{t/n:.4}")
t = timeit.timeit(lambda: vec_operation(A, B, C), number=n)
print(f" - Time with numba vectorization: \t{t/n:.4}")
t = timeit.timeit(lambda: cu_operation(A, B, C), number=n)
print(f" - Time with cuda vectorization: \t{t/n:.4}")