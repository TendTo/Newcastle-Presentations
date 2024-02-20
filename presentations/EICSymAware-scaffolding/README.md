# EICSymAware scaffolding

<qrcode width="200" />

<!-- New section -->

## Presentation

<div class="cols">

<img src="./img/profile.jpg" width="500px" />

<div>

**Ernesto Casablanca**

- Completed _MSc Computer Science_ @ [University of Catania](https://www.unict.it/)
- Currently _PhD Student_ @ [Newcastle University](https://www.ncl.ac.uk/)
- Extensive experience in [_software development_](https://github.com/TendTo)
- _Full-stack projects_ at [CTMobi](https://www.ctmobi.it/)

</div>

</div>

<!-- New section -->

## Requirements

What characteristics will EICSymAware have?

- Written in python
<!-- .element: class="fragment" -->
- Easy to distribute
<!-- .element: class="fragment" -->
- Independent development
<!-- .element: class="fragment" -->
- Flexible and modular architecture
<!-- .element: class="fragment" -->
- Easily interchangeable components
<!-- .element: class="fragment" -->

<!-- New subsection -->

### Written in python / Easy to distribute

The easiest way to distribute a python package is through [PyPI](https://pypi.org/).

With a properly configured [`pyproject.toml`](https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/) file and [CI/CD](https://about.gitlab.com/topics/ci-cd/) pipeline, the whole process can be automated and triggered by pushing a new tag.

<!-- .element: class="fragment" data-fragment-index="1" -->

Installation just requires `pip`:

<!-- .element: class="fragment" data-fragment-index="2" -->

```bash
pip install eicsymaware
```

<!-- .element: class="fragment" data-fragment-index="2" -->

<!-- New subsection -->

### Independent development

Each module can be developed independently with its own repository and CI/CD pipeline.

There needs to be agreement on a common API and some coding standards should be enforced (e.g. code style, docstrings, etc.).

<!-- .element: class="fragment" -->

Modules should be deployed regularly to allow for integration testing.

<!-- .element: class="fragment" -->

```bash
eicsymAware-mpi # Module from mpi (repository)
└── src
    └── eicsymaware # namespace (no __init__.py)
        └── mpi # package (__init__.py)

eicsymAware-sisw # Module from sisw (repository)
└── src
    └── eicsymaware  # namespace (no __init__.py)
        └── sisw # package (__init__.py)
```

<!-- .element: class="fragment"" -->

<!-- New subsection -->

### Flexible and modular architecture

Each component should be as independent as possible from the others.

```mermaid
%%{ init : { "flowchart" : { "curve" : "basis" }}}%%
flowchart LR
    env_input{{External inputs from environment}}
    agent_input{{External inputs from another agent}}

    subgraph agent_j[Agent j]
        direction TB
        transmitted_output([Received Communication])
    end

    subgraph human[Human agent]
        direction LR
        goal([Goal])
        preferences([User preferences])
    end

    subgraph agent_i[Agent i]
        direction LR
        perceptual_information[Perceptual Information]
        knowledge[Knowledge]
        received_communication[Received Communication]
        chosen_action[Chosen Action]
        physical_state[Physical State of the system]
        communication_human[Communication Interface with Human Agent]
        communication_agent[Communication Interface with Agent j]

        subgraph situational_awareness[Situational Awareness]
            direction LR
            state([State])
            intent([Intent])
            uncertainty([Uncertainty])
            risk([Risk])
        end
    end

    env_input --> perceptual_information
    agent_input --> received_communication

    received_communication --> knowledge
    received_communication --> situational_awareness

    perceptual_information --> knowledge
    perceptual_information --> communication_agent
    perceptual_information --> situational_awareness

    knowledge --> situational_awareness
    knowledge --> communication_agent

    situational_awareness --> communication_agent
    situational_awareness --> chosen_action
    situational_awareness --> communication_human

    chosen_action --> communication_agent
    chosen_action --> communication_human
    chosen_action --> physical_state

    physical_state --> perceptual_information

    communication_human --> human
    communication_agent --> agent_j

classDef yellow stroke:yellow,stroke-width:1px
classDef red stroke:red,stroke-width:1px
classDef green stroke:green,stroke-width:1px
classDef blue stroke:blue,stroke-width:1px

class state,intent,uncertainty,risk,situational_awareness,knowledge red;
class human,communication_human,goal,preferences green;
class agent_j,communication_agent,transmitted_output,agent_input,received_communication blue;
class env_input,perceptual_information,physical_state yellow;
style chosen_action stroke:magenta,stroke-width:1px;
```

<!-- .element: class="fragment" -->

<!-- New subsection -->

### Flexible and modular architecture

Each module will publish its own package.

An API foundation package would help enforce a common interface between components.

<!-- .element: class="fragment" data-fragment-index="2" -->

Everything will come together in a single package, the entrypoint of the project.

<!-- .element: class="fragment" data-fragment-index="3" -->

```mermaid
flowchart TB
    received_communication[Communication]
    perceptual_information[Perceptual]
    physical_state[Physical Sensors]
    knowledge[Knowledge]
    situational_awareness[Situational Awareness]
    chosen_action[Choose Action]

    api[API]
    agent[Agent]


received_communication --> api
perceptual_information --> api
physical_state --> api
knowledge --> api
situational_awareness --> api
chosen_action --> api

agent --> received_communication
agent --> perceptual_information
agent --> physical_state
agent --> knowledge
agent --> situational_awareness
agent --> chosen_action

classDef yellow stroke:yellow,stroke-width:1px
classDef red stroke:red,stroke-width:1px
classDef green stroke:green,stroke-width:1px
classDef blue stroke:blue,stroke-width:1px

class state,intent,uncertainty,risk,situational_awareness,knowledge red;
class human,communication_human,goal,preferences green;
class agent_j,communication_agent,transmitted_output,agent_input,received_communication blue;
class env_input,perceptual_information,physical_state yellow;
style chosen_action stroke:magenta,stroke-width:1px;
style api stroke:green,stroke-width:1px;
style agent stroke:orange,stroke-width:1px;
```

<!-- .element: class="fragment" -->

<!-- New subsection -->

### Easily interchangeable components

The components should be easily interchangeable, as long as they respect the common API.

Only the main package knows all the modules and how they communicate with each other $\implies$ it is possible to replace a each with a compatible one without affecting the others.

<!-- .element: class="fragment" -->

Adapting the [Publisher-Subscriber](https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern) design pattern makes it easier to decouple the components.

<!-- .element: class="fragment" -->

```mermaid
classDiagram
direction LR

class Publisher {
    <<Abstract>>
    -Dictionary[EventId, List[Callback]] callbacks
    +add(EventId event, Callback callback)
    +remove(EventId event, Callback callback)
    +notify(EventId event, Any data)
}

class ConcretePublisher {
    #State state
}

Publisher <|-- ConcretePublisher
```

<!-- .element: class="fragment" -->

<!-- New subsection -->

#### Event based communication

Working with events makes it easier to segregate the implementation of each component from the transmission of data.

<div class="cols">

```mermaid
sequenceDiagram
    participant P as Perception
    participant A as Agent
    participant SA as Situation Awareness
    participant C as Choose Action

    P->>A: event("input", input)
    A->>SA: dispatch("input", input)
    SA->>A: event("new_awareness", awareness)
    A->>C: dispatch("new_awareness", awareness)
    C->>A: event("action", action)
```

<!-- .element: class="fragment" -->

```mermaid
flowchart TB
    A[Agent]
    P[Perception]
    C[Choose Action]
    SA[Situation Awareness]

    P -- 1 event - input --> A
    A -- 2 dispatch - input --> SA
    SA -- 3 event - new_awareness --> A
    A -- 4 dispatch - new_awareness --> C
    C -- 5 event - action --> A

style P stroke:yellow,stroke-width:1px
style SA stroke:red,stroke-width:1px
style C stroke:magenta,stroke-width:1px
style A stroke:green,stroke-width:1px;
```

<!-- .element: class="fragment" -->

</div>

<!-- New section -->

## Example

A simple example to show how the architecture could be built is currently available on [GitLab](https://gitlab.com/testsimaware).

It includes all the package configuration files, as well as ready to use testing, linting and documentation tools.
All is integrated with a CI/CD pipeline.

<qrcode url="https://gitlab.com/testsimaware" width="200">

<!-- New subsection -->

### Group

A group on GitLab is a collection of projects.

<img src="./img/gitlab-group.png" width="1200px" />

<!-- New subsection -->

### Module

Each module is a separate project.

<img src="./img/testsymaware-mpi.png" width="550px" />

<!-- New subsection -->

### Package

Each module publishes its own package using a CI/CD pipeline.

<div class="cols">

<img src="./img/gitlab-pipeline.png" width="100%" />

<img src="./img/gitlab-package.png" width="100%" />

</div>

```bash
pip install testsimaware-mpi --index-url https://gitlab.com/api/v4/projects/52682823/packages/pypi/simple
pip install testsimaware-sisw --index-url https://gitlab.com/api/v4/projects/52755635/packages/pypi/simple
```

<!-- New subsection -->

### Agent

The agent will combine all the modules together and provide the entrypoint to the project.

```python[|1,2|4-18|6,7|8-11|19,20|]
from testsimaware.mpi import Perception
from testsimaware.sisw import SituationAwareness

class Agent:
    def __init__(self):
        self.perception = Perception()
        self.situation_awareness = SituationAwareness()
        self.perception.add("system_status", self.situation_awareness.update)
        self.situation_awareness.add("low_cpu", lambda _: self.stop)
        self.situation_awareness.add("low_memory", lambda _: self.stop)
        self.situation_awareness.add("low_disk", lambda _: self.stop)

    def start(self):
        self.perception.start()

    def stop(self):
        self.perception.stop()

agent = Agent()
agent.start()
```

<!-- New subsection -->

### Agent complete example

For a more complete example, check the [agent.py](./examples/agent.py) file.

<!-- New section -->

## Questions

Any questions or comments?
