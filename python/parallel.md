# Parallel

This information is mainly outdated. For simple parallel programs, it is
recommended to use the library `concurrent.futures` and `Pool`'s objects.
There is more info about it in `speed_up.md`

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
 - Conditional Variables: With `Condition()` you can instatie them. It contains the
   same functionalities as mutex (therefore you can lock and release) but you can also 
   `wait` and `notify` to make a thread wait and notify to wake up the waiting threads
   to re-evaluate the condition.
 - `Barrier(N)`. Used to make a thread wait for N more threads to be waiting. Once N
   threads reached the barrier, all of them will be woken up.
 - Waiting group: Self implemented class that can be used with the main methods:

     - `count`: Variable that keep tracks of how many threads are alive
     - `wait`: Wait till count > 0
     - `done`: subtracts one to count
     - `add`: Add one to count. This can be done by either the main thread or any
       subthread by creating new subthreads.

 - Shared memory: In threads memory is shared. You have extra objects such as `queue`
   from `Queue`. You can also use the `queue` from `multiprocessing` for processes (it
   implements an inner lock).
 - Sending data among processes: `Pipe` from `multiprocessing` creates a pipe (1on1
   communication that can be uni or bidirectional). THe object creates a 2 elements
   tuple that can be passed to two processes to share information among them. Queue can
   be used to share data as well. This one can be N on M (not only 1 on 1). You can
   also use `array` from multiprocessing for this.

## Design patterns

### Pipeline pattern

Pattern used when you have a few functions that are executed in order and having a
dependent relationship, like in an assembly line. In this case, instead of waiting the
first function to do all the job and then switching to the second function, this
pattern suggests using pipelines to start adding jobs to the pipeline. Then, the next
function would be hearing this pipeline and processing the incoming jobs. When the
entire process consists of N steps or functions, you will need to create N-1 pipes.
Each pipe connects two related or consecutive steps. Therefore, here is an example with
processes, being each function a different process:

```python
def first_step(connection_A)  # Send messages through A pipe
def second_step(connection_A, connection_B)  # Receive messages through A and send new
                                             # messages to the next step through B
def third_step(connection_B)  # Receives messages through B
```

### Thread pool

A master thread sends jobs to a queue and then all the other child processes are
listening to this queue. If there is a new job, any of these will take it out and
process it.
