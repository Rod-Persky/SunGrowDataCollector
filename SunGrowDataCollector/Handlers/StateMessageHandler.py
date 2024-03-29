import logging
from SunGrowDataCollector.Messages.BaseMessage import ResponseBase
from SunGrowDataCollector.Messages.StateMessage import StateResponse
from SunGrowDataCollector.Core.services import IMessageHandler

_LOGGER = logging.getLogger(__name__)


class StateMessageHandler(IMessageHandler):
    async def HandleMessage(self, message : ResponseBase) -> bool:
        if message.service != "state":
            return False
        
        message = StateResponse(message)
        if message.Validate() == False:
            _LOGGER.error("StatisticsMessageHandler: Invalid message")
            return False

        print(message._data)
        
        return True