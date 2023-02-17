# Compilation and building

Compilation:

1) Preprocessing: The preprocessor takes the source code and processes any preprocessor
directives, such as `#include` and `#define`, and generates a preprocessed version of the
code. `.i` or `.cpp` extensions.
2) Compiling: The compiler takes the preprocessed code and generates object files,
which contain machine code for each function or class defined in the source code. `.o`
or `.obj` extensions.
3) Assembling: The assembler takes the object files and combines them into a single
object file, which is then passed to the linker. `.o` or `.obj` extensions.
4) Linking: The linker takes the object file and any libraries that are required by the
program, and combines them into a single executable file that can be run on the target
machine. It can be `.exe` for example.

## Make, Cmake and g++

- `make` is a build automation tool that is commonly used to compile software projects
  on Unix-based systems. `make` uses a file called a makefile to specify how the software
  should be built, including dependencies between different components and the commands
  needed to compile each component.

- `CMake` is a cross-platform build system generator that is used to generate
  platform-specific build scripts (such as makefiles) from a single, platform-independent
  `CMakeLists.txt` file. CMake provides a high-level, domain-specific language for
  specifying build instructions, and it can generate build scripts for a wide range of
  build systems, including makefiles, Visual Studio projects, and Xcode projects.

- `g++` is the GNU Compiler Collection's C++ compiler. g++ is used to compile C++
  source code into executable programs or shared libraries. g++ can be used directly
  from the command line, but it is often used in conjunction with build systems like
  make or CMake to compile larger projects.

## Compiling vs building

Compiling refers to the process of translating source code written in a high-level
programming language (such as C++ or Python) into machine code that can be executed
directly by a computer's CPU. During the compilation process, the source code is
transformed into an object file, which contains machine code that is ready to be linked
into an executable program or library.

Build, on the other hand, refers to the process of creating a complete software product
from its constituent parts. This process typically involves several steps,
including: 1) compiling, 2) linking object files into single executable or library, 3)
copying resources (images, data files...) and 4) packaging.

## How to compile or build

Inside the project, you need to create a `/build` directory. Inside, you have to perform
`cmake ..` to build the make system and them `make`.
