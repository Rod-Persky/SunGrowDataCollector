from SunGrowDataCollector.Client.Handlers.RuntimeMessageHandler import RuntimeMessageHandler, RuntimeResponse

import opentelemetry.metrics

class OTelRuntimeMessageHandler(RuntimeMessageHandler):
    def __init__(self):
        
        self._total_energy_gauge = opentelemetry.metrics.get_meter(__name__).create_gauge(
            "TotalEnergy",
            "kilowatthours"
        )
        
        self._today_energy_gauge = opentelemetry.metrics.get_meter(__name__).create_gauge(
            "TodayEnergy",
            "kilowatthours"
        )
        
        self._current_power_gauge = opentelemetry.metrics.get_meter(__name__).create_gauge(
            "CurrentPower",
            "kilowatts"
        )
        
        self._reactive_power_gauge = opentelemetry.metrics.get_meter(__name__).create_gauge(
            "ReactivePower",
            "kilowatts"
        )
        
        
    async def OnMessage(self, message: RuntimeResponse):
        for device_index, device in enumerate(message.devices):
            attributes = {
                "Service": "Runtime",
                "DeviceIndex": device_index,
                "DeviceName": device.dev_name,
                "DeviceModel": device.dev_model,
                "DeviceType": device.dev_type
            }
            
            self._today_energy_gauge.set(device.today_energy, attributes)
            self._total_energy_gauge.set(device.total_energy, attributes)
            self._current_power_gauge.set(device.curr_power, attributes)
            self._reactive_power_gauge.set(device.reactive_power, attributes)

