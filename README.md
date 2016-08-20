# Elevator System

Hello, this is a test project for implementing system for manipulation several elevators in building

First you need to import **ElevatorSystem** from **elevator.py**

```python
from elevator import ElevatorSystem
```

After that you should create system object

```python
system = ElevatorSystem(3, 9)
```

So we create 3 elevators(0, 1, 2) in 10 floor building(0, ... , 9)

__This system start count from 0, so the first floor will have 0 index and 10th floor - 9 index.
Same situation for elevators.
You need to remember this__


When system was created, the default state for all elevators is the first floor.

Now we can push the button, for example, on the 5 floor(4 index) for the second elevator(1 index)

```python
system.pickup(1, 4)
```

And we could see this result

```python
Elevator 1 close door on 0 floor
Elevator 1 move up
Elevator 1 move up
Elevator 1 move up
Elevator 1 move up
Elevator 1 stop at 4 floor
Elevator 1 open door on 4 floor
```

For sure we can check status of elevator.

```python
system.status(1)
```

And see result.

```
(4, 4)
```

Fist number - current elevator floor and the second - target floor

If we push button from 3 floor(2 index).

```python
system.pickup(1, 2)
```

We could see this result.

```python
Elevator 1 close door on 4 floor
Elevator 1 move down
Elevator 1 move down
Elevator 1 stop at 2 floor
Elevator 1 open door on 2 floor
```
