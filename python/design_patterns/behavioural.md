# Behavioral

## Chain of responsability

Allow components to process information or events in a chain. It lets you pass requests
along a chain of handlers.

## Command

Encapsulate a request into a separate object. Good for audit, undo or redo.

## Iterator

Provides an interface for accessing elements of an aggregate object.

## Mediator

Provides mediation services between two or more objects. As an example, this worls like
the control tower in an airport. Objects no longer have to know about the existance of
other objects. Only has to communicate with the mediator.

## Memento

Store the representation of a system state, what can be used to undo/redo in a history
of states. You can take snapshots that will rememeber the current state of the object.

## Observer

Allows notificaion of changes or events being triggered in a component. It can be
either a instance attribute or property for example. Other classes can
subscribe/unsuscribe to the list that notifies these changes.


## State

Finite state machine modeled into a design pattern.

## Strategy

Similar to template. Each strategy is defined by a class that derives from an abstract
class. Then, you can even select the strategy to be selected in
runtime.

## Template

It defines a skeleton. The Abstract class defines the common "steps" that will be
executed by the class, while the concrete classes will define the specific steps. You
can also define "hooks" that can be optionally overridden by the concrete class.

## Visitor

Allows non-intrusive addition of functionalities. Instead of modifying a class, the
visitor adds the functionality without applying any change to the already existing
class.
