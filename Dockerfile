FROM python:3.11

WORKDIR /usr/app/src

COPY main.py ./
COPY requirements.txt ./

RUN pip install -r requirements.txt

CMD [ "python", "./main.py"]
