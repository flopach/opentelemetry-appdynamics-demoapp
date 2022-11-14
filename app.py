from flask import Flask, request
import os
import requests
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
#from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.wsgi import collect_request_attributes
from opentelemetry.propagate import extract
from opentelemetry.sdk import resources

# Service name namespace is required for AppD
resource = resources.Resource(attributes={
    resources.SERVICE_NAME: "pyserver",
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

app = Flask(__name__)

@app.route("/add")
def add():
    """
    Sum of the 2 requested number and a random weather request
    """
    n1 = int(request.args.get('n1'))
    n2 = int(request.args.get('n2'))
    with tracer.start_as_current_span(
        name="server_request",
        context=extract(request.headers),
        kind=trace.SpanKind.SERVER,
        attributes=collect_request_attributes(request.environ)
        ):

        sum = n1 + n2

        current_span = trace.get_current_span()
        current_span.set_attribute("result", str(sum))

        # random API request for testing
        with tracer.start_as_current_span(
        name="weather_request",
        kind=trace.SpanKind.CLIENT,
        attributes={
            SpanAttributes.HTTP_METHOD : "GET",
            SpanAttributes.HTTP_URL : "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m",
            SpanAttributes.HTTP_SCHEME : "https",
            SpanAttributes.HTTP_HOST : "api.open-meteo.com",
            SpanAttributes.HTTP_TARGET : "/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m"
        }):
            requests.get("https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m")
            return str(sum)
