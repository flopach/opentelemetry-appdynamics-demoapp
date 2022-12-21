FROM arm64v8/python:3.10-slim-buster

RUN mkdir /usr/app/
COPY requirements.txt /usr/app/requirements.txt
COPY client.py /usr/app/client.py
RUN pip install -r /usr/app/requirements.txt
RUN chmod +x /usr/app/client.py

ENTRYPOINT ["python /usr/app/client.py"]