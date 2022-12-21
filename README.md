# opentelemetry-appdynamics-demoapp

This a sample weather app provides more insight into leveraging Open Telemetry (Otel).

Components:

* Flask Server - Otel auto instrumented
* Flask Server - Otel manual insutrumented
* Client - Requesting data from the servers above
* Jaeger
* Otel Collector

## Configuration

1. Clone this repository.

2. Insert your AppDynamics configuration (API keys, account, host, port) in the file ´otel-collector-config.yaml´

3. Change the Docker base layers to x86/ARM plaform

4. Run: `docker-compose up`

## Use:

* Flask Server auto: [](http://localhost:8000)
* Flask Server manual: [](http://localhost:8001)
* Jaeger Interface: [](http://localhost:16686)

