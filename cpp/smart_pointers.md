# Smart pointers

## unique_ptr

Unique owner. Example:

```cpp
  auto array = std::make_unique<int[]>(SIZE); // C++14
  // Note: <> is the type. () are the arguments passed to the constructor of that type.
```

Parenthesis represents the arguments that will be forwarded to the constructor of the
object. If the object is already created, you can also do:

```cpp
shared_ptr<int[]> ptr(object);
```

When passing to functions it will be something like:

```cpp
void test_func(std::unique_ptr<Square>& square){
  square->print_hello();
}
```

## shared_ptr

It counts the number of references pointing to a single object. If it reaches zero, it
will release the object from memory. It is useful to deal with a complex program that
is handling the same object in different parts of the program. This pointer will make
sure that the object is released from memory when not used.

```cpp
  auto array = std::make_shared<int[]>(3); // C++14
```

To create more shared pointers:

```cpp
//Initialize with copy constructor. Increments ref count.
auto sp3(sp2);

//Initialize via assignment. Increments ref count.
auto sp4 = sp2;
```

Instead of `auto` you can also use `shared_ptr<type>`. You can print the count
with `use_count()` method.

## weak_ptr

Create it with `std::weak_ptr<auto>`. These do not increment the count. Can be used to
solve circular dependency issues.
