from .parameter import ParameterChanger
from typing import Union


T = Union[int, str, float, None]

class Flux(ParameterChanger):
    
    def __init__(
        self, 
        start: T='before_next', 
        end: T='after_next', 
        operation: str='reset', 
        value: T=None, 
        channel_name: str="flux"
    ) -> None:
    
        super().__init__(start=start, end=end, operation=operation, value=value, channel_name=channel_name, parameter="frequency")
            