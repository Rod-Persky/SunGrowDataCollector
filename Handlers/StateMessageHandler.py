import logging
from Messages.BaseMessage import ResponseBase
from Messages.StateMessage import StateResponse
from Core.services import IMessageHandler

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