from ._base import Instruction
import numpy as np
from scipy.interpolate import interp1d
from typing import Callable, Union, List, Any

T = Union[int, str, float, None]

class ParameterChanger(Instruction):
    
    def __init__(
        self, 
        start: T='before_next', 
        end: T='after_next', 
        operation: str='reset', 
        parameter: T=None, 
        value: T=None, 
        channel_name: str="parameter"
    ) -> None:
        
        self._operation = operation
        self._parameter = parameter
        self._value = value
        super().__init__(start=start, end=end, channel_name=channel_name)
        
    @property
    def operation(self) -> Any:
        return self._operation
    
    @property
    def parameter(self) -> Any:
        return self._parameter

    @property
    def value(self) -> Any:
        return self._value

