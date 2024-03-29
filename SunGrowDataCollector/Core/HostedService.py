from abc import ABC, abstractmethod


class HostedService(ABC):
    @abstractmethod
    async def Start():
        pass
    
    @abstractmethod
    async def Stop():
        pass
