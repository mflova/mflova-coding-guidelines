# Lambdas

Content between brackets `[]` defines the capture method. `&` will mean that everything
is captured by reference by default and `=` by value. `()` will indicate the type and
name of variables. Content between `{}` will be the content of the lambda function.

```cpp
auto A;
auto lambda = [=](int x) {
    // use A here
};
```

You can also specify exceptions to capture type default:

```cpp
[&i]            // OK: No default. `i` captured by reference
[&, i]{};       // OK: by-reference capture default, except i is captured by copy
[=, &i]{};      // OK: by-copy capture default, except i is captured by reference
```

**Important note**: Be aware that this default thing is only for accessing variables
outside the scope of lambda. If you see the first code snippet, you will realize that
`[=]` will only indicate that if we use `A` inside the lambda function, this will be
used by value. However, the arguments defined in `()` will work on its own: either
value or reference depending on how you define them.

## Explicit return type

In order to indicate the return type of the lambda function, you can add `-> return_type`
to the expression before `{}`. Example:

```cpp
auto func = []() -> int {return 2;};
```

## Generic lambda expressions (C++14)

It is using `auto` as qualifier for input arguments. Types deducted by compiler.

```cpp
auto multiply = [](auto a, auto b) {
    return a * b;
};

int result1 = multiply(5, 10);  // result1 is 50
double result2 = multiply(3.14, 2.0);  // result2 is 6.28
```


## Templated ones (C++20)

Example:

```cpp
auto glambda = []<class T>(T a) -> T {return a;};
```
