# std

Main functions to know:

## Containers

Those that store a collection of objects:
`std::vector`, `std::list`, `std::map`, `std::set`

## Algorithms

### std::sort

Sort elements in ascending order. Complexity `O(N·log(N))`.
If a `comp` function is provided, `sort` will swap numbers if `False` is returned.

```cpp
void sort( RandomIt first, RandomIt last );
void sort( RandomIt first, RandomIt last, Compare comp );

// Examples
std::sort(s.begin(), s.end()); // Ascending order
std::sort(s.begin(), s.end(), std::greater<int>()); // Descending order
// With lambda (ascending)
std::sort(s.begin(), s.end(), [](int a, int b)
                              {
                                  return a < b;
                              });
```

### std::find

Returns iterator poitning to end if the element could not be found.

```cpp
v.find(elem);
```

### std::search

Searches for the first occurrence of the sequence of elements `[s_first, s_last)` in the
range `[first, last)`. Elements are compared using operator==.

```cpp
ForwardIt1 search( ForwardIt1 first, ForwardIt1 last,
                   ForwardIt2 s_first, ForwardIt2 s_last );
// Returned value related to the first container It1, so if it is equal to end, the
sequence could not be found.
```

### std::for_each

Apply a function to every single element of the container. Example:

```cpp
std::for_each(v.begin(), v.end(), [](int& x){x++;});
```

### std::transform

Similar to `for_each`. Difference is that this function will store the result into a
different container.

```cpp
#include <algorithm>
std::vector<std::string> names = {"hi", "test", "foo"};
std::vector<std::size_t> name_sizes;

std::transform(names.begin(), names.end(), std::back_inserter(name_sizes), [](const std::string& name) { return name.size();});
```

### std::accumulate

Computes the sum of the given value init and the elements in the range
[first, last).
Requires `#include <numeric>`.

```cpp
T accumulate( InputIt first, InputIt last, T init );
```

Returns the result.

## Smart pointers

See `smart_pointers.md`. These are mainly `std::unique_ptr`, `std::shared_ptr`, `std::weak_ref`.

## Input/Output

These are:

- `std::cin`
- `std::cout`
- `std::getline`
- `std::scanf`
- `std::printf`

## Exceptions

These are:

- `std::exception`
- `std::throw`
- `std::try`
- `std::catch`

```cpp
try {
   // protected code
} catch( ExceptionName e ) {
  // code to handle ExceptionName exception
}
```

## String manipulation

All these methods are applied to `char` or `char []`.

### std::getline
### std::toupper
### std::tolower
### std::stoi
