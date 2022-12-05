import networkx as nx
from typing import Any, Tuple, Optional
from pandas.core.dtypes.common import is_list_like

class Device:
    """
    a Device is a wrapper to a networkx Graph class
    The graph requires the following:
        - nodes must have a node attribute "qubit" that is of type Qubit
        - edges must have an edge attribute "coupler" that is of type Coupler
    The graph can additionally have the following optional properties
        - nodes can include "control" attributes of type "Control"
    """
    
    def __init__(
        self, 
        topology: nx.Graph
    ) -> None:
        
        self.topology = topology
        self._set_attributes()

    def _set_attributes(self) -> None:

        attributes = {}
        for node in self.topology.nodes.data():
            key, attribute = node
            control = attribute.get("control", None)
            if not is_list_like(control):
                attributes[key] = {"control": [control]}
        nx.set_node_attributes(self.topology, attributes)
        
    def draw(self, *args: tuple, **kwargs: dict) -> None:
        nx.draw(self.topology, *args, **kwargs)