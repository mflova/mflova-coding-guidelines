# Standards

Main changes introduced:

## C++98/03:

- Standardization of C++ as an ISO standard.
- Introduction of Standard Template Library (STL).
- Support for namespaces, exceptions, and templates.
- Runtime type information (RTTI) and `dynamic_cast` operator.
- The auto keyword is introduced to deduce the type of an expression at compile-time.
- Smart pointers (`auto_ptr`) are introduced.

## C++11:

- Introduction of move semantics and rvalue references, allowing for more efficient move construction and assignment of objects.
- Support for variadic templates, allowing functions and classes to accept a variable number of arguments of different types.
- Introduction of lambda expressions, making it easier to write short, anonymous functions.
- Support for multithreading with the introduction of the `<thread>` library and other threading features.
- Initialization lists for non-static data members and array initialization.
- Smart pointers are improved with the introduction of `unique_ptr`, `shared_ptr`, and `weak_ptr`.

## C++14:

- Binary literals and digit separators for easier readability of numeric literals.
- Generic lambda expressions, allowing lambda functions to be templated. This is using
 `auto` as qualifiers in input arguments.
- Runtime-sized arrays can be declared in function parameters.

    ```cpp
    // Note how n, size of array, can be defined at runtime.
    void print_array(int n, int arr[n]) {
        for (int i = 0; i < n; i++) {
            std::cout << arr[i] << " ";
        }
        std::cout << std::endl;
    }
    ```
- Return type deduction for normal functions. This is using `auto` as return type to
  let the compilet deduce the returned type.

## C++17:

- Structured bindings to allow multiple return values to be bound to individual
  variables. This is unpacking multiple values returned by a function into two variables.
  Only works with `auto`. Example:

    ```cpp
    #include <tuple>

    std::tuple<int, double> my_function() {
        return std::make_tuple(42, 3.14);
    }

    int main() {
        auto [x, y] = my_function();
        std::cout << x << " " << y << std::endl;  // prints "42 3.14"
        return 0;
    }
    ```

- Inline variables that can be defined in headers without causing linker errors.
- Deduction guides for class templates. This is some kind of guide that indicates that,
  for a given parameter type, what will be the resolved type for the template. Example:

    ```cpp
    template<typename T>
    class my_container {
    public:
        my_container(T t) : data(t) {}
    private:
        T data;
    };

    // Here you indicate that if the input is an int, the deducted template type is `double`
    my_container(int) -> my_container<double>;  // deduction guide

    int main() {
        my_container c(42);  // deduces T to be double
        return 0;
    }

    ```

- Filesystem library for portable file and directory handling. This is `std::filesystem`.
  High level library to work with the file system: including creating, copying, moving,
  and deleting files and directories, as well as iterating over directory contents.

- New algorithms and types added to STL. Like:
  - `any`: Handles multiple types.
  - `optional`: Handles null values

  ```cpp
    std::optional<int> x = my_function();
    if (x) {
        std::cout << *x << std::endl;  // prints "42"
    }
  ```

  - `variant`: To store multiple a value that can have multiple types. You use `std::get`
    to obtain its value:

  ```cpp
    int main() {
        std::variant<int, double, std::string> v = "hello";
        std::cout << std::get<std::string>(v) << std::endl;  // prints "hello"

        v = 3.14;
        std::cout << std::get<double>(v) << std::endl;  // prints "3.14"
        return 0;
    }

  ```

- `constexpr` is an `if` condition but instead of checked at runtime, it is done at
  compilation time. Useful when comparing `const` variables or anything else that can
  be checked at compile time.

    ```cpp
      const int val = 2;
      if constexpr (val==2)  // is number
                  std::cout << "YES" << std::endl;
    ```

## C++20:

- Concepts, which provide a new way to express and check template constraints. A
  concept is a named set of requirements that a type must satisfy in order to be used
  as a template argument. As an example, you can say that the type must have a given
  operator or you can restrict to certain types like below:

  ```
    #include <concepts>
    #include <string>
    #include <iostream>

    template <typename T>
    concept IsIntOrString = std::same_as<T, int> || std::same_as<T, std::string>;

    void foo(IsIntOrString auto arg) {
      std::cout << arg << '\n';
    }

    int main() {
      int x = 42;
      std::string hello = "Hello, world!";
      foo(x);     // OK
      foo(hello); // OK
      foo(3.14);  // error: no matching function for call to 'foo(double)'
    }
  ```
- Modules, which allow for more efficient and safer organization of code than header
  files. They allow developers to write code that can be compiled separately and linked
  together, reducing build times and making it easier to manage large projects. Modules
  also provide better name hiding and more fine-grained control over the visibility of code.
  ```cpp
    // my_module.cpp
    module my_module;

    export void my_function() {
        // ...
    }

    // A new `my_module` is defined. The export keyword is used to make `my_function`
    // available to other modules. Then you can import it with `export my_module`.
  ```
- Ranges library, which provide a more modern and composable way to work with sequences of elements.
- The spaceship operator, `<=>`, for easy definition of comparison operations.
- The format library, which provides a type-safe and extensible way to format strings.

    ```cpp
    auto s = std::format("My name is {} and I'm {} years old.", name, age);
    // Before (with array)
    char buffer[100];
    int value = 42;
    std::sprintf(buffer, "The value is %d", value);
    // Before (with std::string)
    std::string name = "Alice";
    std::string message = "Hello, " + name + "!";
    ```

- Coroutines, which enable lightweight concurrency and cooperative multitasking. Enable
  lightweight concurrency and cooperative multitasking
