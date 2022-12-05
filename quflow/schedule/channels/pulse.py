from ._base import Channel
from typing import Union, Any
from matplotlib.axes import Axes
from qupy.schedule.instructions import Delay
import numpy as np

class PulseChannel(Channel):
    
    def __init__(
        self, 
        width: Union[int, float]=2, 
        facecolor: str='b', 
        label: str=r'$P$', 
        delaycolor: str='pink', 
        dividercolor: str='gray', 
        *args: tuple, 
        **kwargs: dict
    ) -> None:
        
        self._delaycolor=delaycolor
        self._dividercolor=dividercolor
        super().__init__(width=width, facecolor=facecolor, label=label, *args, **kwargs)
        
    def instruction(self, time: Union[int, float]) -> Any:
        
        if len(self.instruction_boundaries) == 0:
            return 0
        instruction_index = 0
        for i, boundary in enumerate(self.instruction_boundaries):
            if time < boundary:
                break
            instruction_index += 1
        instruction = self.instructions[instruction_index]
        
        return instruction.magnitude(time - instruction.start)
        
    def draw(self, ax: Axes, y_offset: float=0, lw: Union[int, float]=1) -> None:
             
        super().draw(ax, y_offset=y_offset, lw=lw)
        
        # calculate y_max
        times = np.arange(self.max_time+1)
        y_max = np.max([np.max(abs(np.array([float(self.instruction(time)) for time in times]))), 1])
        shift = y_offset + self.width/2
        
        for instruction in self.instructions:
            if isinstance(instruction, Delay):
                ax.plot([instruction.start, instruction.end], [y_offset+self.width/2, y_offset+self.width/2], color=self._delaycolor, zorder=2)
            else:
                times = np.arange(instruction.start, instruction.end)
                times = np.append(times, instruction.end)
                ax.fill_between(times, instruction.magnitude(times-instruction.start) + shift, y2=y_offset+self.width/2, step='post', color=self.facecolor, zorder=1)
            if instruction.start > 0:
                ax.plot([instruction.start, instruction.start], [y_offset, y_offset+self.width], color=self._dividercolor, ls='--')
                
    def _fill_gap(self, index: int, start: Union[int, float], end: Union[int, float]) -> None:
        self.instructions.insert(index, Delay(start=start, end=end))
        
    def _add_last_instruction(self, start: Union[int, float], end: Union[int, float]) -> None:
        self.instructions.append(Delay(start=start, end=end))
    