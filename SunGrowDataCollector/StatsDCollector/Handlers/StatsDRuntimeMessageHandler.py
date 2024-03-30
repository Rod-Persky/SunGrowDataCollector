from SunGrowDataCollector.Client.Handlers.RuntimeMessageHandler import RuntimeMessageHandler, RuntimeResponse
from SunGrowDataCollector.StatsDCollector.StatsDConnection import StatsDConnection


class StatsDRuntimeMessageHandler(RuntimeMessageHandler):
    def __init__(self, statsdConnection: StatsDConnection):
        self._statsdConnection = statsdConnection
        
    async def OnMessage(self, message: RuntimeResponse):
        for device_index, device in enumerate(message.devices):
            with self._statsdConnection.Client().pipeline() as pipe:
                pipe.gauge(f"SunGrowDataCollector.Runtime.Device_{device_index}.TodayEnergy", device.today_energy)
                pipe.gauge(f"SunGrowDataCollector.Runtime.Device_{device_index}.TotalEnergy", device.total_energy)
                pipe.gauge(f"SunGrowDataCollector.Runtime.Device_{device_index}.CurrentPower", device.curr_power)
                pipe.gauge(f"SunGrowDataCollector.Runtime.Device_{device_index}.ReactivePower", device.reactive_power)
                

