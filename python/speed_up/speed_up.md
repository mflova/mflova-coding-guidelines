# Speed up

This guide contains everything related to making the code quicker.

## Making the algorithm more efficient

Analyze the time complexity of the algorithm and tackle the weak points. Not much attention
is given here as this is supposed to be known.

### Pandas

Specific tips for `pandas`:
 - Always avoid `iterrows`. Use `itertuples` instead.

## Concurrent futures

Library provided by built-in Python to easily handle multiprocessing/multithreading.
These are the main differences:

Multithreading:

    - Single core
    - Shared memory, no needed to copy anything to a different memory
    - Concurrency based. This means that it is ideal for those algorithms with low
      computation but long waiting times (waiting for website request for example)

Multiprocessing:

    - Multi core
    - Non shared memory. Therefore, the process of copying data into different
      memory zones can be slower.
    - Multi process based. This means it is ideal for high computation load.


This library uses `Pool` objects to manage all resources. From it, the `executor` derives.
Important note: These features need to be called from a script with `if main`. Otherwise
it will crash.

The example belows are written for multiprocessing, but it is the same for
multithreading. You only need to use the `ThreadPoolExecutor`.

### Multiprocessing and multithreading

Executor mainly uses two methods:

- `map` similart to the built-in map but applied in parallel. It takes a function and an
  iterable that will be applied to each element. The executor will returns an iterator.
  Each element represents the status of the task. If you iterate over this, it will
  block the Python execution. You can see it as a generator.

```python
from concurrent.futures import  ProcessPoolExecutor

def square(number):
    return number ** 2

if __name__ == '__main__':
    numbers = [1, 2, 3, 4, 5]
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = executor.map(square, numbers)
        # The program will continue, but if you start iterating over `results` it will block.
```

- `submit`: Send a function with its arguments to be launched in multiprocess way.
  Differently to `map`, this time the returned object is an iterable of `Future` and
  the blocking part comes when you call `result()` to retrieve the returned value.

```python
from concurrent.futures import ProcessPoolExecutor

def square(number):
    return number ** 2

if __name__ == '__main__':
    with ProcessPoolExecutor(max_workers=4) as executor:
        numbers = [1, 2, 3, 4, 5]

        futures = []

        for number in numbers:
            # You can pass different arguments to each function call
            future = executor.submit(square, number)
            futures.append(future)  # This will make our list have the same launch order
            # Alternative: You can also put executor.submit under a list comprehension

        for future in futures:
            result = future.result()  # Blocking call
            print(result)
```

## Vectorization

Vectorize speeds up the algorithms by using Single Instruction Multiple Data (SIMD).
These are special instructions from the CPU that allow to apply the same instruction
to a "vector" of data instead to a individual values. Libraries such as `pandas`
and `numpy` implement their own vectorized instructions. Therefore, it is always
recommended to use all functions that operate over a set of data instead of using
for loops. These can come from basic operators such as `>` or `+`, or from specific
methods such as `np.sqrt`. For `numpy`. these are also called `universal functions`
or `ufunc`. They basically perform operations in an element wise fashion but to a
group of data. However, you can also create yours (explained in next section.)

## Numba

`numba` is an optimization based library that performs a huge speeds up. It works
quite well with raw for loops and numpy operations. It mainly performs two ideas to
speed up the code:

- Just In Time (JIT) compilation: To pre-compile your function and cache its calls.
- Vectorize: To create your own universal functions.

### Just in time compilation

It pre-compiles a function on its first call and cache the results for further
calls (lazy compilation). Therefore, first call will always be much slower. Done
by using its main decorator:

```python
form numba import jit 

@jit(nopython=True)
def jit_operation(a: FloatArray, b: FloatArray, c: FloatArray) -> FloatArray:
    results = np.zeros((len(a)))
    for idx, (a_value, b_value, c_value) in enumerate(zip(a, b, c)):
        results[idx] = math.sqrt(b_value**2 - 4 * a_value * c_value)
    return results
```

This loop is extremely quick. More than its equivalent with numpy.

Interesting flags that you can add:

 - `nopython`: Forces all the code to be compiled. If there is a problem, a exception
    is raised. Recommended to alwyas have it set to `True`.
 - `parallel`: It will analyze the code and parallelize (multithread) if possible.
    You can also use  `prange` instead of `range` to explicitely indicate parallel loops.
 - `fastmath`: Sacrifice accuracy in exchange of speed

 When using `nopython` mode, it will try to parse all code, meaning that no python
 interpreter will be used. If there is something it cannot parse, it will raise an
 exception instead of falling in `object` mode. This decorator does not need any type hints.


### Vectorize

When you need to execute specific functions, you might reach a point in which you need to
perform for loops again. If you want to avoid this, this section explains how to create
custom vectorized operations. There are two types of vectorization:

- Those which operate on scalars, these are “universal functions” or ufuncs: Simpler to
  set up but worse flow control.
- Those which operate on higher dimensional arrays and scalars, these are “generalized
  universal functions” or gufuncs (@guvectorize below). Harder to set up but more
  possibilities.

Compared to `jit`, first calls to vectorized functions do not take extra time. All
decorators explained here also admit the same ones explained with `jit`.

#### @vectorize

The idea is that you create a function that admits one or multiple scalars and returns
ONLY one. Then, by adding the decorator, your function will admit whole vectors.

```python
from numba import float32, float64, vectorize

# V1
@vectorize
def vec_operation(a: float, b: float, c: float) -> float:
    return math.sqrt(b**2 - 4 * a * c)

# V2
@vectorize([float32(float32, float32, float32), float64(float64, float64, float64)], nopython=True)
def vec_operation(a: float, b: float, c: float) -> float:
    return math.sqrt(b**2 - 4 * a * c)

```

As you can see in the example above, you can specify the signature of the function in
the decorator or not. If it is not done, `numba` will perform lazy compilation. This
means that when the code is running, it will perform the vectorization depending on
the type of data that it receives and it will cache the vectorized function for its
later use. If we know the function signature, it is recommended to use it. Then,
the function can be called as:

```python
# being all A, B, C and D arrays
D = vec_operation(A, B, C)
```

Note that this decorator will make the function untyped. To fix it, you can also create
a wrapper around it.

#### Reduced vectorized functions

`numpy` allows to apply specific functions to any axis we want. Let's say for `np.mean`. You can either compute the mean for all values or you ca specify the axis like `np.mean(arr, axis=0)`. These are called reduced vectorized functions and can be implemented with `numba` as well. This is done with `identity="reorderable`:

```python
@vectorize(
    [
    int64(int64,int64), 
    float32(float32,float32), 
    float64(float64,float64)
    ],
    identity="reorderable"  # This flag is the key
)
def numba_add(x, y):
    return x + y

# Note how reduce is used to create a reduced version of the function
numba_add.reduce(a, axis=0)
numba_add.reduce(a, axis=1)
```


#### @guvectorize

This one is more complex but gives more possibilities. Among them, returning multiple
values. However, these do not work in a element wise fashion way, but in a matrix way.

```python
from numba import guvectorize, float64
import numpy as np

ones = np.ones((3, 3))
twos = ones * 2

@guvectorize(
    [(float64[:], float64[:], float64[:], float64[:])],
    "(n),(n)->(n),(n)",
    nopython=True)
def add_guvectorize(a, b, c, d):
    for i in range(len(a)):
        c[i] = a[i] + b[i]
        d[i] = a[i] + c[i]
threes, fours = add_guvectorize(ones, twos)
```

In the eexample above, there are different things to take into account.
- In the decorator itself, the signature is specified.
- The second element indicates the data transfer. This is which parameters work
  as `input` and which ones as `output`. In the example we can see that the first 2
  variables are inputs and the 2 last variables are outputs.
- Therefore, in order to store the results, we need to pass the array that will
  store them and modify them inside the generalized universal function.


### GPU and cuda

There are two main approaches:
- `@vectorize` with flag `taget="cuda"`: Easier to implement. You dont need to manage memory, threads, blocks, syncornization or any other hardware related stuff. `numba` infers all of it for you.
- `@cuda.jit` this one is much harder, having to manage all the things mentioned before. However, the user has better control. This one will not be explained in this guide.

#### @vectorize with target cuda
Important note: Check that cuda is properly set up in the computer
before (check `cuda.md`).

Numba also supports GPU computing. You only need a vectorized function and setting
up the following flag:

```python
from numba import float64, float32, vectorize

@vectorize([float32(float32, float32, float32), float64(float64, float64, float64)], target="cuda")
def cu_operation(a: float, b: float, c: float) -> float:
    return math.sqrt(b**2 - 4 * a * c)
```

However, be aware that the computation has to be so heavy in order to compensate
all memory transfer to GPU.

### Speed up comparison

After a few tests, it has been seen that the best performances are achieved with:
Usually, this is the speed up order, from low to high:

    1. For loops
    2. Numpy vectorized operations
    3. Numba jit with pre-compiled function
    4. Numba vectorization.
    5. Numba vectorization with `target=parallel` (if heavy enough)
    6. Numba with cuda vectorization `target=cuda` (if operation is heavy enough that
       compensates memory transfers)

## Cupy
Library that is meant to use `cuda` (NVIDIA API) for `numpy` and `scipy`. This library literally
implements a mirrored functions coming from these modules. Example:

```python
import numpy as np
import cupy as cp
x_gpu = cp.array([1, 2, 3])


x_cpu = np.array([1, 2, 3])
l2_cpu = np.linalg.norm(x_cpu)

x_gpu = cp.array([1, 2, 3])
l2_gpu = cp.linalg.norm(x_gpu)
```

About how memory is transfered, here is a more detailed example:

```python
import cupy as cp

# Allocates mmemory in CPU
cpu_array = cp.arange(10)
# Allocates memory in GPU
gpu_array = cp.array(cpu_array)
# Perform operation (result stored in GPU)
gpu_result = cp.sin(gpu_array)
# Copy the result back to the CPU memory
cpu_result = gpu_result.get()
```