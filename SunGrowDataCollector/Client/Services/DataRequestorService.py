import asyncio
import logging
from SunGrowDataCollector.Core.BackgroundService import BackgroundService
from SunGrowDataCollector.Client.Messages.RuntimeMessage import RuntimeRequest
from SunGrowDataCollector.Client.Messages.StateMessage import StateRequest
from SunGrowDataCollector.Client.Messages.StatisticsMessage import StatisticsRequest
from SunGrowDataCollector.Client.Configuration import Configuration
from SunGrowDataCollector.Client.Services.IManagedConnection import IManagedConnection


_LOGGER = logging.getLogger(__name__)

class DataRequestorService(BackgroundService):
    def __init__(self, managedConnection: IManagedConnection, config: Configuration):
        super().__init__()
        self._connection = managedConnection
        self._config = config
        
    async def Execute(self):
        while self.IsStopRequested() != True:
            
            if self.IsStopRequested() != True:
                _LOGGER.info("Requesting statistics")
                statsRequest = StatisticsRequest(self._config.LANG, self._config.TOKEN)
                await self._connection.SendMessage(statsRequest)
                await asyncio.sleep(1)
            
            if self.IsStopRequested() != True:
                _LOGGER.info("Requesting state")
                stateRequest = StateRequest(self._config.LANG, self._config.TOKEN)
                await self._connection.SendMessage(stateRequest)
                await asyncio.sleep(1)
            
            if self.IsStopRequested() != True:
                _LOGGER.info("Requesting runtime")
                runtimeRequest = RuntimeRequest(self._config.LANG, self._config.TOKEN)
                await self._connection.SendMessage(runtimeRequest)
                await asyncio.sleep(1)
            
            
        _LOGGER.info("Stopping")
        
