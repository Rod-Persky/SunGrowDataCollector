from abc import ABC, abstractmethod
from typing import Generator, Generic, Optional, TypeVar



class ResponseBase:
    _code : int
    _msg : str
    _data: dict
    
    def __init__(self, code: int, msg: str, data: dict):
        self._code = code
        self._msg = msg
        self._data = data
        
    @property
    def code(self):
        return self._code
    
    @property
    def message(self):
        return self._msg
    
    @property
    def service(self) -> Optional[str]:
        return self._data.get("service")
    
    @staticmethod
    def Deserialise(response: dict) -> Optional["ResponseBase"]:
        code = response.get("result_code")
        msg = response.get("result_msg")
        data = response.get("result_data")
        
        if code is None or msg is None or data is None:
            return None
        
        return ResponseBase(code, msg, data)

class RequestBase(ABC):
    _lang : str
    _token : str
    
    def __init__(self, lang: str, token: str):
        self._lang = lang
        self._token = token
        
    @abstractmethod
    def Serialise(self) -> dict:
        pass



    




    
