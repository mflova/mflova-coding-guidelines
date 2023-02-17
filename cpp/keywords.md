# Keywords

## virtual

Without using the keyword, C++ by default uses early-binding. If used, late-binding.
Differences are:

- early binding: Quicker. The method to be used (either from superclass or subclass)
  is decided at compilation time.
- late bindng: Slower. The method to be used (either from superclass or subclass) is
  decided at runtime.

Side note: Binding refers to the process of converting identifiers (such as variable
and performance names) into addresses

As an example, if you have the following code:

```cpp
void func(Animal *xyz) { xyz->eat(); }
```

Early binding will allow call the `eat` method from the superclass (`Animal`) even if
you pass a subclass object (`Cat`) with its overridden method `eat`. However, late
binding will call the `eat` method from the subclass, as it can be known which class is
passed in runtime.

NOTE: There is a scenario that can cause memory leak. This happens when both base class
and derived class implemented a non-virtual destructor. Due to this, early binding
might cause that the destructor called is the one from base class and not from the
derived class. Due to this it is important to define the destructor of the base class
as virtual (this will cause all the destructors of the derived class to be virtual, as
the property is "propagated"). This is needed wherever the base class implements ANY
virtual function.

## override

This keyword is used to tell the compiler that the member function is indeed overriding
a function from its base clase and it is not a mistake where I am just shadowing. When
using this keyword, `virtual` becomes redundant so it can be removed. This is also
because `virtual`-ness is propagated. Which means that if the base class has the method
`virtual`, the derived classes will be virtual even if the keyword is not used.

```cpp
// Both are valid. Maybe the first one can be considered redundant
virtual float get_area() override {return 2;}
float get_area() override {return 2;}
```

## final

Prevents the member function to be overridden

```cpp
float get_area() final {return 2;}
```

## static

Depending on the context:

Static Variables in a Function: When a variable is declared as static inside a function,
its value is retained across multiple function calls. This means that the value of a
static variable inside a function is preserved between function calls, unlike regular
local variables which are destroyed and recreated each time the function is called.

Static Variables at File Scope: When a variable is declared as static at file scope
(outside of any function), it has internal linkage and is only accessible within the
same file. This makes the variable effectively private to the file it is declared in.

Static Member Variables in a Class: When a member variable of a class is declared as
static, it is shared across all instances of the class and only one instance of the
variable exists for all objects of the class.

Static Member Functions in a Class: When a member function of a class is declared as
static, it can be called even if no object of the class exists. A static member
function does not have access to this pointer, and can only access other static
members of the class.

## new

It calls the constructors to initialize an object. The difference is that:

- When you do it the "normal" way, the object will be released as soon as this one goes
  out of the scope. While if we use `new`, it requires `delete`.
- It allows creating arrays with a size known only at runtime. Example below:

```cpp
  int *array = new int[size];
  delete [] array;
```

They require `delete` to deallocate memory once it goes out of the scope, so you can
also use unique ptr to avoid this potential memory leak.

```cpp
std::unique_ptr<int[]> array(new int[size]); // Before C++14
auto array = std::make_unique<int[]>(size); // C++14
```

What's the difference with `malloc()` then? Mainly:

- Failure condition: `malloc` returns `NULL`. `new` throws exception.
- Size: For `malloc`, size needs to be calculated manually. In `new` size is calculated
  by the compiler.
- Buffer size: `malloc` allows to change the size of buffer using `realloc()` while `new`
  doesn’t.
- Calling constructors: `new` calls it. `malloc` do not.

## inline

The inline keyword in C++ is used to suggest to the compiler that a function should be
inlined, meaning that the code for the function should be inserted directly into the
code of any calls to the function, rather than being compiled as a separate function
and called using a function call.

Using inline can lead to improved performance, as it eliminates the overhead of a
function call and allows the compiler to optimize the inlined code more effectively.
However, there are also some downsides to using inline, such as increased code size and
reduced readability, so it should be used with caution.

Important note: It is only a suggestion for the compiler.

## Placing qualifiers

As you can see, here we have two different `const`:

```cpp
class Square{
    public:
        const float get_area() const{return this->side*this->side;};
        int side;
};
```

The first one indicates that the returned value cannot be modified. The second one means
that the member variables of the class will not be modified (in this case, `this->side`).
