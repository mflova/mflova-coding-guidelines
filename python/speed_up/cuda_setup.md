# cuda

In order to use `numba` or `cupy`, you need to have set up `cuda`. Which is the interface
that comunicates with the GPU. Typical requirements are:

- NVIDIA CUDA GPU with the Compute Capability 3.0 or larger$$.
- CUDA Toolkit: v10.2 / v11.0 / v11.1 / v11.2 / v11.3 / v11.4 / v11.5 / v11.6 / v11.7 /
  v11.8 / v12.0 / v12.1. This requirement is optional if you install CuPy
  from conda-forge. However, you still need to have a compatible driver installed for
  your GPU. See Installing CuPy from Conda-Forge for details.
- Python: v3.8 / v3.9 / v3.10 / v3.11

When installing the cuda toolkit, a few things will be installed:
- A CUDA-capable GPU
- A supported version of the OS
- (Only windows, optional) A supported version of Microsoft Visual Studio
- The NVIDIA CUDA Toolkit (available at https://developer.nvidia.com/cuda-downloads)

During the installation, a few components are asked to be installed (Nsight
profilers/debugers, cuda itself...). If you did not install Microsoft Visual Studio,
make sure that you uncheck all boxes related to it (or to MVS). It will work the
same for `numba` and `cupy`, as this is only related to IDEs. However, the
installation wizard will raise a warning.