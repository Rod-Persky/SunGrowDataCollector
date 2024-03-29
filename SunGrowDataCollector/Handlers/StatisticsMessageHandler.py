import logging
from SunGrowDataCollector.Messages.BaseMessage import ResponseBase
from SunGrowDataCollector.Messages.StatisticsMessage import StatisticsResponse
from SunGrowDataCollector.Core.services import IMessageHandler

_LOGGER = logging.getLogger(__name__)


class StatisticsMessageHandler(IMessageHandler):
    """
    Handles statistics messages.

    This class implements the IMessageHandler interface and provides the functionality to handle statistics messages.
    """

    def __init__(self):
        pass

    async def HandleMessage(self, message : ResponseBase) -> bool:
        """
        Handles the given message.

        This method is responsible for handling the given message. It checks if the message is a statistics message,
        creates a StatisticsResponse object from the message, and prints the data of the response.

        Parameters:
            message (ResponseBase): The message to be handled.

        Returns:
            bool: True if the message was handled successfully, False otherwise.
        """
        if message.service != "statistics":
            return False
        
        message = StatisticsResponse(message)
        if message.Validate() == False:
            _LOGGER.error("StatisticsMessageHandler: Invalid message")
            return False
        
        print(message._data)
        
        return True