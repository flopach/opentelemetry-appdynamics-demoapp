# opentelemetry-appdynamics-demoapp

work in progress!

Simple app to show the power of opentelemetry + appdynamics.

## Configure Otel Collector

1. Insert API key in the config.

2. Run:

```
docker run -p 4317:4317 \
    -v $(pwd)/otelcollector/otelcollector-config.yaml:/etc/otelcollector-config.yaml \
    otel/opentelemetry-collector:latest \
    --config=/etc/otelcollector-config.yaml
```

## Install + Configure Python App

Install dependencies, run flask app:

```
pip install -r requirements.txt
flask run
```

Open another terminal, run client:

```
python client.py
```

## Optional: Run with Jaeger

1. Disable Otel collector
2. Run jaeger all in one:

```
docker run --name jaeger \
  -e COLLECTOR_OTLP_ENABLED=true \
  -p 16686:16686 \
  -p 4317:4317 \
  -p 4318:4318 \
  jaegertracing/all-in-one:latest
```
