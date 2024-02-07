FROM python:3.11

WORKDIR /usr/app/src

COPY . /usr/app/src/

# COPY main.py ./
# COPY requirements.txt ./
# ADD asana ./asana
# ADD procore ./procore

RUN pip install -r requirements.txt

CMD [ "python", "./main.py"]
