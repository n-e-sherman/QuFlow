# QuFlow

&#10021;&#10021; This project is still in development &#10021;&#10021;

Package for the simulation of quantum processors.
There are three major modules in this code base: Device, Schedule, Simulator.

### Device: 
This module defines a physical device configuration to run simulations.
This includes classes for defining a Device: Qubit, Coupler, Controller.
Device also takes in a networkx graph to define the arrangement of qubits as nodes, and the qubits that are connected via edges.
###### Qubit:
This defines the qubit Hamiltonian, and includes necessary parameters, such as coupling constants, and optionally T1 / T2 values.
###### Coupler:
This defines the two-qubit Hamiltonian for the qubits that are connected to each other. 
###### Controller:
This defines the time-dependent terms in the Hamiltonian that are used to control the qubits. Controllers also require a "channel_name", and "channel_type", which are used in the Schedule module.



### Schedule: 
This module enables implementing pulse sequences to perform quantum computations at the pulse level. There is also the ability to change parameters of the device for a specified time. This can be thought of as an ideal flux insertion for example.
There is a "compile_schedule" method that will take all specified Instructions, and create a full schedule.
Lastly, there is a "draw" method which will compile the schedule if not compiled, and then create a visual of the circuit.
Schedules require a Device as input to function properly
This module includes classes for defining a Schedule: Channel, Instruction.
###### Channel:
This is used to implement controls on specific qubits, and to define a sequence of instruction on a particular control in the device.
This includes adding "Instructions" for a specified duration, such as a pulse shape, with start time and end time.
This class also includes drawing a channel for seeing a full schedule of instructions.
###### Instruction:
This class is used to add specific instructions on the Schedule. This includes a specific pulse, on a specified Channel corresponding to a Control on the Device, or a change of the Device parameters for a specified time. All Instructions must have a start time and final time. (Working on infering start and end times if not specified).



### Simulator:
This module will take a Schedule (which includes a Device), and then define a Hamiltonian (or Lindbladian) to perform time evolution. The schedule will discretize time for us, and then we treat the Schedule as piecewise constant for each time step, enabling straightforward time evolution.

**This module is currently not implemented.**



