from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

import opentelemetry.metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
import opentelemetry.sdk.resources

class OTelProvider:
    def __init__(self):
        self.Init()
        
    def Init(self):
        readers = [
            PeriodicExportingMetricReader(
                OTLPMetricExporter(),
                export_interval_millis=10000
            )
        ]
        
        resource = opentelemetry.sdk.resources.Resource(
                attributes = {
                    opentelemetry.sdk.resources.SERVICE_NAME: "SunGrowDataCollector"
                }
            )

        
        meter_provider = MeterProvider(
            resource=resource,
            metric_readers=readers,
            shutdown_on_exit=False,
        )
        
        opentelemetry.metrics.set_meter_provider(meter_provider)
