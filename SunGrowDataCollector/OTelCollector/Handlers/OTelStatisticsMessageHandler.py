from SunGrowDataCollector.Client.Handlers.StatisticsMessageHandler import StatisticsMessageHandler, StatisticsResponse
from SunGrowDataCollector.OTelCollector import OTelProvider

import opentelemetry.metrics

class OTelStatisticsMessageHandler(StatisticsMessageHandler):
    def __init__(self):
        
        self._today_energy_gauge = opentelemetry.metrics.get_meter(__name__).create_gauge(
            "TodayEnergy",
            "kilowatthours"
        )
        
        self._total_energy_gauge = opentelemetry.metrics.get_meter(__name__).create_gauge(
            "TotalEnergy",
            "kilowatthours"
        )
        
        self._current_power_gauge = opentelemetry.metrics.get_meter(__name__).create_gauge(
            "CurrentPower",
            "kilowatts"
        )
        
        self._current_reactive_gauge = opentelemetry.metrics.get_meter(__name__).create_gauge(
            "CurrentReactive",
            "kilowatts"
        )
        
        self._rated_power_gauge = opentelemetry.metrics.get_meter(__name__).create_gauge(
            "RatedPower",
            "kilowatts"
        )
        
        self._rated_reactive_gauge = opentelemetry.metrics.get_meter(__name__).create_gauge(
            "RatedReactive",
            "kilowatts"
        )
        
        self._adjust_power_uplimit_gauge = opentelemetry.metrics.get_meter(__name__).create_gauge(
            "AdjustPowerUplimit",
            "kilowatts"
        )
        
        self._adjust_reactive_uplimit_gauge = opentelemetry.metrics.get_meter(__name__).create_gauge(
            "AdjustReactiveUplimit",
            "kilowatts"
        )
        
        self._adjust_reactive_lowlimit_gauge = opentelemetry.metrics.get_meter(__name__).create_gauge(
            "AdjustReactiveLowlimit",
            "kilowatts"
        )
        
        
    async def OnMessage(self, message: StatisticsResponse):
        for device_index, device in enumerate(message.devices):
            attributes = {
                "Service": "Statistics",
                "DeviceIndex": device_index
            }
            
            self._today_energy_gauge.set(device.today_energy, attributes)
            self._total_energy_gauge.set(device.total_energy, attributes)
            self._current_power_gauge.set(device.curr_power, attributes)
            self._current_reactive_gauge.set(device.curr_reactive, attributes)
            self._rated_power_gauge.set(device.rated_power, attributes)
            self._rated_reactive_gauge.set(device.rated_reactive, attributes)
            self._adjust_power_uplimit_gauge.set(device.adjust_power_uplimit, attributes)
            self._adjust_reactive_uplimit_gauge.set(device.adjust_reactive_uplimit, attributes)
            self._adjust_reactive_lowlimit_gauge.set(device.adjust_reactive_lowlimit, attributes)
            