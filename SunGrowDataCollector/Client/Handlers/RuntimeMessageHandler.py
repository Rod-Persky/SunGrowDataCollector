import logging
from SunGrowDataCollector.Client.Messages.BaseMessage import ResponseBase
from SunGrowDataCollector.Client.Messages.RuntimeMessage import RuntimeResponse
from SunGrowDataCollector.Client.Handlers.IMessageHandler import IMessageHandler

_LOGGER = logging.getLogger(__name__)


class RuntimeMessageHandler(IMessageHandler[RuntimeResponse]):
    
    async def OnMessage(self, message: RuntimeResponse):
        print(message._data)

    async def HandleMessage(self, message : ResponseBase) -> bool:
        if message.service != "runtime":
            return False
        
        message = RuntimeResponse(message)
        if message.Validate() == False:
            _LOGGER.error("StatisticsMessageHandler: Invalid message")
            return False
        
        await self.OnMessage(message)
        
        return True