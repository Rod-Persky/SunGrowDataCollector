import logging
from SunGrowDataCollector.Client.Messages.BaseMessage import ResponseBase
from SunGrowDataCollector.Client.Messages.StateMessage import StateResponse
from SunGrowDataCollector.Client.Handlers.IMessageHandler import IMessageHandler

_LOGGER = logging.getLogger(__name__)


class StateMessageHandler(IMessageHandler[StateResponse]):
    async def OnMessage(self, message: StateResponse):
        print(message._data)
        
    async def HandleMessage(self, message : ResponseBase) -> bool:
        if message.service != "state":
            return False
        
        message = StateResponse(message)
        if message.Validate() == False:
            _LOGGER.error("StatisticsMessageHandler: Invalid message")
            return False

        await self.OnMessage(message)
        
        return True