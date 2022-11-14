import os
import requests
from opentelemetry import trace
from opentelemetry.propagate import inject
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
#from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk import resources
import time

# Service name namespace is required for AppD
resource = resources.Resource(attributes={
    resources.SERVICE_NAME: "pyclient",
    resources.SERVICE_NAMESPACE: "astronomyshop",
    resources.TELEMETRY_SDK_LANGUAGE: "python",
    resources.HOST_NAME : "macbook",
    resources.TELEMETRY_SDK_NAME : "opentelemetry"
})

# Sets the global default tracer provider
trace.set_tracer_provider(TracerProvider(resource=resource))

# Set exporter and add it to the tracer provider
otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)
span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

tracer = trace.get_tracer(__name__)

def add_request(n1,n2):
    with tracer.start_as_current_span(
        name="client_request",
        kind=trace.SpanKind.CLIENT,
        attributes={
            SpanAttributes.HTTP_METHOD : "GET",
            SpanAttributes.HTTP_URL : f"http://127.0.0.1:5000/add?n1={n1}&n2={n2}",
            SpanAttributes.HTTP_SCHEME : "http",
            SpanAttributes.HTTP_HOST : "127.0.0.1:5000",
            SpanAttributes.HTTP_TARGET : f"/add?n1={n1}&n2={n2}"
        }):
        headers = {}
        inject(headers)
        requests.get(f"http://127.0.0.1:5000/add?n1={n1}&n2={n2}",headers=headers)

# Request the numbers from the server and make ca. 1k requests

i = 0

while i < 1000:
    i += 1
    i2 = i+1
    add_request(i,i2)
    time.sleep(1)
    print(f"requesting: {i},{i2}")
