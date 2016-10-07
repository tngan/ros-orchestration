# ros-orchestration

A state controller orchestrating ROS nodes

### Design Principles

**Stateless action nodes**

Action node is for executing action. One action node is responsible for single action. The overall state control should be delegated to a centralize controller node, and trigger the action node to be executed. It's not recommended to change the state in action nodes. Otherwise, it's not feasible and clear to coordinate the overall mission.

**Easy configurable**

State machine can be generalized with single .yml file.

**Universal**

This controller should be compatible for every standard ROS nodes. It can be applied on every robots using ROS.

### Suites

Suite is the order of how it plays the orchestration. The documentation will be released very soon, in the meantime, we have put a proof-of-concept `poc.yml` under the folder `suites/`.

### ROS node integration

Integrate the current ROS nodes is easy, for minimal setup, developers just need to add one kickstart service in ROS node, and call the `/step_over` service and change to the next state once the action is finished.
