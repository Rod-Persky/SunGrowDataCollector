from SunGrowDataCollector.Client.Handlers.StatisticsMessageHandler import StatisticsMessageHandler, StatisticsResponse
from SunGrowDataCollector.StatsDCollector.StatsDConnection import StatsDConnection

class StatsDStatisticsMessageHandler(StatisticsMessageHandler):
    def __init__(self, statsdConnection: StatsDConnection):
        self._statsdConnection = statsdConnection
        
    async def OnMessage(self, message: StatisticsResponse):
        for device_index, device in enumerate(message.devices):
            with self._statsdConnection.Client().pipeline() as pipe:
                pipe.gauge(
                    f"SunGrowDataCollector.Statistics.Device_{device_index}.TodayEnergy", device.today_energy)
                pipe.gauge(
                    f"SunGrowDataCollector.Statistics.Device_{device_index}.TotalEnergy", device.total_energy)
                pipe.gauge(
                    f"SunGrowDataCollector.Statistics.Device_{device_index}.CurrentPower", device.curr_power)
                pipe.gauge(
                    f"SunGrowDataCollector.Statistics.Device_{device_index}.CurrentReactive", device.curr_reactive)
                pipe.gauge(
                    f"SunGrowDataCollector.Statistics.Device_{device_index}.RatedPower", device.rated_power)
                pipe.gauge(
                    f"SunGrowDataCollector.Statistics.Device_{device_index}.RatedReactive", device.rated_reactive)
                pipe.gauge(
                    f"SunGrowDataCollector.Statistics.Device_{device_index}.AdjustPowerUplimit", device.adjust_power_uplimit)
                pipe.gauge(
                    f"SunGrowDataCollector.Statistics.Device_{device_index}.AdjustReactiveUplimit", device.adjust_reactive_uplimit)
                pipe.gauge(
                    f"SunGrowDataCollector.Statistics.Device_{device_index}.AdjustReactiveLowlimit", device.adjust_reactive_lowlimit)
                
                