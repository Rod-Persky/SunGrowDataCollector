import logging
from SunGrowDataCollector.Messages.BaseMessage import ResponseBase
from SunGrowDataCollector.Messages.RuntimeMessage import RuntimeResponse
from SunGrowDataCollector.Core.services import IMessageHandler

_LOGGER = logging.getLogger(__name__)


class RuntimeMessageHandler(IMessageHandler):

    async def HandleMessage(self, message : ResponseBase) -> bool:
        if message.service != "runtime":
            return False
        
        message = RuntimeResponse(message)
        if message.Validate() == False:
            _LOGGER.error("StatisticsMessageHandler: Invalid message")
            return False
        
        print(message._data)
        
        return True