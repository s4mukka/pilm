FROM docker.io/library/python:3.9

RUN useradd -m pilm

WORKDIR /home/pilm

ADD ../requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ../pilm/ pilm/

COPY ../scripts/* .

RUN chown -R pilm:pilm /home/pilm

USER pilm
