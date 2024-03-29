from typing import Optional

from SunGrowDataCollector.Messages.BaseMessage import RequestBase, ResponseBase

class StateRequest(RequestBase):
    def __init__(self, lang: str, token: str):
        super().__init__(lang, token)
        self._service = "state"
        pass
    
    def Serialise(self):
        return {
            "lang": self._lang,
            "token": self._token,
            "service": self._service
        }

# {
#  "result_code": 1,
#  "result_msg": "success",
#  "result_data": {
#   "service": "state",
#   "total_fault": "0",
#   "total_alarm": "0",
#   "wireless_conn_sts": "0",
#   "wifi_conn_sts": "1",
#   "eth_conn_sts": "0",
#   "eth2_conn_sts": "0",
#   "wireless_cmd": "170",
#   "wifi_cmd": "170",
#   "cloud_conn_sts": "1",
#   "server_net_type": "1"
#  }
# }

class StateResponse(ResponseBase):
    def __init__(self, base : ResponseBase):
        super().__init__(base._code, base._msg, base._data)
        
    @property
    def service(self):
        return self._data.get("service")
    
    @property
    def total_fault(self):
        return self._data.get("total_fault")
    
    @property
    def total_alarm(self):
        return self._data.get("total_alarm")
    
    @property
    def wireless_conn_sts(self):
        return self._data.get("wireless_conn_sts")
    
    @property
    def wifi_conn_sts(self):
        return self._data.get("wifi_conn_sts")
    
    @property
    def eth_conn_sts(self):
        return self._data.get("eth_conn_sts")
    
    @property
    def eth2_conn_sts(self):
        return self._data.get("eth2_conn_sts")
    
    @property
    def wireless_cmd(self):
        return self._data.get("wireless_cmd")
    
    @property
    def wifi_cmd(self):
        return self._data.get("wifi_cmd")
    
    @property
    def cloud_conn_sts(self):
        return self._data.get("cloud_conn_sts")
    
    @property
    def server_net_type(self):
        return self._data.get("server_net_type")

    def Validate(self):
        return (self.service is not None
                and self.total_fault is not None
                and self.total_alarm is not None
                and self.wireless_conn_sts is not None
                and self.wifi_conn_sts is not None
                and self.eth_conn_sts is not None
                and self.eth2_conn_sts is not None
                and self.wireless_cmd is not None
                and self.wifi_cmd is not None
                and self.cloud_conn_sts is not None
                and self.server_net_type is not None)
    
    @staticmethod
    def Deserialise(response : dict) -> Optional["StateResponse"]:
        container = StateResponse(ResponseBase.Deserialise(response))
        
        if container.Validate() == False:
            return None
        
        return container