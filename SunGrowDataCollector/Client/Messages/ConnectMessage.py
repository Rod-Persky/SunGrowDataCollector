from typing import Optional

from SunGrowDataCollector.Client.Messages.BaseMessage import RequestBase, ResponseBase


class ConnectRequest(RequestBase):
    _service: str
    
    def __init__(self, lang: str, token: str):
        super().__init__(lang, token)
        self._service = "connect"
        
    def Serialise(self):
        return {
            "lang": self._lang,
            "token": self._token,
            "service": self._service
        }
    
class ConnectResponse(ResponseBase):
    def __init__(self, code: int, msg: str, service: str, token: str, uid: int, tips_disable: int):
        data = {
            "service": service,
            "token": token,
            "uid": uid,
            "tips_disable": tips_disable
        }
        
        super().__init__(code, msg, data)

    def __init__(self, base : ResponseBase):
        super().__init__(base._code, base._msg, base._data)
        
    @property
    def service(self):
        return self._data.get("service")
    
    @property
    def token(self):
        return self._data.get("token")
    
    @property
    def uid(self):
        return self._data.get("uid")
    
    @property
    def tips_disable(self):
        return self._data.get("tips_disable")
    
    def Validate(self):
        return self.service is not None and self.token is not None and self.uid is not None and self.tips_disable is not None
    
    @staticmethod
    def Deserialise(response : dict) -> Optional["ConnectResponse"]:
        container = ConnectResponse(ResponseBase.Deserialise(response))
        
        if container.Validate() == False:
            return None
        
        return container
