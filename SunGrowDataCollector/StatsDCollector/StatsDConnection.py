import statsd
from SunGrowDataCollector.StatsDCollector.StatsDConfiguration import StatsDConfiguration

class StatsDConnection:
    def __init__(self, config : StatsDConfiguration):
        self._config = config
        self.Init()
        
    def Client(self) -> statsd.StatsClient:
        return self._client
    
    def Init(self):
        self._client = statsd.StatsClient(self._config.Host, self._config.Port, self._config.Prefix)
    
    def Shutdown(self):
        self._client.close()