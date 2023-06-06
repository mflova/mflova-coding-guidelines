# Concurrent futures

Note: Python implements different ways of parallelism. This is found to be the easiest one
and that covers most of the use cases.

Library provided by built-in Python to easily handle multiprocessing/multithreading.
These are the main differences between both techniques:

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

Be aware that when working with big arrays, these values need to be copied from RAM
memory to the CPU cache in order to perform operations on them. Therefore, it is not
always obvious which ones are CPU-bounded problems (multiprocessing better) or
IO-bounded problems (multithreading better)

This library uses `Pool` objects to manage all resources. From it, the `executor` derives.
Important note: These features need to be called from a script with `if main`. Otherwise
it will crash.

The example belows are written for multiprocessing, but it is the same for
multithreading. You only need to use the `ThreadPoolExecutor`.

## Multiprocessing and multithreading

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