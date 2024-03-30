from SunGrowDataCollector.Core.HostedService import HostedService
from SunGrowDataCollector.Client.Handlers.MessageRouter import MessageRouter
from SunGrowDataCollector.Client.Services.DataRequestorService import DataRequestorService
from SunGrowDataCollector.Client.Services.ManagedConnection import ManagedConnection
from SunGrowDataCollector.Client.Services.MessageRoutingService import MessageRoutingService

# Our Handlers
from SunGrowDataCollector.OTelCollector.Handlers.OTelRuntimeMessageHandler import OTelRuntimeMessageHandler
from SunGrowDataCollector.OTelCollector.Handlers.OTelStateMessageHandler import OTelStateMessageHandler
from SunGrowDataCollector.OTelCollector.Handlers.OTelStatisticsMessageHandler import OTelStatisticsMessageHandler
from SunGrowDataCollector.OTelCollector.OTelProvider import OTelProvider
from SunGrowDataCollector.OTelCollector.RootConfiguration import RootConfiguration


class Program(HostedService):
    def __init__(self, config : RootConfiguration):
        self._connection = ManagedConnection(config.ConnectionConfig)
        self._otelProvider = OTelProvider()

        # Message Handlers
        self._statisticsMessageHandler = OTelStatisticsMessageHandler()
        self._stateMessageHandler = OTelStateMessageHandler()
        self._runtimeMessageHandler = OTelRuntimeMessageHandler()
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