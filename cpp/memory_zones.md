# Memory zones

## Stack

This is a region of memory that stores temporary data, such as function call frames,
local variables, and function arguments. The stack grows and shrinks dynamically as
functions are called and return. Access to stack memory is fast, but its size is limited,
and the stack data is automatically released when the function returns.

## Heap

This is a region of memory that is used to store dynamically allocated objects, such as
those created with the new operator. The heap is large and can grow or shrink as needed,
but access to heap memory is slower than access to stack memory. The lifetime of
objects on the heap must be managed manually by the programmer, as they persist until
they are explicitly deleted or until the program terminates.

## Static

This is a region of memory that stores objects that have static storage duration. These
objects are created before the program starts and persist until the program terminates.
They can be global or local to a function.

## Constants

This is a region of memory that stores read-only data, such as string literals,
constant variables, and compile-time constants. The data in this zone is initialized at
program start and is never modified during program execution.

## Code

This is a region of memory that stores the compiled code of the program. This region is
read-only and executed by the CPU to carry out the program's instructions.
