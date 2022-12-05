from ._base import Controller
from qusim.schedule.channels import Channel, ParameterChannel
from qusim.device.qubits import Qubit

class ParameterController(Controller):
    
    def __init__(self, channel_name: str="parameter", channel_type: Channel=ParameterChannel) -> None:
        super().__init__(channel_name=channel_name, channel_type=channel_type)
        
    def update_qubit(self, qubit: Qubit , instruction: dict) -> None:
        
        operation = instruction.get('operation', None)
        parameter = instruction.get('parameter', None)
        value = instruction.get('value', None)
        
        # validate code, move it
        if not parameter in qubit.__dict__:
            raise ValueError('Trying to change parameter {}, which does not exist'.format(parameter))
        
        # perform operation
        if operation == 'shift':
            qubit.__dict__[parameter] += value
        elif operation == 'set':
            qubit.__dict__[parameter] = value
        elif operation == 'reset':
            qubit.__dict__[parameter] = qubit.__dict__[parameter+'0']
        else:
            raise ValueError('operation {} is not implemented'.format(operation))