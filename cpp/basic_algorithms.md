# Basic algorithms

## Find elements in vector

`std::find` returns an iterator the first element in the range that
compares to `elem`. `last` if not found.

```cpp
std::find(A.begin(), A.end(), elem) != A.end();
```

## Remove elements from vector

`std::remove_if` will move all indicated elements from a container to the end. This
function will not change the size of the container and will return an iterator pointing
to the first element moved. Therefore, if you want to remove them, you can use it in
combination with `vector.erase()` by providing that returned value as `begin` and an
iterator pointing to the end of the container.

```cpp
std::remove_if(it_start, it_end, predicate_lambda_function);
// Predicate is a function that returns a boolean
// Example
auto aux = std::remove_if(v.begin(), v.end(), [&](const int x){return x%2==0});
v.erase(aux, v.end());
```
