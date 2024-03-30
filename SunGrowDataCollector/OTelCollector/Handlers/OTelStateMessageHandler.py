from SunGrowDataCollector.Client.Handlers.StateMessageHandler import StateMessageHandler, StateResponse

import opentelemetry.metrics

class OTelStateMessageHandler(StateMessageHandler):
    def __init__(self):
        
        self._total_fault_gauge = opentelemetry.metrics.get_meter(__name__).create_gauge(
            "TotalFault",
            "count"
        )
        
        self._total_alarm_gauge = opentelemetry.metrics.get_meter(__name__).create_gauge(
            "TotalAlarm",
            "count"
        )
        
        self._wireless_conn_sts_gauge = opentelemetry.metrics.get_meter(__name__).create_gauge(
            "WirelessConnStatus"
        )
        
        self._wifi_conn_sts_gauge = opentelemetry.metrics.get_meter(__name__).create_gauge(
            "WifiConnStatus"
        )
        
        self._eth_conn_sts_gauge = opentelemetry.metrics.get_meter(__name__).create_gauge(
            "EthernetConnStatus"
        )
        
        self._eth2_conn_sts_gauge = opentelemetry.metrics.get_meter(__name__).create_gauge(
            "Ethernet2ConnStatus"
        )
        
        self._wireless_cmd_gauge = opentelemetry.metrics.get_meter(__name__).create_gauge(
            "WirelessCommand"
        )
        
        self._wifi_cmd_gauge = opentelemetry.metrics.get_meter(__name__).create_gauge(
            "WifiCommand"
        )
        
        self._cloud_conn_sts_gauge = opentelemetry.metrics.get_meter(__name__).create_gauge(
            "CloudConnStatus"
        )
        
        self._server_net_type_gauge = opentelemetry.metrics.get_meter(__name__).create_gauge(
            "ServerNetType"
        )
        
    async def OnMessage(self, message: StateResponse):
        attributes = {
            "Service": "State"
        }
        
        self._total_fault_gauge.set(message.total_fault, attributes=attributes)
        self._total_alarm_gauge.set(message.total_alarm, attributes=attributes)
        self._wireless_conn_sts_gauge.set(message.wireless_conn_sts, attributes=attributes)
        self._wifi_conn_sts_gauge.set(message.wifi_conn_sts, attributes=attributes)
        self._eth_conn_sts_gauge.set(message.eth_conn_sts, attributes=attributes)
        self._eth2_conn_sts_gauge.set(message.eth2_conn_sts, attributes=attributes)
        self._wireless_cmd_gauge.set(message.wireless_cmd, attributes=attributes)
        self._wifi_cmd_gauge.set(message.wifi_cmd, attributes=attributes)
        self._cloud_conn_sts_gauge.set(message.cloud_conn_sts, attributes=attributes)
        self._server_net_type_gauge.set(message.server_net_type, attributes=attributes)
