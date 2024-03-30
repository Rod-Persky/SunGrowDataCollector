import logging
from SunGrowDataCollector.Core.BackgroundService import BackgroundService
from SunGrowDataCollector.Client.Services.ManagedConnection import ManagedConnection
from SunGrowDataCollector.Client.Handlers.IMessageRouter import IMessageRouter


import asyncio

_LOGGER = logging.getLogger(__name__)


class MessageRoutingService(BackgroundService):
    """
    Service responsible for routing messages received from a connection using a message router.
    """

    def __init__(self, connection: ManagedConnection, messageRouter: IMessageRouter):
        super().__init__()
        self._connection = connection
        self._messageRouter = messageRouter

    async def Execute(self):
        """
        Executes the message routing service.

        This method continuously waits for messages from the connection and routes them using the message router.
        """
        while self.IsStopRequested() != True:
            _LOGGER.info("MessageRoutingService: Waiting for messages")
            async for message in self._connection.GetMessages():
                if self.IsStopRequested() == True:
                    break
                
                await self._messageRouter.RouteMessage(message)

            if self.IsStopRequested() == False:
                await asyncio.sleep(1)
            
        _LOGGER.info("Stopping MessageRoutingService")