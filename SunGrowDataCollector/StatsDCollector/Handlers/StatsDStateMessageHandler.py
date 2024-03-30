from SunGrowDataCollector.Client.Handlers.StateMessageHandler import StateMessageHandler, StateResponse
from SunGrowDataCollector.StatsDCollector.StatsDConnection import StatsDConnection

class StatsDStateMessageHandler(StateMessageHandler):
    def __init__(self, statsdConnection: StatsDConnection):
        self._statsdConnection = statsdConnection
        
    async def OnMessage(self, message: StateResponse):
        with self._statsdConnection.Client().pipeline() as pipe:
            pipe.gauge("SunGrowDataCollector.State.TotalFault", message.total_fault)
            pipe.gauge("SunGrowDataCollector.State.TotalAlarm", message.total_alarm)
            pipe.gauge("SunGrowDataCollector.State.WirelessConnStatus", message.wireless_conn_sts)
            pipe.gauge("SunGrowDataCollector.State.WifiConnStatus", message.wifi_conn_sts)
            pipe.gauge("SunGrowDataCollector.State.EthernetConnStatus", message.eth_conn_sts)
            pipe.gauge("SunGrowDataCollector.State.Ethernet2ConnStatus", message.eth2_conn_sts)
            pipe.gauge("SunGrowDataCollector.State.WirelessCommand", message.wireless_cmd)
            pipe.gauge("SunGrowDataCollector.State.WifiCommand", message.wifi_cmd)
            pipe.gauge("SunGrowDataCollector.State.CloudConnStatus", message.cloud_conn_sts)
            pipe.gauge("SunGrowDataCollector.State.ServerNetType", message.server_net_type)
