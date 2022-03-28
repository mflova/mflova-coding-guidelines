# Basics

For good coding practices, SOLID design principles should apply:

 - (S)ingle responsability: Class with a single responsability.
 - (O)pen closed principle: Code should be open to extension but closed for
   modifications.
 - (L)iskov substitution principle: When expected a base class, assigning any subclass
   should be working.
 - (I)nterface seggeregation: Many different interfaces prefered over a single one.
   Each interface can be responsible for a single feature. Then, with inheritance, a
   class can inherit from more than one interface.
 - (D)ependency inversion: Make the code depend on abstractions instead of concrete
   classes.

Do not mistaken dependency inversion with dependency injection. Dependency injection
consists of isolating the creation of an object and its use. When you create a class B
inside A, this makes it harder to test and debug. As any change in B will also change A.
This pattern usually requires to create the instance of B outside of A, and pass it as
input parameter to A to the function that actually uses or needs it. It allows to create
simpler functions to test that do not depend on this class.


## Gamma categorization

This categorization divides the design patterns into:

 - Creational patterns: To build complex objects.
 - Structural patterns: Concerned with the structure. Many of them are wrapppres that
   mimic the underlying class interface.
 - Behavioral patterns: No central theme, they are all different.
