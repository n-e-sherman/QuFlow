from ._base import Qubit


class Transmon(Qubit):
    ''' 
        A transmon is an AHO with Hamiltonian given by
        .. math ::
        H = \omega a^{\dagger} a + \frac{\alpha}{2} a^{\dagger} a^{\dagger} a a
    '''
    def __init__(self, frequency: float=1, anharmonicity: float=-0.1) -> None:
        self.frequency=frequency
        self.anharmonicity=anharmonicity
        super().__init__()
        
        
    def Hamiltonian_terms(self, *args: tuple) -> tuple:
        
        res = [(self.frequency - 0.5*self.anharmonicity, *args, 'N'),
               (0.5*self.anharmonicity, *args, 'NN')]
        return res
