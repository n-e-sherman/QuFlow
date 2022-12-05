from .parameter import ParameterChannel
from qupy.schedule.instructions import Flux

class FluxChannel(ParameterChannel):
    
    def __init__(
        self, 
        width: float=1., 
        facecolor: str='aquamarine', 
        label: str=r"$\phi$",
        *args: tuple, 
        **kwargs: dict
    ) -> None:
    
        super().__init__(width=width, facecolor=facecolor, label=label, *args, **kwargs)
        
    def _add_last_instruction(self, start, end):
        self.instructions.append(Flux(start=start, end=end, operation='reset'))