# rvalue and lvalues

## lvalue 

An lvalue is an expression that refers to a memory location and can appear on the left
side of an assignment operator but also at right. An lvalue must have a memory address
that can be accessed and modified. Examples of lvalues include variables, arrays, and
dereferenced pointers.

## rvalue

On the other hand, an rvalue is an expression that does not refer to a memory location
and can only appear on the right side of an assignment operator. rvalues are often
temporary values that are created during expression evaluation, and they do not have a
memory address that can be accessed or modified. Examples of rvalues include literals,
temporary objects, and the results of arithmetic expressions. Related to "temporary"

## Operators

- lvalue reference: `&` is used. Only lvalues can be passed here. However, if `const`
  qualifier is used, you can also pass an `rvalue`.
- rvalue reference: `&&` is used.

```cpp
#include <iostream>

void foo(int &x) {
  std::cout << "Lvalue reference, x = " << x << std::endl;
}

void foo(int &&x) {
  std::cout << "Rvalue reference, x = " << x << std::endl;
}

int main() {
  int a = 42;
  foo(a); // Calls the lvalue reference version of foo
  foo(84); // Calls the rvalue reference version of foo
  return 0;
}
```

## Move semantics

In C++11 and later, these are used to move `rvalues` into variables instead of being
copied, which means better performance and reduced memory usage. Why? Because `rvalues`
are associated to temporary values. Due to this, we know that the program already
allocated resources when creating it but we know that it is not going to be used later.
Due to this, we can transfer the ownership.
