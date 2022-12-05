from ._base import Controller
from qusim.schedule.channels import Channel, PulseChannel

class PulseController(Controller):
    '''
        A PulseController is connected to a qubit, and is modelled by
        .. math ::
        H_c(t) = f(t) * (a + a^{\dagger})
    '''
    
    def __init__(self, channel_name: str="pulse", channel_type: Channel=PulseChannel) -> None:
        super().__init__(channel_name=channel_name, channel_type=channel_type)
        
    def Hamiltonian_terms(self, *args: tuple) -> tuple:
        
        res = [(self.strength, *args, 'B'),
               (self.strength, *args, 'Bd')]
        return res
    
    def update_strength(self, strength: float) -> None:
        self.strength = strength