# Plugins

## pyfakefs

Originally created by google. It mocks all the python-based built-in modules (such as
`os` or `shutil`) to mock a new filesystem. Just after the installation, the  `fs`
fixture becomes available for its use. The fixture can mainly be used with:

- `create_file`: Create a new fake file. You can simulate its content. Recursive.
- `add_real_file`: Add a real file from your system into the fake one.
- `create_dir`: Create a fake directory. Recursive.
