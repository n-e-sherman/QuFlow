from qusim.schedule.channels import Channel

class Controller:
    
    # Corresponding circuit element
    
    def __init__(self, channel_name: str="channel", channel_type=Channel) -> None:
        
        self._channel_name = channel_name
        self._channel_type = channel_type
    
    def build_channel(self) -> Channel:
        return self._channel_type()
    
    @property
    def channel_name(self) -> str:
        return self._channel_name