from abc import abstractmethod
import asyncio
import logging
from Core.HostedService import HostedService

_LOGGER = logging.getLogger(__name__)

class BackgroundService(HostedService):
    def __init__(self):
        super().__init__()
        self._task = None
        self._stop_requested = False
        
    def IsStopRequested(self):
        return self._stop_requested
    
    @abstractmethod
    async def Execute(self):
        pass
    
    async def Start(self):
        _LOGGER.info("Starting service")
        self._task = asyncio.create_task(self.Execute())

    async def Stop(self):
        if self._task == None:
            return
        
        _LOGGER.info("Stopping service")
        
        try:
            self._stop_requested = True
            await self._task
        except asyncio.CancelledError:
            self._task = None
            self._task.cancel()
            
        _LOGGER.info("Service stopped")
            