# Testing strategies

## Property based testing

It is about testing properties that you certainly now that they are going to happen
after executing my function to be tested. These can be:

- The length of a list
- Non empty fields in a dictionary
- Applying the function and then the anti-function should return the same (for example a function that adds 1 and returns 1)
- Specific math properties (for example if some conditions are given, a matrix multiplication will always be one)

This type of testing allows the use of randomized and massive testing to find bugs. Of
course it will also be necessary to do the traditional testing to check specific corner
cases.
