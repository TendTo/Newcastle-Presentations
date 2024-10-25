# ROS in SymAware

<!-- New section -->

## ROS

The Robot Operating System (ROS) is a set of software libraries and tools that help you build robot applications.

At its core, you can see it as a middleware that takes care of the communication between different components (called nodes).

<!-- .element: class="fragment" -->

Its success is due to the fact that it is open-source, modular, and has a large community providing support and packages.

<!-- .element: class="fragment" -->

<!-- New subsection -->

### Example of a ROS system

```mermaid
architecture-beta

    service node1(server)[ROS node 1]
    service node2(server)[ROS node 2]
    service node3(server)[ROS node 3]
    service node4(server)[ROS node 4]
    service network(internet)[Network]

    node1:R -- L:network
    node2:B -- T:network
    node3:L -- R:network
    node4:T -- B:network
```

<!-- New subsection -->

### Topics

Nodes communicate with each other by publishing messages to topics.

```mermaid
graph LR

    subgraph Node 1
        p[Publisher]
    end

    subgraph Node 2
        s[Subscriber]
    end

    p -- message --> s
```

<!-- New subsection -->

### Multiple topics

Each node can publish to multiple topics and subscribe to multiple topics.

<a target="_blank" href="https://fr.mathworks.com/help/examples/ros/win64/ExchangeDataWithROSPublishersAndSubscribersExample_01.png
">
    <img src="https://fr.mathworks.com/help/examples/ros/win64/ExchangeDataWithROSPublishersAndSubscribersExample_01.png" width="100%" />
</a>


<!-- New section -->

## Integrating SymAware

SymAware is a framework which can interact with multiple simulators and provides a common interface to write components that determine the behaviour of agents in the environment.

<!-- New subsection -->

### SymAware and Prescan

SymAware already supports the Prescan simulator, which is a powerful tool for simulating autonomous vehicles.

<a target="_blank" href="https://www.docker.com">
    <img src="./img/prescan.jpg" width="50%" />
</a>

<!-- New subsection -->

### ROS nodes

```mermaid
flowchart TB

r{{Network}}

subgraph lA[Robot]
    direction LR
    n1[VEC ROS node]
    n2[Controller ROS node]
end

subgraph lB[Prescan machine]
    n3[Simulator ROS node]
end

style lA stroke:#f00
style lB stroke:#0f0
classDef ros stroke:orange,stroke-dasharray:5

class n1,n2,n3 ros

    r <-- topics --> n1
    r <-- topics --> n2
    r <-- topics --> n3
```

<!-- New subsection -->

#### Pros and cons

| Pros                           | Cons                                                 |
| ------------------------------ | ---------------------------------------------------- |
| Direct efficient communication | Requires ROS to be installed on the Prescan machine  |
| More standard ROS approach     | SymAware goes from a Python package to a ROS package |

<!-- New subsection -->

### On Robot ROS bridge

```mermaid
flowchart TB

r{{Network}}

subgraph lA[Robot]
    direction LR
    n1[VEC ROS node]
    n2[Controller ROS node]
    n3[Bridge ROS node]
end

subgraph lB[Prescan machine]
    n4[Simulator API]
end

style lA stroke:#f00
style lB stroke:#0f0
classDef ros stroke:orange,stroke-dasharray:5
classDef api stroke:cyan,stroke-dasharray:5

class n1,n2,n3 ros
class n4 api

    n3 <-- topics --> n1
    n3 <-- topics --> n2
    r <-- json --> n3
    r <-- json --> n4
```

<!-- New subsection -->

#### Pros and cons

| Pros                                               | Cons                                   |
| -------------------------------------------------- | -------------------------------------- |
| No need to install ROS on the Prescan machine      | Slower middleware communication        |
| SymAware only needs to implement the communication | Higher computational load on the Robot |

<!-- New subsection -->

### On middleware ROS bridge

```mermaid
flowchart TB

r{{Network}}

subgraph lA[Robot]
    direction LR
    n1[VEC ROS node]
    n2[Controller ROS node]
end

subgraph lB[Middle machine]
    n3[Bridge ROS node]
end

subgraph lC[Prescan machine]
    n4[Simulator API]
end



style lA stroke:#f00
style lC stroke:#0f0
style lB stroke:#00f
classDef ros stroke:orange,stroke-dasharray:5
classDef api stroke:cyan,stroke-dasharray:5

class n1,n2,n3 ros
class n4 api

    r <-- topics --> n1
    r <-- topics --> n2
    n3 <-- topics --> r
    r <-- json --> n3
    r <-- json --> n4
```

<!-- New subsection -->

#### Pros and cons

| Pros                                               | Cons                                 |
| -------------------------------------------------- | ------------------------------------ |
| No need to install ROS on the Prescan machine      | Even slower middleware communication |
| SymAware only needs to implement the communication | Needs another ROS machine            |

<!-- New subsection -->

### Light ROS node

```mermaid
flowchart TB

r{{Network}}

subgraph lA[Robot]
    direction LR
    n1[VEC ROS node]
    n2[Controller ROS node]
end

subgraph lB[Prescan machine]
    n3[Simulator ROS node]
end

style lA stroke:#f00
style lB stroke:#0f0
classDef ros stroke:orange,stroke-dasharray:5
classDef api stroke:pink,stroke-dasharray:5

class n1,n2 ros
class n3 api

    r <-- topics --> n1
    r <-- topics --> n2
    r <-- topics --> n3
```

<!-- New subsection -->

#### Pros and cons

| Pros                                          | Cons                |
| --------------------------------------------- | ------------------- |
| No need to install ROS on the Prescan machine | May not be possible |
| Direct efficient communication                |                     |
