# Optimization

This summarizes the math-based optimizations.

## Optimization types

[TBD]

## Insights

### Differentiation related

Differentiation is important as it is what determines what next steps will be taken during
optimization. Sometimes these can even take more time than the cost evaluation itself.

Before proceeding, it is important to know the differences between `gradient` and `jacobian`:

- `Gradient`: f: R^n -> R
- `Jacobian`: f: R^n -> R^m

Therefore, the gradient can be seen a special sub-case of the Jacobian. Hence, from now
own `Jacobian` term will be used instead of gradient.

Now, here are the three main methods:

- `Finite differences`: Usually, optimization-based packages like `scipy` use finite
  differences for the jacobian computation. These re-evaluate the cost function with small
  changes in the input in order to evaluate the gradient. Due to the election of the small
  step, this method will always have some error. Among the main sub-methods, these usually
  includes 2 modes:

    - `2-point`: Requires n + 1 evaluations (being n the number of input dimensions and 1
      the evaluation at x).
    - `3-point`. These require 2n+1 evaluations. This evaluates at x + h and x-1. Hence
      the 2n term.

  These kind of method scalates poorly with the amount of inputs. Having 1_000 inputs
  means that, for each step, you would need to evaluate the function at least 2_001 times.

- `Symbolic` or `analytic`: The purpose of this approach is to end up with the analytical
  form that allows for the computation of the jacobian. This will be exact precision and
  much quicker than finite differences (usually), as the function you write would allow
  the use of vectorization and it only needs to be evaluated once in order to compute the
  Jacobian. These functions can usually be passed to `scipy.optimize` as the `jac`
  argument.

- `Autodiff`: They internally modify the original cost function to not only compute the
  cost but also the Jacobian. All of this without the user doing anything (that's why it
  is "auto"). Therefore, the cost function would return the cost and the Jacobian. This is
  made by following the basic definitions of derivatives. This method compares in speed to
  the `symbolic` or `analytical` one. It is much quicker than finite differences specially
  for a big amount of input parameters. This is the default method apply for `jax`
  optimizations and it is way it is that quick. There are two main sub-methods:

    - `forward`: They compute the jacobian in the same direction as the inputs. As a
      consequence, this method is super well performant in cases where n >> m (more inputs
      than outputs).
    - `backward`: They compute the jacobian from the output to the input. Because of this,
      this method is super well performant in cases where m >> n (more outputs than
      inputs)