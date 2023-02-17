# Parallelism and concurrency

Parallelism is the property of a system to execute multiple tasks simultaneously by
dividing the workload among multiple processors or cores. The goal of parallelism is to
complete a task faster by dividing it into smaller parts that can be executed
simultaneously.

Concurrency, on the other hand, is the property of a system to appear to be executing
multiple tasks simultaneously, even though only one task is actually executing at a time.
In a concurrent system, tasks are interleaved, and each task makes progress in small,
incremental steps. The goal of concurrency is to improve the responsiveness and
scalability of a system by allowing multiple tasks to run in the background, without
blocking the main thread.

## Main objects

- `std::thread`: Its main method is `join()`, whose method returns when the thread
  execution has completed.
- `std::mutex`: Only one thread will access a given object. It can be used with
  `m.lock()` or `m.unlock()`, but this one is not exception safe. For this, you can use
  `lock_guard`
- `std::semaphore`: Same as mutex but with multiple threads.
- `std::condition_variable`: Thread will wait till a condition is met. It can be also
  others set up for threads to notify all threads.
- `std::lock_guard`: is a RAII (Resource Acquisition Is Initialization) wrapper for a
  `std::mutex`. It automatically acquires the mutex when it is constructed and releases
  the mutex when it goes out of scope. This makes it easy to write correct,
  exception-safe code that uses mutexes to protect shared data.
- `std::unique_lock`: A `std::unique_lock` is similar to `std::lock_guard`, but provides
  more flexibility in terms of when the mutex is acquired and released. For example,
  you can use a `std::unique_lock` to conditionally acquire a mutex, or to temporarily
  release the mutex while waiting for a condition variable.

## Examples

Redundant objects. It is only to show how they are used.

```cpp
#include <iostream>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <semaphore.h>

std::mutex mtx;
std::condition_variable cv;
sem_t semaphore;
int buffer = 0;
bool ready = false;

void producer() {
  // Acquire the semaphore
  sem_wait(&semaphore);

  // Acquire the mutex and update the buffer
  {
    std::lock_guard<std::mutex> lock(mtx);
    buffer = 42;
    ready = true;
  }

  // Notify the consumer that the buffer has been updated
  cv.notify_one();

  // Release the semaphore
  sem_post(&semaphore);
}

void consumer() {
  // Acquire the semaphore
  sem_wait(&semaphore);

  // Wait for the buffer to be updated
  std::unique_lock<std::mutex> lock(mtx);
  cv.wait(lock, []{return ready;});

  // Print the value of the buffer
  std::cout << "The value of the buffer is: " << buffer << std::endl;

  // Release the semaphore
  sem_post(&semaphore);
}

int main() {
  // Initialize the semaphore
  sem_init(&semaphore, 0, 1);

  // Start the producer and consumer threads
  std::thread t1(producer);
  std::thread t2(consumer);

  // Wait for the threads to finish
  t1.join();
  t2.join();

  // Destroy the semaphore
  sem_destroy(&semaphore);

  return 0;
}
```

## Atomic

These are variables that automatically handle multiple threads accessing these variables.
This will make the code simpler compared to using mutex. However, for more complex
requirements, atomics might not be the most suitable solution. This option is typically
faster specially if the platform has HW acceleration.

```cpp
#include <iostream>
#include <thread>
#include <atomic>

std::atomic<int> counter(0);

void incrementCounter() {
    for (int i = 0; i < 100000; ++i) {
        ++counter;
    }
}

int main() {
    std::thread firstThread(incrementCounter);
    std::thread secondThread(incrementCounter);

    firstThread.join();
    secondThread.join();

    std::cout << "Final counter value: " << counter << std::endl;
    return 0;
}
```
