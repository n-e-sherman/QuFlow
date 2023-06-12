from quflow.schedule.instructions import Instruction
from typing import Union, Any
from matplotlib.axes import Axes



class Channel:
    
    def __init__(
        self, 
        width: float=1., 
        facecolor: str='b', 
        edgecolor: str='k', 
        label: str='C'
    ) -> None:
        
        self._width = width
        self._facecolor = facecolor
        self._edgecolor = edgecolor
        self._label = label
        self.instructions = []
        
        
    def instruction(self) -> Any:
        pass
        
    def add_instruction(self, instruction: Instruction) -> None:
        self.instructions.append(instruction)
        
    def compile_instructions(self, max_time: Union[int, float]) -> None:
        
        self._check_times(max_time)
        self._build_instruction_boundaries()
        
    @property
    def width(self) -> Union[int, float]:
        return self._width
    
    @property
    def facecolor(self) -> str:
        return self._facecolor
    
    @property
    def edgecolor(self) -> str:
        return self._edgecolor
    
    @property
    def label(self) -> str:
        return self._label
    
    def draw(self, ax: Axes, y_offset: float=0., lw: float=0.3) -> None:
        
        # horizontal framing
        ax.plot([0, self.max_time], [y_offset           , y_offset           ], color=self.edgecolor, lw=lw)
        ax.plot([0, self.max_time], [y_offset+self.width, y_offset+self.width], color=self.edgecolor, lw=lw)
        
        # vertical framing
        ax.plot([self.max_time, self.max_time], [y_offset, y_offset+self.width], color=self.edgecolor, lw=lw)
        ax.plot([0,0], [y_offset, y_offset+self.width], color=self.edgecolor, lw=lw)
        
        # label the channel
        ax.text(1.005*self.max_time, y_offset+self.width/2, self.label, fontsize=14, ha='left', va='center')
        
    def _check_times(self, max_time: Union[int, float]) -> None:
        
        time = 0
        gaps = []
        for i,instruction in enumerate(self.instructions.copy()):
            start = instruction.start
            end = instruction.end
            if start < 0:
                raise ValueError("Instruction on channel {} started at negative time.".format(instruction.channel_name))
            if start < time:
                raise ValueError("Instructions on channel {} overlap.".format(instruction.channel_name))
            if end < start:
                raise ValueError("Instruction on channel {} has a negative duration.".format(instruction.channel_name))
            if start > time:
                gaps.append((i, time, start))
            time = end
        for i, gap in enumerate(gaps):
            self._fill_gap(i+gap[0], *gap[1:])
            
        if time < max_time:
            self._add_last_instruction(time, max_time)
        self.max_time = max_time
            
    def _build_instruction_boundaries(self) -> None:
        self.instruction_boundaries = []
        for instruction in self.instructions:
            if instruction.start >= 0:
                self.instruction_boundaries.append(instruction.start)
    
    def _fill_gap(self, index: int, start: Union[int, float], end: Union[int, float]) -> None:
        pass
    
    def _add_last_instruction(self, start: Union[int, float], end: Union[int, float]) -> None:
        pass
    
