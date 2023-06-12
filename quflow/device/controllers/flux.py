from .parameter import ParameterController
from quflow.schedule.channels import Channel, FluxChannel
from quflow.device.qubits import Qubit

class FluxController(ParameterController):
        
    def __init__(self, channel_name: str="flux", channel_type: Channel=FluxChannel) -> None:
        super().__init__(channel_name=channel_name, channel_type=channel_type)
        
    def update_qubit(self, qubit: Qubit, instruction: dict) -> None:
        
        # validate code, move it
        parameter = instruction.get('parameter', None)
        if not parameter in ['frequency', None]:
            raise ValueError('IdealFluxController can only change frequency')
        instruction['parameter'] = 'frequency'
        
        super().update_qubit(qubit, instruction)