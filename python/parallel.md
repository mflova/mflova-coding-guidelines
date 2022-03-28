# Parallel

## Multithreading

Typical for IO-bound problems, as Python executes the threads concurrently (same
processor). Handled by the GIL (Global Interpreter Lock). You can create threads
with:

```python
from threading import Thread

for i in range(3):
    t = Thread(target=my_func, args=())
    t.start()
```

You can use mutexes with `mutex.lock()` and `mutex.release()` when accessing same
variables by different threads.


## Multiprocessing
