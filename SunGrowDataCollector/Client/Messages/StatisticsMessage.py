from typing import Generator, Optional

from SunGrowDataCollector.Client.Messages.BaseMessage import FloatConversionHelper, RequestBase, ResponseBase

class StatisticsRequest(RequestBase):
    def __init__(self, lang: str, token: str):
        super().__init__(lang, token)
        self._service = "statistics"
        pass
    
    def Serialise(self):
        return {
            "lang": self._lang,
            "token": self._token,
            "service": self._service
        }

class DeviceStatisticsResponse:
    _data : dict
    
    def __init__(self, data : dict):
        self._data = data
    
    @property
    def today_energy(self) -> Optional[float]:
        return FloatConversionHelper(self._data.get("today_energy"))
    
    @property
    def today_energy_unit(self):
        return self._data.get("today_energy_unit")
    
    @property
    def total_energy(self):
        return FloatConversionHelper(self._data.get("total_energy"))
    
    @property
    def total_energy_unit(self):
        return self._data.get("total_energy_unit")
    
    @property
    def curr_power(self):
        return FloatConversionHelper(self._data.get("curr_power"))
    
    @property
    def curr_power_unit(self):
        return self._data.get("curr_power_unit")
    
    @property
    def curr_reactive(self):
        return FloatConversionHelper(self._data.get("curr_reactive"))
    
    @property
    def curr_reactive_unit(self):
        return self._data.get("curr_reactive_unit")
    
    @property
    def rated_power(self):
        return FloatConversionHelper(self._data.get("rated_power"))
    
    @property
    def rated_power_unit(self):
        return self._data.get("rated_power_unit")
    
    @property
    def rated_reactive(self):
        return FloatConversionHelper(self._data.get("rated_reactive"))
    
    @property
    def rated_reactive_unit(self):
        return self._data.get("rated_reactive_unit")
    
    @property
    def adjust_power_uplimit(self):
        return FloatConversionHelper(self._data.get("adjust_power_uplimit"))
    
    @property
    def adjust_power_uplimit_unit(self):
        return self._data.get("adjust_power_uplimit_unit")
    
    @property
    def adjust_reactive_uplimit(self):
        return FloatConversionHelper(self._data.get("adjust_reactive_uplimit"))
    
    @property
    def adjust_reactive_uplimit_unit(self):
        return self._data.get("adjust_reactive_uplimit_unit")
    
    @property
    def adjust_reactive_lowlimit(self):
        return FloatConversionHelper(self._data.get("adjust_reactive_lowlimit"))
    
    @property
    def adjust_reactive_lowlimit_unit(self):
        return self._data.get("adjust_reactive_lowlimit_unit")
    
    def Validate(self):
        return (self.today_energy is not None
                and self.today_energy_unit is not None
                and self.total_energy is not None 
                and self.total_energy_unit is not None
                and self.curr_power is not None
                and self.curr_power_unit is not None 
                and self.curr_reactive is not None
                and self.curr_reactive_unit is not None
                and self.rated_power is not None
                and self.rated_power_unit is not None 
                and self.rated_reactive is not None 
                and self.rated_reactive_unit is not None 
                and self.adjust_power_uplimit is not None 
                and self.adjust_power_uplimit_unit is not None 
                and self.adjust_reactive_uplimit is not None 
                and self.adjust_reactive_uplimit_unit is not None 
                and self.adjust_reactive_lowlimit is not None 
                and self.adjust_reactive_lowlimit_unit is not None)
        
    @staticmethod
    def Deserialise(data : dict) -> Optional["DeviceStatisticsResponse"]:
        container = DeviceStatisticsResponse(data)
        
        if container.Validate() == False:
            return None
        
        return container



class StatisticsResponse(ResponseBase):
    def __init__(self, base : ResponseBase):
        super().__init__(base._code, base._msg, base._data)
        
    @property
    def service(self):
        return self._data.get("service")
    
    @property
    def devices(self) -> Generator[DeviceStatisticsResponse, None, None]:
        for device in self._data.get("list"):
            container = DeviceStatisticsResponse.Deserialise(device)
            if container is not None:
                yield container
                
    @property
    def count(self):
        return self._data.get("count")
    
    def Validate(self):
        return self.service is not None and self.count is not None
    
    @staticmethod
    def Deserialise(response : dict) -> Optional["StatisticsResponse"]:
        container = StatisticsResponse(ResponseBase.Deserialise(response))
        
        if container.Validate() == False:
            return None
        
        return container