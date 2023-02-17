# Data structures

## Queue

First In First Out (FIFO). Its init method that not accept numbers. Main methods:

- `push`: Put element.
- `pop`: Remove element (returns void).
- `size`: Size of queue
- `front`: Front of the queue (element that will be popped).
- `back`: Back of the queue.

## Stack

First In Last Out (LIFO).

- `empty`: Check if empty.
- `size`: Check size
- `back`: Check the back. Elements are removed from here.
- `push_back`: Add element.
- `pop_back`: Remove element.

## Set

- `insert`: It admits either one value or two iterators (start and end).
- `erase`: Similar to `insert`.
- `size`: Similar to `insert`.
- `find`: Returns iterator pointing to element found. `end` if not found.
- `clear`: Clear the set
- `empty`: Check if empty.

## Vector

Main methods:

- `begin`: Iterator pointing to first element.
- `end`: Iterator pointing to last element.
- The two aboves can be combined with `r` for reverse (`rbegin`, `rend`) or `c` for
  constant (`cbegin`, `cend`) or both (`crbegin`, `crend`).
- `data`: returns pointer to first element.
- `push_back`: Push elements into vector
- `pop_back`: Pop elements from vector.
- `insert`: inserts new element at the specified position.
- `erase`: same as insert

## Map

Quite similar to python. Non existing keys are automatically added without any issue.
As main methods you have:

- `find`

## Arrays

These are usually fixed in size in compilation time:

```cpp
int a[] = {1,2,3,4};
int b[SIZE];
```

But can also be dynamic:

```cpp
// include <memory>
int* arr = new int (SIZE);
std::unique_ptr<int[]> ptr(arr);
delete [] arr;

// Alternative:
auto ptr = std::make_unique<int[]>(SIZE);
```
