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

Useful sync features:

 - Mutex: You can use mutexes with `mutex.lock()` and `mutex.release()` when accessing same
   variables by different threads.
 - Joins: `joins()` is used in the parent thread to wait for the child thread to finish
   its execution.
 - Conditional Variables: With `Condition()` you can instatie them. It contains teh
   same functionalities as mutex (therefore you can lock and release) but you can also 
   `wait` and `notify` to make a thread wait and notify to wake up the waiting threads
   to re-evaluate the condition.
 - `Barrier(N)`. Used to make a thread wait for N more threads to be waiting. Once N
   threads reached the barrier, all of them will be woken up.
 - Waiting group: Self implemented class that can be used with the main methods:

     - `count`: Variable that keep tracks of how many threads are alive
     - `wait`: Wait till count > 0
     - `done`: substracts one to count
     - `add`: Add one to count. This can be done by either the main thread or any subthread by creating new subthreads.
