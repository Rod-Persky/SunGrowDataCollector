import logging
from typing import List
from SunGrowDataCollector.Messages.BaseMessage import ResponseBase
from SunGrowDataCollector.Core.services import IMessageHandler, IMessageRouter

_LOGGER = logging.getLogger(__name__)

class MessageRouter(IMessageRouter):
    """Router for messages coming from the websocket

    Args:
        IMessageRouter (_type_): List of all message handlers
    """
    def __init__(self, handlers : List[IMessageHandler]):
        self._handlers = handlers
        self._connection = False
            
    async def RouteMessage(self, message : ResponseBase):
        for handler in self._handlers:
            messageWasHandled = await handler.HandleMessage(message)
            if messageWasHandled == True:
                return
        
        _LOGGER.error("MessageRouter: No handler found for message")
        
            
        