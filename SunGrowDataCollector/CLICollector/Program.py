from SunGrowDataCollector.CLICollector.RootConfiguration import RootConfiguration
from SunGrowDataCollector.Core.HostedService import HostedService
from SunGrowDataCollector.Client.Handlers.MessageRouter import MessageRouter
from SunGrowDataCollector.Client.Handlers.RuntimeMessageHandler import RuntimeMessageHandler
from SunGrowDataCollector.Client.Handlers.StateMessageHandler import StateMessageHandler
from SunGrowDataCollector.Client.Handlers.StatisticsMessageHandler import StatisticsMessageHandler
from SunGrowDataCollector.Client.Services.DataRequestorService import DataRequestorService
from SunGrowDataCollector.Client.Services.ManagedConnection import ManagedConnection
from SunGrowDataCollector.Client.Services.MessageRoutingService import MessageRoutingService
from SunGrowDataCollector.Client.Configuration import Configuration


class Program(HostedService):
    def __init__(self, config : RootConfiguration):
        self._connection = ManagedConnection(config.ConnectionConfig)

        # Message Handlers
        self._statisticsMessageHandler = StatisticsMessageHandler()
        self._stateMessageHandler = StateMessageHandler()
        self._runtimeMessageHandler = RuntimeMessageHandler()
        self._messageRouter = MessageRouter([self._statisticsMessageHandler, self._stateMessageHandler, self._runtimeMessageHandler])

        # Message Processors
        self._messageRoutingService = MessageRoutingService(self._connection, self._messageRouter)
        self._dataRequestorService = DataRequestorService(self._connection, config.ConnectionConfig)


    async def Start(self):
        await self._connection.Start()
        await self._messageRoutingService.Start()
        await self._dataRequestorService.Start()

    async def Stop(self):
        await self._connection.Stop()
        await self._messageRoutingService.Stop()
        await self._dataRequestorService.Stop()