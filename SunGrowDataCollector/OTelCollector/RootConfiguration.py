import configparser

from SunGrowDataCollector.Client.Configuration import Configuration

class RootConfiguration(object):
    ConnectionConfig = Configuration()
    
def LoadConfigurationFromIniFile(file : str) -> RootConfiguration:
    configreader = configparser.ConfigParser()
    configreader.read(file)
    
    config = RootConfiguration()
    
    config.ConnectionConfig.SERVER = configreader.get("Connection", "Server")
    config.ConnectionConfig.PORT = configreader.getint("Connection", "Port")
    config.ConnectionConfig.ENDPOINT = configreader.get("Connection", "Endpoint")
    config.ConnectionConfig.LANG = configreader.get("Connection", "Lang")
    config.ConnectionConfig.TOKEN = configreader.get("Connection", "Token")
    
    return config
    
    
    