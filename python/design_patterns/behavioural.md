# Behavioral

For more details, visit refactor guru website.

## Chain of responsability

Allow components to process information or events in a chain. It lets you pass requests
along a chain of handlers. The idea is to have something similar to a linked list where
each node computes its corresponding part.

```
class Handler (with methods `setNext(h: Handler)` and `handle(request)`)
class BassHandler (for common methods)
class ConcreteHandler (implements `handle(request)`)

Then, on the main code we can concatenate to a single handler a sequence of different
handlers with `setNext`
```

## Command

Encapsulate a request into a separate object. Good for audit, undo or redo.

## Iterator

Provides an interface for accessing elements of an aggregate object. For example, a
tree might implement `getDepthIterator()` and `getBreadthIterator()` which returns
specific classes that will iterate over that collection.

## Mediator

Provides mediation services between two or more objects. As an example, this works like
the control tower in an airport. Objects no longer have to know about the existance of
other objects. Only has to communicate with the mediator. This will implement a new
class `Mediator` usually with a single method `notify(sender)`. Each component will
have a reference to the mediator. Then, another new subclass `ConcreteMediator` will
handle the relationship between all different components with methods like `reactOnA`,
`reactOnB`... Only problem is that mediator can escalate too quickly.

## Memento

Store the representation of a system state, what can be used to undo/redo in a history
of states. You can take snapshots that will rememeber the current state of the object.
Three main classes:

- `Originator`: Can take snapshots of itself
- `Memento`: Class that represents one state from `originator`.
- `Caretaker`: Main handler. It has the history of mementos (snapshots) and can undo or
  move between them.

## Observer

Allows notificaion of changes or events being triggered in a component. It can be
either an instance attribute or property for example. Other classes can
subscribe/unsuscribe to the list that notifies these changes.


## State

Finite state machine modeled into a design pattern. Each state will be defined in a
separate class. Therefore, we would have:

- `Context`: it stores the current state. It also has methods like `changeState(state)`.
- `State` (abstract): Which defines common methods for all `ConcreteStates`. This one
  will have a reference to `context` so that each object of type `ConcreteStates` can
  switch among different states.
- `ConcreteStates` defines the strategy given that specific state

## Strategy

Similar to template. Each strategy is defined by a class that derives from an abstract
class. Then, you can even select the strategy to be selected in
runtime. Main classes:

- `Context`: It holds the current strategy but has a method `setStrategy(strategy)`
  that can be used to change the strategy. It will also have a method that will operate
  based on that strategy.
- `Strategy`: Defines the common method that all concrete ones will have.
- `ConcreteStrategy`: Defines strategy itself

## Template

It defines a skeleton. The Abstract class defines the common "steps" that will be
executed by the class, while the concrete classes will define the specific steps. You
can also define "hooks" that can be optionally overridden by the concrete class.

## Visitor

Allows non-intrusive addition of functionalities. Instead of modifying a class, the
visitor adds the functionality without applying any change to the already existing
class.
