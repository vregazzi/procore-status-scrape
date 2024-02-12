FROM python:3.11-alpine

WORKDIR /usr/app/src

COPY procore/* ./procore/
COPY main.py ./
COPY requirements.txt ./

RUN pip install -r requirements.txt

CMD [ "python", "./main.py"]
