from Core.HostedService import HostedService
from Handlers.MessageRouter import MessageRouter
from Handlers.RuntimeMessageHandler import RuntimeMessageHandler
from Handlers.StateMessageHandler import StateMessageHandler
from Handlers.StatisticsMessageHandler import StatisticsMessageHandler
from Services.DataRequestorService import DataRequestorService
from Services.ManagedConnection import ManagedConnection
from Services.MessageRoutingService import MessageRoutingService
from configuration import Configuration


class Program(HostedService):
    def __init__(self, config : Configuration):
        self._connection = ManagedConnection(config)

        # Message Handlers
        self._statisticsMessageHandler = StatisticsMessageHandler()
        self._stateMessageHandler = StateMessageHandler()
        self._runtimeMessageHandler = RuntimeMessageHandler()
        self._messageRouter = MessageRouter([self._statisticsMessageHandler, self._stateMessageHandler, self._runtimeMessageHandler])

        # Message Processors
        self._messageRoutingService = MessageRoutingService(self._connection, self._messageRouter)
        self._dataRequestorService = DataRequestorService(self._connection, config)


    async def Start(self):
        await self._connection.Start()
        await self._messageRoutingService.Start()
        await self._dataRequestorService.Start()

    async def Stop(self):
        await self._connection.Stop()
        await self._messageRoutingService.Stop()
        await self._dataRequestorService.Stop()