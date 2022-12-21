FROM arm64v8/python:3.10-slim-buster

RUN mkdir /usr/app/
COPY requirements.txt /usr/app/requirements.txt
COPY pyserver_manual.py /usr/app/pyserver_manual.py
COPY templates /usr/app/templates
RUN pip install -r /usr/app/requirements.txt
RUN chmod +x /usr/app/pyserver_manual.py

EXPOSE 8001
ENTRYPOINT ["python /usr/app/pyserver_auto.py"]