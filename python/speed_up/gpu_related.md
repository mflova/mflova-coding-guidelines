# GPU related

This document explains some techniques that can be used for speeding up the code by using
a NVIDIA based GPU.

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

About how memory is transferred, creating an array with `cp` already allocates it in GPU
memory. There are two main methods to transfer this data from or to CPU.

```python
cp.asarray(np_arr_in_cpu)  # It will transfer CPU to GPU
cp.asnumpy(cp_arr_in_gpu)  # It will transfer GPU to CPU
```

## Dask

As a brief summary, this library allows you to work with extremely huge data. It
implements mirrored `numpy`, `pandas` or `list` based functions that can
overflow the memory. It also applies batch-optimization, which means that the library
will detect which operations can be ran in parallel. However, in order to be more
efficient, it needs to work with millions of values.

## cuDF

This library implements similar workflow compared to pandas. Capable of using GPU to speed
up pandas processing.