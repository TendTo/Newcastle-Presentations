# SyimAware: Software architecture

<urltoqr width="200" />

<!-- New section -->

## High level goal

The goal is to create a collection python packages an user can easily install on their machine.

The software must allow for different component implementations to be swapped easily.

<!-- .element: class="fragment" -->

<!-- New section -->

## Project structure

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

classDef yellow stroke:#50623A,stroke-width:1px
classDef red stroke:red,stroke-width:1px
classDef green stroke:green,stroke-width:1px
classDef blue stroke:blue,stroke-width:1px
classDef background fill:#00000015

class state,intent,uncertainty,risk,situational_awareness,knowledge red;
class human,communication_human,goal,preferences green;
class agent_j,communication_agent,transmitted_output,agent_input,received_communication blue;
class env_input,perceptual_information,physical_state yellow;
style chosen_action stroke:magenta,stroke-width:1px;

class agent_i,situational_awareness,human,agent_j background;
```

<!-- New section -->

## Package architecture

All packages will be namespaced under the `symaware` namespace.
From the `symaware.base` package, each team will then develop their own implementation of one or more elements of the system.

<div class="r-stack">

```mermaid
---
title: Package architecture from the prospective of the user
---
flowchart RL
    subgraph symawarep["symaware (namepsace)"]
        symaware["symaware.symaware"]
    end

classDef background fill:#00000015
class symawarep background;
```

<!-- .element: class="fragment fade-in-then-out m-unset" -->

```mermaid
---
title: The base package provides an abstract implementation of the system
---
flowchart RL
    subgraph symawarep["symaware (namepsace)"]
        base[symaware.base]
        symaware[symaware.symaware]
    end

    symaware --> base

classDef background fill:#00000015
class symawarep background;
```

<!-- .element: class="fragment fade-in-then-out m-unset" -->

```mermaid
---
title: |
    Each team will build their own implementation of some elements of the system
    for them to be combined together in the public package
---
flowchart RL
    subgraph symawarep["symaware (namepsace)"]
        base[symaware.]
        mpi[symaware.mpi]
        kth[symaware.kth]
        tue[symaware.tue]
        uu[symaware.uu]
        nlr[symaware.nlr]
        sisw[symaware.sisw]
        base[symaware.base]
        symaware[symaware.symaware]
    end

    mpi --> base
    kth --> base
    tue --> base
    uu --> base
    nlr --> base
    sisw --> base
    symaware --> mpi
    symaware --> kth
    symaware --> tue
    symaware --> uu
    symaware --> nlr
    symaware --> sisw

classDef background fill:#00000015
class symawarep background;
```

<!-- .element: class="fragment fade-in-then-out m-unset" -->

</div>

<!-- New section -->

### Software design of `symaware.base`

The main elements of the software have been divided in subpackages in order to enforce a coarse but clear separation of concerns.

<div class="r-stack">

```mermaid
---
title: Assuming transitive dependencies
---
flowchart TB
    user{{User}}
    subgraph base["symaware.base"]
        direction TB
        agent([base.Agent])
        examples[base.examples]
        components[base.components]
        models[base.models]
        data[base.data]
        utils[base.utils]
    end

user --> agent
user --> examples
agent --> components
examples --> components
components --> models
models --> data
models --> utils

classDef background fill:#00000015
classDef yellow stroke:#50623A,stroke-width:1px
classDef red stroke:red,stroke-width:1px
classDef green stroke:green,stroke-width:1px
classDef blue stroke:blue,stroke-width:1px
classDef orange stroke:orange,stroke-width:1px
classDef magenta stroke:magenta,stroke-width:1px

class examples red;
class agent orange;
class components green;
class models blue;
class utils yellow;
class data magenta;
class base background;
```

<!-- .element: class="fragment fade-in-then-out m-unset" -->

```mermaid
---
title: Explicit dependencies
---
flowchart TB
    user{{User}}
    subgraph base["symaware.base"]
        direction TB
        agent([base.Agent])
        examples[base.examples]
        components[base.components]
        models[base.models]
        utils[base.utils]
        data[base.data]
    end

user --> agent
user --> examples
agent --> models
agent --> components
agent --> data
examples --> components
examples --> models
examples --> data
components --> utils
components --> models
components --> data
models --> utils
models --> data

classDef background fill:#00000015
classDef yellow stroke:#50623A,stroke-width:1px
classDef red stroke:red,stroke-width:1px
classDef green stroke:green,stroke-width:1px
classDef blue stroke:blue,stroke-width:1px
classDef orange stroke:orange,stroke-width:1px
classDef magenta stroke:magenta,stroke-width:1px

class examples red;
class agent orange;
class components green;
class models blue;
class utils yellow;
class data magenta;
class base background;
```

<!-- .element: class="fragment fade-in-then-out m-unset" -->

```mermaid
---
title: Explicit dependencies
---
flowchart TB
    user{{User}}
    subgraph base["symaware.base"]
        direction TB
        agent([base.Agent])
        subgraph examples[base.examples]
            direction TB
            example_environment([examples.ExampleEnvironment])
            example_controller([examples.ExampleController])
        end
        subgraph components[base.components]
            direction TB
            controller([components.Controller])
            perception_system([components.PerceptionSystem])
            communication_system([components.CommunicationSystem])
            risk_evaluator([components.RiskEvaluator])
            uncertainty_evaluator([components.UncertaintyEvaluator])
        end
        subgraph models[base.models]
        direction TB
            dynamical_model([models.DynamicModel])
            environment([models.Environment])
        end
        subgraph utils[base.utils]
            direction TB
            logger[utils.log]
        end
        subgraph data[base.data]
            direction TB
            knowledge([data.Knowledge])
            awareness_vector([data.AwarenessVector])
        end
    end

user --> agent
user --> examples
agent --> components
examples --> components
components --> models
models --> data
models --> utils


classDef background fill:#00000015
classDef yellow stroke:#50623A,stroke-width:1px
classDef red stroke:red,stroke-width:1px
classDef green stroke:green,stroke-width:1px
classDef blue stroke:blue,stroke-width:1px
classDef orange stroke:orange,stroke-width:1px
classDef magenta stroke:magenta,stroke-width:1px

class examples red;
class agent orange;
class components green;
class models blue;
class utils yellow;
class data magenta;
class base,examples,components,models,utils,data background;
```

<!-- .element: class="fragment fade-in-then-out m-unset" -->

</div>

<!-- New subsection -->

### Sequence diagram

The following sequence diagram shows the interaction between the different components of the system.

```mermaid
sequenceDiagram
    participant p as Perception System
    participant cs as Communication System
    participant a as Agent
    participant ru as Risk Evaluator<br>Uncertainty Evaluator
    participant c as Controller

p ->> a: Perceptual Information
cs ->> a: Received Communication
note over a: State = Awareness + Knowledge
a ->> ru: Current state
ru ->> a: Risk/Uncertainty
a ->> c: Updated state
c ->> a: Chosen action
a ->> cs: Updated state
```
