from ._base import Coupler


class CapacitiveCoupler(Coupler):
    '''
        A capactive coupler couples two qubits with interaction Hamiltonian
        .. math ::
        H_I = -g (a_1 - a_1^{\dagger}) (a_2 - a_2^{\dagger})
    '''
    def __init__(self, g: float=1) -> None:
        super().__init__()
        self.g = g
        
    def Hamiltonian_terms(self, *args: tuple) -> tuple:
        res = [(self.g, *args ,'Bd', 'B'),
               (self.g, *args, 'B', 'Bd'),
               (-self.g, *args, 'Bd', 'Bd'),
               (-self.g, *args, 'B', 'B')]
        return res
        
        