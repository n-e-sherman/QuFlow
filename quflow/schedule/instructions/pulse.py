from ._base import Instruction
import numpy as np
from scipy.interpolate import interp1d
from typing import Callable, Union, List, Any

Envelope = Union[Callable, List, None]
T = Union[int, str, float, None]

class Pulse(Instruction):
    
    def __init__(
        self, 
        envelope: Envelope=None, 
        time: T=None, 
        frequency: float=0., 
        phase: float=0, 
        start: T=None, 
        end: T=None, 
        channel_name: str="pulse"
    ) -> None:

        self._frequency = frequency
        self._phase = phase
        self._time = time
        time = np.asarray(time)
        if envelope is not None:
            if callable(envelope):
                self._envelope = envelope
            else:
                envelope = np.asarray(envelope)
                if not len(envelope) == len(time):
                    raise ValueError("envelope and time are not the same length.")
                self._envelope = interp1d(time, envelope, kind='cubic')
                self._time = np.max(time)
        super().__init__(start=start, end=end, channel_name = channel_name)

            
    def magnitude(self, t):
        return self._envelope(t) * np.cos(self._frequency * t + self._phase)
        
class Delay(Pulse):
    
    def __init__(self, time: T=0, start: T=None, end: T=None):
        super().__init__(time=time, start=start, end=end)

        
    def magnitude(self, t: Any) -> Any:
        return 0*t