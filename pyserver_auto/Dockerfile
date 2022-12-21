FROM arm64v8/python:3.10-slim-buster

RUN mkdir /usr/app/
COPY requirements.txt /usr/app/requirements.txt
COPY pyserver_auto.py /usr/app/pyserver_auto.py
COPY templates /usr/app/templates
RUN pip install -r /usr/app/requirements.txt
RUN chmod +x /usr/app/pyserver_auto.py

EXPOSE 8000
ENTRYPOINT ["opentelemetry-instrument flask --app /usr/app/pyserver_auto.py run"]