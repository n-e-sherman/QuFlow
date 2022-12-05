class Qubit:
    
    def __init__(self) -> None:
        self._set_initial()
    
    def _set_initial(self) -> None:
        
        initials = {}
        for k,v in self.__dict__.items():
            initials[k+'0'] = v
        self.__dict__.update(initials)