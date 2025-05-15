# Optimization

This summarizes the math-based optimizations.

## Categories

I like splitting the types following this criteria:

- First order methods: These are the ones that use the information about the Jacobian
  (first derivative) in order to optimize a given cost function. Technically, the
  direction given by the gradient is not the most optimal one. Therefore, this methods,
  although quicker, they lack stability or robustness. Among these, you can find:

    - Gradient descent: Use the gradient descent with a constant learning rate ("step").
    - Stochastic gradient descent: In order to save computational resources, this one only
      uses a few terms from all the available ones in a Jacobian. Although it might look
      worse, it tends to have a better convergence since this technique introduces
      "noise". However, it might require more iterations.
    - Momentum gradient descent: This one uses information on the past step to update the
      current step. If you visualize this algorithm, it would look as a ball that has
      certain inertia.

- Second order merthods: These are the ones that use second order derivatives (Hessian) on
  top of the first one in order to be more efficient in terms on convergence and
  stability. The second derivative gives information about the curavture, what allows to
  choose a better direction and learning rate (in combination with the first derivative).
  For example, this would allow to choose a dynamic learning rate that would be higher for
  flat regions and lower for steep zones. As a consequence, these methods are
  computationally more expensive than the previous ones. However, you have to be aware
  that the Hessian can be tricky for not well behaved problems. Here there are typically 2
  main groups:

    - Newton-based: These would blindly trust the Hessian, which can be either
      approaximate or fully calculated depending on the method. Here we can find methods
      like:

        - Newton Rapshon: Calculates an exact hessian (either autodiff or analytical). It
          is slow and it can be problematic when the Hessian is not well behaved.

    - Hessian approximators: These ones compute an approximation of the Hessian.
        
        - Quasi-Newton based: They approximate the Hessian similar to finite differences
          (i.e by observing how the gradient changes). Inside this category we would have
          BFGS or L-BFGS. The first one computes and approximation of the inverse of the
          Hessian. The second one is Large-Memory wich optimizes better for the RAM usage
          (ideal for high dimensionality problems). These might require more iterations
          but it is more robust than GN (the next method).
        - Gauss-Newton: This one approximates the Hessian by using the Jacobian (Jt x J).
          Quicker than the previous one but it is considered less robust, especially if
          residuals are not small or if the problem is not very lineal.

    - Trust-region: While the previous methods blindly rely on the Hessian (either exact
      calculation or approximation), these ones defines a trust-region. These define a
      maximum distance to walk each step based on the accuracy of the Hessian. No matter
      if the Hessian is calculated or approximated, these are valid for a local region.
      The further away you move, the least accurate they would be. The idea of the trust
      region is to take into account this problem. They are the slowest ones but, at the
      same time, the most robust ones. `least_squares` from `scipy` uses this one by
      default.

    - Misc: These ones are typically a combination of the previous ones that do not fit
      into the previous definitions:

      - Levenberg-Marquadt: This one uses a combination between gradient descent and
        Gaussian-Newton ones for the learning step. This algorithm calculates a metric
        that indicate the quality of the Hessian approximation made by the Gaussian-Newton
        method. If the confidence is low, this parameter would give much more strength to
        the gradient descent technique (and hence using a constant learning rate). This
        way the algorithm takes the best from each method: goes quicker when the
        approximation is good and decelarates when not.

## Well behaved problems

Well behaved problems are easier to approximate and give less problems. One condition that
is usually looked at is that the Hessian must be positive defined. Methods that need this
(and therefore, the ones that are less stable):

- Classic Newton
- Gauss-Newton
- Levenberg-Marquadt: This one only in its traditional form (Gaussian-Newton). When the
  confidence rate is low, it would switch to the gradient descent, being again more
  stable.

On the other side, methods that do not require it as those that, in the above section,
were considered more stable: Quasi-Newton ones and trust-region methods. These are the main problems they address:

  - Non-convex: 
      - Functions that are non-convex can have multiple local minima and inflection
        points. This makes it easy for optimization algorithms to get stuck in a local
        minimum instead of finding the global one.
      - Trust region helps by limiting the step size to a "trustable" region where the
        model behaves well. This prevents the algorithm from taking large steps into areas
        where the model is no longer valid, avoiding getting trapped in poor local minima.

  - Numerically unstable: 
      - Functions that are numerically unstable may be prone to precision issues,
        especially when calculating derivatives, inverses, or using finite differences.
        Small errors in computation can lead to large errors in optimization, resulting in
        poor performance or failure.
      - Trust region mitigates this by adjusting the size of the step based on how
        well the model predicts the function's behavior. If the model is inaccurate due to
        numerical issues, the region is reduced, ensuring that the optimization doesn't
        take risky steps that could be further destabilized by numerical errors.


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

More source:
  - https://wandb.ai/wandb_fc/tips/reports/Enhancing-Performance-with-SciPy-Optimize-and-W-B-A-Deep-Dive--Vmlldzo0NjE4MDEy