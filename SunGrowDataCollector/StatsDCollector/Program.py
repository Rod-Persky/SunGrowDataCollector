from SunGrowDataCollector.Core.HostedService import HostedService
from SunGrowDataCollector.Client.Handlers.MessageRouter import MessageRouter
from SunGrowDataCollector.Client.Services.DataRequestorService import DataRequestorService
from SunGrowDataCollector.Client.Services.ManagedConnection import ManagedConnection
from SunGrowDataCollector.Client.Services.MessageRoutingService import MessageRoutingService

# Our Handlers
from SunGrowDataCollector.StatsDCollector.Handlers.StatsDRuntimeMessageHandler import StatsDRuntimeMessageHandler
from SunGrowDataCollector.StatsDCollector.Handlers.StatsDStateMessageHandler import StatsDStateMessageHandler
from SunGrowDataCollector.StatsDCollector.Handlers.StatsDStatisticsMessageHandler import StatsDStatisticsMessageHandler
from SunGrowDataCollector.StatsDCollector.StatsDConnection import StatsDConnection
from SunGrowDataCollector.StatsDCollector.RootConfiguration import RootConfiguration



class Program(HostedService):
    def __init__(self, config : RootConfiguration):
        self._connection = ManagedConnection(config.ConnectionConfig)
        self._statsdConnection = StatsDConnection(config.StatsDConfig)

        # Message Handlers
        self._statisticsMessageHandler = StatsDStatisticsMessageHandler(self._statsdConnection)
        self._stateMessageHandler = StatsDStateMessageHandler(self._statsdConnection)
        self._runtimeMessageHandler = StatsDRuntimeMessageHandler(self._statsdConnection)
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
        self._statsdConnection.Shutdown()