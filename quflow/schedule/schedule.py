from quflow.device import Device
from quflow.schedule.instructions import Instruction, Flux, ParameterChanger, Pulse
from typing import Any, Hashable, Union
from quflow.schedule.channels import PulseChannel
import numpy as np
import matplotlib.pyplot as plt




class Schedule:
    
    _compiled = False
    def __init__(self, device: Device, timestep: float=1.) -> None:
        
        self._dt = timestep
        self.device = device
        self._set_channels()
        
    def add_instruction(self, node: Hashable, instruction: Instruction, channel_name: Union[str, None]=None) -> None:
        
        qubit = self.qubits.get(node, None)
        if qubit is None:
            raise ValueError("trying to implement instruction on qubit {} that is not on the device".format(node))
        
        qubit["instructions"].append(instruction)
        channels = qubit.get("channels", None)
        channel = channels.get(channel_name, channels.get(instruction.channel_name, None))
        if channel is None:
            raise ValueError("There is no channel that permits this instruction.")
        
        channel.add_instruction(instruction)
        self._compiled = False
        
    def add_pulse(self, node: Hashable, instruction: Pulse) -> None:
        
        if not isinstance(instruction, Pulse):
            raise ValueError("tried adding an instruction of type {} to a pulse channel".format(type(instruction)))
        channel_name = "pulse"
        self.add_instruction(node, instruction, channel_name=channel_name)
        
    def add_flux(self, node: Hashable, instruction: Flux) -> None:
        
        if not isinstance(instruction, Flux):
            raise ValueError("tried adding an instruction of type {} to a flux channel".format(type(instruction)))
        channel_name = "flux"
        self.add_instruction(node, instruction, channel_name=channel_name)
        
    def add_parameter_changer(self, node: Hashable, instruction: ParameterChanger) -> None:
        
        if not isinstance(instruction, ParameterChanger):
            raise ValueError("tried adding an instruction of type {} to a parameter channel".format(type(instruction)))
        channel_name = "parameter"
        self.add_instruction(node, instruction, channel_name=channel_name)
    
    def compile_schedule(self) -> None:
        
        if self._compiled:
            return
        self._set_instruction_times()
        
        # get max_time
        max_time = 0
        self.active_qubits = {}
        for key, qubit in self.qubits.items():
            channels = qubit["channels"]
            for channel_name, channel in channels.items():
                if len(channel.instructions) > 0:
                    self.active_qubits[key] = {"channels": {}}
                    max_time = np.max([max_time, channel.instructions[-1].end])
                    
        for key, qubit in self.qubits.items():
            channels = qubit["channels"]
            for channel_name, channel in channels.items():
                if len(channel.instructions) > 0:
                    self.active_qubits[key]["channels"][channel_name] = channel
                channel.compile_instructions(max_time)
                
        self.max_time = max_time     
        self._compiled = True
        
    def draw(self, channel_space: float=0.2) -> None:
        
        self.compile_schedule()
        
        # could only do qubits with instructions later.
        qubits = self.active_qubits
        fig, axes = plt.subplots(len(qubits),1, squeeze=False, subplot_kw={'ymargin': 0.05})
        axs = axes.ravel()
        fig.tight_layout()
        fig.set_size_inches(12.5,1.75*len(qubits))
        if len(axs) > 1:
            for ax in axs[:-1]:
                ax.axis('off')
        axs[-1].grid(False)
        axs[-1].spines['left'].set_visible(False)
        axs[-1].spines['top'].set_visible(False)
        axs[-1].spines['right'].set_visible(False)
        axs[-1].tick_params(left=False, labelleft=False)
        axs[-1].set_xlabel(r'$t$')
            
        for index, key in enumerate(qubits):
            qubit = qubits[key]
            ax = axs[index]
            y_offset = 0
            channels = qubit["channels"]
            
            # draw pulse channels
            for channel_name, channel in channels.items():
                if isinstance(channel, PulseChannel):
                    channel.draw(ax, y_offset)
                    y_offset += (channel.width+channel_space)
            
            # draw other channels
            for channel_name, channel in channels.items():
                if not isinstance(channel, PulseChannel):
                    channel.draw(ax, y_offset)
                    y_offset += (channel.width+channel_space)
                    
            # label the qubit
            ax.annotate(r'$q_{}$'.format(str(key)), 
                        (-0.01*self.max_time, y_offset/2), 
                        fontsize=22, ha='right', va='center')
        
        
        # draw line divider between channels
        r = fig.canvas.get_renderer()
        bboxes = []
        for ax in axs:
            bboxes.append(np.array(ax.get_position(r)).ravel()) 
        for i in range(len(bboxes)-1):
            top = bboxes[i]
            bottom = bboxes[i+1]
            y_mid = np.mean([top[1], bottom[-1]])
            dy = top[1] - bottom[-1]
            left = top[0]
            right = top[-2]
            line = plt.Line2D((left, right),(y_mid, y_mid), color="k", linewidth=3)
            fig.add_artist(line)
        
        # adjust bottom spine
        axs[-1].spines['bottom'].set_bounds((0, self.max_time))
        if len(bboxes) > 1:
            axs[-1].spines['bottom'].set_position(('axes', -2*dy))
                
    def _set_channels(self) -> None:
        
        from qupy.device.controllers import PulseController
         
        self.qubits = {}
        for node in self.device.topology.nodes.data():
            key, attributes = node
            self.qubits[key] = {}
            self.qubits[key]["channels"] = {}
            self.qubits[key]["instructions"] = []
            for control in attributes["control"]:
                if isinstance(control, PulseController):
                    self.qubits[key]["channels"][control.channel_name] = control.build_channel()
            for control in attributes["control"]:
                if not isinstance(control, PulseController):
                    self.qubits[key]["channels"][control.channel_name] = control.build_channel()
            
        
    def _set_instruction_times(self):
        
        # Set start and end
        pass
    
    