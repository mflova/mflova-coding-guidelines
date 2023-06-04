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
and `numpy` implement C-based code and their own vectorized instructions. Therefore,
it is always recommended to use all functions that operate over a set of data instead
of using for loops. These can come from basic operators such as `>` or `+`, or from
specific methods such as `np.sqrt`. For `numpy`. these are also
called `universal functions` or `ufunc`. They basically perform operations in an
element wise fashion but to a group of data. However, you can also create yours
(explained in next section.)

## Numba

`numba` is an optimization based library that performs huge speeds up. It works
quite well with raw for loops and `numpy` operations (therefore not `math` recommended).
It mainly performs two ideas to speed up the code:

- Just In Time (JIT) compilation with `@jit`: To pre-compile your function into machine
  code and cache its calls. Due to this compilation part, the compiler can apply multiple
  optimizations. Differently to `numpy`, this one does not compile to C first, but
  directly to machine code. 
- Vectorize (`@vectorize` or `@guvectorize`): To create your own universal functions.
  These functions use special vectorize-based instructions from the CPU.
- Stencil (with `@stencil` decorator): Common computational pattern in which array
  elements are updated according to some fixed pattern called the stencil kernel.
  This is typical for image processing algorithms, where the local value of the pixel
  is updated according to the value of neighbour pixels. This decorator is not explained
  in this guide.

How this is achieved?

In pure Python, When you launch the code, `Python` generates pre-compiled bytecode
(`.pyc`) files that the interpreter can understand line by line. However, this
pre-compiled code, due to the dynamism of Python, cannot be optimized. This is
why it is so slow.

On the opposite side, `numba` translates the code so that it can be used as input to
`LLVM` compiler. Then, this one performs the optimizations that any compiler can make
(loop fusion, better memory mamangement, inlining...)

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
    Recommended its use when data is more than 1KB at least.
 - `fastmath`: Sacrifice accuracy in exchange of speed
 - `cache`: Cache the compiled function into a file to avoid re-compilating it whenever
   the program is launched for the first time.

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
  universal functions” or gufuncs (`@guvectorize` below). Harder to set up but more
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
the decorator or not. If it is not done, `numba` will create a "dynamic universal
function". This means that when the code is running, it will perform the vectorization
depending on the type of data that it receives and it will cache the vectorized function
for its later use (lazy compilation). If we know the function signature, it is
recommended to use it. Then, the function can be called as:

```python
# being all A, B, C and D arrays
D = vec_operation(A, B, C)
```

Note that this decorator will make the function untyped. To fix it, you can also create
a wrapper around it.

#### Reduced vectorized functions

`numpy` allows to apply specific functions to any axis we want. Let's say for `np.mean`.
You can either compute the mean for all values or you ca specify the axis
like `np.mean(arr, axis=0)`. These are called reduced vectorized functions and can be
implemented with `numba` as well. This is done with `identity="reorderable`:

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
You can think of `@vectorize` as a specific and limited case of `@guvectorize`.

```python
from numba import guvectorize, int64

@guvectorize([(int64[:], int64, int64[:])], '(n),()->(n)', nopython=True)
def g(x, y, res):
    for i in range(x.shape[0]):
        res[i] = x[i] + y
```

In the example above, there are different things to take into account.
- In the decorator itself, the signature is specified.
- The second element indicates the data flow. Everything before the arrow means input.
  After it, outputs. All of them can be either a *1D ARRAY* with `n` elements (or any
  letter) with `(n)` or they can be a scalar `()`.
- Therefore, `numba` will manage the creation of the output arrays. This have a few
  consequences:
  - Outputs ALWAYS have to be of the type `xxx[:]` on the first part of the signature.
  - For the second part, depending on the dimensions of the output, it can be
    either `()` (scalar) or `(n)` (1D array). About this one, there are two main
    restrictions:
      - You cannot use integers here
      - Due to the generalization nature, every letter that appears in the right side,
        it has to be on the left side. More comments on this are done later.
  - When calling this function, we will do as `g(a,b)`. The third element (output) is
    not passed.
- We can also pass `nopython` flag for further optimization.

However, the explanation about `()` or `(n)` is more complex. In reality, the decorator
can work with dimensions higher than 1D. It is like if the decorator flattens the given
input arrays to a 1D array, apply the function, and then reshapes them back to its
original shape when it is returned. As an example, if we have `(n)->()`, it can mean:

- If we pass a 1D array, the returned value will be a scalar
- If we pass a 2D array, the returned value will be a 1D array
- And so on

But if we have `(n)->(n)`, the output will always be same dimension as the input.

With the code snippet above:

```python
>>> a = np.arange(6).reshape(2, 3)
>>> a
array([[0, 1, 2],
       [3, 4, 5]])
>>> g(a, 10)
array([[10, 11, 12],
       [13, 14, 15]])
>>> g(a, np.array([10, 20]))
array([[10, 11, 12],
       [23, 24, 25]])
```

Conclusion: In order to avoid confusion when writting your function, think as if you only
work with either scalars or 1D arrays.

##### More complex cases

As I said before, there are two main restrictions when writting the second part of the
decorator:

- All symbols appearing at right, must be at left
- All symbols must be letters, no numbers.

So what if I have a forward kinematic function that works with 5 joint values (or in
general, an array Nx5) and returns 3 points (Nx3)? How do we write the output?

```python
# We cannot do this, as we cannot use constants
@guvectorize([(float64[:], float64[:])], '(n)->(3)', nopython=True)
# We cannot do this, as `m` symbol is not defined on the left side
@guvectorize([(float64[:], float64[:])], '(n)->(m)', nopython=True)
```

How can it be solved?

The solution so far given can be found [HERE](https://github.com/numba/numba/issues/2797).
This is creating and passing a dummy array to indicate dimensions. This would be:

```python
@guvectorize([(float64[:], float64[:], float64[:])], "(n),(m) -> (m)")
def fk(ths: FloatArray, dummy: FloatArray, res: FloatArray) -> None:
  # Do nothing with `dummy`
  ...
```

As you can see in the example, we are not breaking any rules. Therefore, to call the
function we need to:

```python
# Suppose we have `arr`. This should be shape (N, 5).
N = len(arr)
dummy = np.zeros((N, 3), dtype=np.float64)
fk(arr, dummy)
```

By doing this and passing dummy, we are indicating to the generalized vectorized function
what's the shape of the output array (which will be same rows as the first array passed
but with 3 columns). This approach takes some extra time and memory to allocate that dummy
array, but it is still much faster than any other option.

##### More practical examples

Function `g()` receives an uninitialized array through the `res` parameter. Assigning
a new value to it doesn't modify the original array passed to the function. Note how
in the example below, `res` is `float64[:]` but it is denoted as an scalar in the
second element of the string. Note we since we do not know how many elements our function
will have (just `n`), we need to apply functions that apply to all of our 1D input array.
These are opperations that already work with vectors of data (`numpy`-based) like in
this example, or `for` loops like in the next example.

```python
@guvectorize([(float64[:], float64[:], float64[:])], '(n),(n)->()')
def g(x, y, res):
    res[:] = np.sum(x * y)
```

Source: https://stackoverflow.com/questions/66608336/weird-behavior-of-numba-guvectorize

Another example is where we can have multiple output arrays. Be aware how, since we do
not know hoy many elements we will have, we have to use a `for` loop to iterate over
all `n` elements. Next example will be different.

```python
@guvectorize(
    [(float64[:], float64[:], float64[:], float64[:])],
    "(n),(n)->(n),(n)",
    nopython=True)
def add_guvectorize(a, b, c, d):
    for i in range(len(a)):
        c[i] = a[i] + b[i]
        d[i] = a[i] + c[i]
```

Source: https://stackoverflow.com/questions/30417465/get-multiple-return-values-from-numba-vectorize

About the example analyzed in the section above (forward kinematics equation with 5 input
values and 3D point as output). In this example, although the first input array is `n`
elements according to the signature, we know that inside our function, it will be a
flattened 1D array with 5 elements. Since in our case is ALWAYS going to be 5, instead of
iterating with a for loop over all elements as we did in the examples above, we can just
grab/index the first five elements and implement the algorithm with these only values:

```python
@guvectorize([(float64[:], float64[:], float64[:])], "(n),(m) -> (m)", target="parallel", nopython=True)
def forward_kinematics(angle: FloatArray, dummy: FloatArray, res: FloatArray) -> None:
    th1 = ths[0]
    th2 = ths[1]
    th3 = ths[2]
    th4 = ths[3]

    # Here you perform calculations and store results in res[0], res[1] and res[2]

dummy = np.zeros((len(joints), 3), dtype=np.float64)
forwad_kinematics(joints, dummy)
```

You can read more information about the `dummy` array above.



### GPU and cuda

There are two main approaches:
- `@vectorize` with flag `target="cuda"`: Easier to implement. You dont need to manage
  memory, threads, blocks, syncornization or any other hardware related
  stuff. `numba` infers all of it for you.
- `@cuda.jit` this one is much harder, having to manage all the things mentioned before.
  However, the user has better control. This one will not be explained in this guide.

Be aware that when working with CUDA, you can only do a reduced number of things. For
example, you cannot build a list. You have to think from the point of view of C and arrays.

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
    5. Numba guvectorization (if possible to implement)
    5. Numba vectorization with `target=parallel` (if heavy enough)
    6. Numba with cuda vectorization `target=cuda` (if operation is heavy enough that
       compensates memory transfers)

Official numba website recomends using `target=cpu` for data less than 1KB.
`target=parallel` for data less than 1MB and `target=cuda` for greater than
1MB and with heavy computation. However, it depends a lot on the use case,
so it is better to experiment.

## Cupy

Library that is meant to use `cuda` (NVIDIA API) for `numpy` and `scipy`. This library
literally implements mirrored functions coming from these modules. Example:

```python
import numpy as np
import cupy as cp
x_gpu = cp.array([1, 2, 3])


x_cpu = np.array([1, 2, 3])
l2_cpu = np.linalg.norm(x_cpu)

x_gpu = cp.array([1, 2, 3])
l2_gpu = cp.linalg.norm(x_gpu)
```

About how memory is transfered, creating an array with `cp` already allocates it in GPU
memory. There are two main methods to transfer this data from or to CPU.

```python
cp.asarray(np_arr_in_cpu)  # It will trasnfer CPU to GPU
cp.asnumpy(cp_arr_in_gpu)  # It will transger GPU to CPU
```