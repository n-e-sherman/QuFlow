import numpy as np
import matplotlib.patches as patches
from typing import Union, Any

T = Union[int, str, float, None]

class Instruction:
    
    def __init__(
        self, 
        start: T=None, 
        end: T=None, 
        channel_name: str="channel"
    ) -> None:
        
        self._start = start
        self._end = end
        self._channel_name = channel_name
        self.validate()
        
    def validate(self) -> None:
        pass
    
    def set_start(self, start: Any) -> None:
        self._start = start
        
    def set_end(self, end: T) -> None:
        self._end = end
        
    @property
    def start(self) -> Any:
        return self._start
    
    @property
    def end(self) -> Any:
        return self._end
    
    @property
    def channel_name(self) -> Any:
        return self._channel_name
    