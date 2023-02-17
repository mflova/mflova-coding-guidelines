# Templates

They can be used to minimize duplicated code


## Templated functions

Example:

```cpp
template <typename T> T myMax(T x, T y)
{
    return (x > y) ? x : y;
}
```

## Templates classes

```cpp
template <typename T> class Array {
    private:
        T* ptr;
        int size;
}
```

## Template specialization

If you wish to define a specific code for one specific type, you can do the following:

```cpp
// A generic sort function
template <class T>
void sort(T arr[], int size)
{
    // code to implement Quick Sort
}
 
// Template Specialization: A function
// specialized for char data type
template <>
void sort<char>(char arr[], int size)
{
    // code to implement counting sort
}
```
