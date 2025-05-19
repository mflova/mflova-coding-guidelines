# JAX

Jax is extremely powerful for array based computation on big sizes. It mainly sues an
async-based engine and XLA to compile the functions to a more optimized versions. It has
many possibilities. It can work with dictionaries and jax based arrays and its API is
almost identical to numpy. It also has another scipy-based API that replicates its
functionalities.

## Common issues

Be aware that JAX by default works with 32 bits as opposed to numpy (32 bits). Whenever
you prepare a benchmark, make sure that there is no implicit conversion between the input
arrays otherwise you might be timing the computation time plus the conversion dtype, which
is huge.

## Profiling

Jax can generate a dashboard with the different traces involves just by wrapping your code
into the following context manager:

```py
with jax.profiler.trace("/tmp/jax-trace", create_perfetto_link=True):
    # Your code
```

## JIT

Jut in time compilation works similar to `numba`'s one. It is used as a decorator and it
will automatically speed up the code by compiling the function and using it whenever the
function is called. The way it works is by assigning two different types of data to the
input arguments: dynamic traces and static. The dynamic ones are typically array or
PyTrees (casted as Python dictionaries, tuples and list). JAX JIT will check how thees
traces evolve after execution the function (i.e shape). This means that, if we give an
input array with different shape, the function will need to be recompiled. Compilation
will take less time if we tend to use primitives and methods that are closer to XLA
(`jax.lax`) instead of Python-native for loops. In general, if it is not possible to
analyze how the traces change, the function cannot normally be JITTED. Therefore, we
should mark as static arguments all those input arguments that modify the traces. These
must be known at compilation time.

## Vectorization

Same as `vectorize` and `guvectorize`, `jax` has `vmap`. It simplifies the workflow quite
a lot. You only need to write the function at a scalar level and then you can "elevate"
the dimensions by using `jax.vmap`. This function has some input arguments to specify how
the dimensions should be staked to have more control. Examples:

```py
vmap_f = jax.vmap(f, in_axes=0)  # Apply the funcion towards axis 0. This is arr[0], arr[1]...
# If we have a vector, it will be element by element.
# If instead, the function was written to work with a vector of, let's say, 5 numbers, if we pass a (n, 5),
# it will be applied row by row
```

## Sharding

Sharding allows to map different regions of an array into multiple devices (GPU, TPUs...).
However, for the CPU case, multiple devices can also mean multiple cores. The only needed
thing is defining a sharding map for the array. Once this is done, any operation made on
it will be splitted depending on the map defined. No matter if we use any operation like
`jnp.cos` or a whole function.

We can easily combine all th eprevious techniques. For example:

```py
# Before importing JAX we set the flag to indicate how many cores are detected as different devices
import os
os.environ["XLA_FLAGS"] = '--xla_force_host_platform_device_count=20'
import jax

# func is defined as a function expects a vector of 5 elements
# With vmap we vectorize it so that it takes (n, 5)
# And previously, we map the corresponding array to divide the rows into 20 cores.
# The product 20 x 1 has to be the same as the previous flag we set.
print(jax.devices())  # We should see 20 cores as different devices
mesh = jax.make_mesh((20, 1), ('x', 'y'))
arr = jax.device_put(arr, NamedSharding(mesh, P('x', 'y')))
func_vmap = jax.jit(jax.vmap(func, in_axes=0))
```

We can also visualize the sharding map with:

```py
jax.debug.visualize_array_sharding(arr)
```

However, the if we choose a mesh of 20x1 and the array is not divisible by this mesh, it
will throw an error. One recommended and common solution is to perform padding and fill
the array until we reach the next size that is divisible by our mesh. However, it is
important to indicate that adding the padding can be quite expensive if not done through
JIT.

## Optimization

For math-based optimization, `jaxopt` was typically the option to go. Now it seems to be divided between: 
    - `optix` (more first order methods like gradient-descent): Typically for very high
      dimensional problems like deep learning.
    - `optimistix` (more similar to `jaxopt`): With classy methods like Levenberg-Marquadt
      or trust-region based.
