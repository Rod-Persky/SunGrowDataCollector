from typing import Generator, Optional

from SunGrowDataCollector.Messages.BaseMessage import RequestBase, ResponseBase

class RuntimeRequest(RequestBase):
    def __init__(self, lang: str, token: str):
        super().__init__(lang, token)
        self._service = "runtime"
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
#   "service": "runtime",
#   "count": 1,
#   "list": [{
#     "dev_name": "SG8.0RT(COM1-001)",
#     "dev_model": "SG8.0RT",
#     "dev_type": 21,
#     "dev_procotol": 2,
#     "today_energy": "10.4",
#     "today_energy_unit": "kWh",
#     "total_energy": "4341.0",
#     "total_energy_unit": "kWh",
#     "dev_state": "0",
#     "dev_state_unit": "",
#     "curr_power": "1.10",
#     "curr_power_unit": "kW",
#     "reactive_power": "-0.00",
#     "reactive_power_unit": "kvar"
#    }],
#   "connect_count": 1,
#   "off_count": 0
#  }
# }

class DeviceRuntimeResponse:
    _data : dict
    
    def __init__(self, data : dict):
        self._data = data
    
    @property
    def dev_name(self):
        return self._data.get("dev_name")
    
    @property
    def dev_model(self):
        return self._data.get("dev_model")
    
    @property
    def dev_type(self):
        return self._data.get("dev_type")
    
    @property
    def dev_procotol(self):
        return self._data.get("dev_procotol")
    
    @property
    def today_energy(self):
        return self._data.get("today_energy")
    
    @property
    def today_energy_unit(self):
        return self._data.get("today_energy_unit")
    
    @property
    def total_energy(self):
        return self._data.get("total_energy")
    
    @property
    def total_energy_unit(self):
        return self._data.get("total_energy_unit")
    
    @property
    def dev_state(self):
        return self._data.get("dev_state")
    
    @property
    def dev_state_unit(self):
        return self._data.get("dev_state_unit")
    
    @property
    def curr_power(self):
        return self._data.get("curr_power")
    
    @property
    def curr_power_unit(self):
        return self._data.get("curr_power_unit")
    
    @property
    def reactive_power(self):
        return self._data.get("reactive_power")
    
    @property
    def reactive_power_unit(self):
        return self._data.get("reactive_power_unit")
    
    def Validate(self):
        return (self.dev_name is not None  
                and self.dev_model is not None  
                and self.dev_type is not None  
                and self.dev_procotol is not None  
                and self.today_energy is not None  
                and self.today_energy_unit is not None  
                and self.total_energy is not None  
                and self.total_energy_unit is not None  
                and self.dev_state is not None  
                and self.dev_state_unit is not None  
                and self.curr_power is not None  
                and self.curr_power_unit is not None  
                and self.reactive_power is not None  
                and self.reactive_power_unit is not None)
    
    @staticmethod
    def Deserialise(data : dict) -> Optional["DeviceRuntimeResponse"]:
        container = DeviceRuntimeResponse(data)
        
        if container.Validate() == False:
            return None
        
        return container



class RuntimeResponse(ResponseBase):
    def __init__(self, base : ResponseBase):
        super().__init__(base._code, base._msg, base._data)
        
    @property
    def service(self):
        return self._data.get("service")
    
    @property
    def devices(self) -> Generator[DeviceRuntimeResponse, None, None]:
        for device in self._data.get("list"):
            container = DeviceRuntimeResponse.Deserialise(device)
            if container is not None:
                yield container
                
    @property
    def count(self):
        return self._data.get("count")
    
    def Validate(self):
        return self.service is not None and self.count is not None
    
    @staticmethod
    def Deserialise(response : dict) -> Optional["RuntimeResponse"]:
        container = RuntimeResponse(ResponseBase.Deserialise(response))
        
        if container.Validate() == False:
            return None
        
        return container
    