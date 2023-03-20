# CMake

Look for a good cheat sheet like this one:
https://usercontent.one/wp/cheatsheet.czutro.ch/wp-content/uploads/2020/09/CMake_Cheatsheet.pdf

```cmake
cmake_minimum_required_version(VERSION 2.9)

# Setup projectname
project (HelloProject)

# Compile and link main.cpp and foo.cpp
# First argument is the target. Following the files.
add_executable(Hello src/main.cpp src/foo.cpp)
```

By default, when using `add_executable` will search for the associated header
like `foo.h` that is included in files like `main.cpp` or `foo.cpp`. There will be no
problems if these are in the same foulder. If it is in a different folder, the command
`include_directories()` will add paths to the header search path.

If you need to compile code but without generating an executable, you need to
use `add_library(target STATIC files)`.

NOTE about `STATIC`: STATIC is a library type option in CMake's `add_library` command
that specifies that the library should be built as a static library, meaning that its
object code is combined with the object code of the final executable binary, rather
than being a separate shared object that is loaded dynamically at runtime. In general,
it makes the code more portable, better performance and easier versioning (since there
is no way to match wrong executable with library). However, the size is bigger and it
is harder to maintain, since updating the library requires recompiling all the code,
not only the library.

## Main commands

- `add_executable`
- `add_library`: Adds a library target called with a specific name. This will be
  typically built into `.a` or `.lib` file depending on the system.
- `add_subdirectory`: Add a subdirectory to the build. Useful when including more
  sub-`CMakeLists`.
- `target_link_libraries`: Specify libraries or flags to use when linking a given
  target and/or its dependents
- `find_package`: Include external packages.
- `include_directories`: This function will make the compiler add these directories
  with `-I` flag. This flag contains all directories where the compiler will search for
  libraries. Useful for absolute path includes.

## Complex projects

Some project both contains multiple executables and multiple libraries. For
instance when having both unit tests and programs. It is common to separate
these subprojects into subfolders

Imagine following files:

```cmake
CMakeLists.txt
somelib/CMakeLists.txt
somelib/foo.hpp
somelib/foo.cpp
someexe/main.cpp
```

The corresponding `CMakeLists.txt` would be:

```cmake
# CMakeLists.txt
cmake_minimum_required(VERSION 2.9)
# Setup project name
project(HelloProject)
add_subdirectory(somelib)
add_subdirectory(someexe)

add_executable(Project someexe/main.cpp)

# If we do not add this line, we will get `undefined reference` issues.
target_link_libraries(Project Foo)
```


```cmake
# somelib/CMakeLists.txt
# Compile and link foo.cpp
add_library(Foo STATIC foo.cpp)
```

## Searching for source files

You can also use glob patterns like:

```cmake
# CMakeLsts.txt
cmake_minimum_required (VERSION 2.9)
# Setup project name
project(HelloProject)
file(GLOB sourcefiles
    "src/∗.hpp"
    "src/∗.cpp")
add_executable(Hello ${sourcefiles})
```

## Include external packages

For example, including `OpenCV`:

```cmake
cmake_minimum_required(VERSION 2.8)
project( DisplayImage )

find_package( OpenCV [VERSION] REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} )
add_executable( DisplayImage DisplayImage.cpp )
target_link_libraries( DisplayImage ${OpenCV_LIBS} )
```

In general, a package can be installed with `apt`, `yum`, `homebrew`... However, not
all packages can be included with `find_package`. Usually the author gives instructions
about how to include them in the CMake thing.
