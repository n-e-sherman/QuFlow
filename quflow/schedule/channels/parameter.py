from ._base import Channel
from typing import Union, Any
from matplotlib.axes import Axes
import matplotlib.patches as patches
from quflow.schedule.instructions import ParameterChanger

class ParameterChannel(Channel):

    def __init__(
        self, 
        width: float=1., 
        facecolor: str='lime', 
        edgecolor: str='k', 
        label: str='C',
        *args: tuple, 
        **kwargs: dict
    ) -> None:
        
        super().__init__(width=width, facecolor=facecolor, label=label, *args, **kwargs)
        
    def instruction(self, time: Union[int, float]) -> Any:
        
        if len(self.instruction_boundaries) == 0:
            return 0
        instruction_index = -1
        for i, boundary in enumerate(self.instruction_boundaries):
            if time < boundary:
                break
            instruction_index += 1
        instruction = self.instructions[instruction_index]
        return (instruction.operation, instruction.parameter, instruction.value)
        
    def draw(self, ax: Axes, y_offset: float=0, lw: Union[int, float]=1, squeeze: float=0.1, fontsize: int=12) -> None:
        
        super().draw(ax, y_offset=y_offset, lw=lw)
        
        # find locations with active instruction
        for instruction in self.instructions:
            if instruction.operation in ["set", "shift"]:
                rectangle = patches.Rectangle((instruction.start, y_offset+squeeze*self.width), 
                                              instruction.end - instruction.start, 
                                              self.width*(1.-2*squeeze), 
                                              facecolor=self.facecolor, 
                                              edgecolor=self.edgecolor, 
                                              zorder=1000)
                rx, ry = rectangle.get_xy()
                cx = rx + rectangle.get_width()/2.0
                cy = ry + rectangle.get_height()/2.0
                ax.text(cx, cy, instruction.operation, color='black', weight='bold', fontsize=fontsize, ha='center', va='center',zorder=1001)
                ax.add_patch(rectangle)
        
    def _add_last_instruction(self, start, end):
        self.instructions.append(ParameterChanger(start=start, end=end, operation='reset'))