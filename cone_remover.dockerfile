# Python support can be specified down to the minor or micro version
# (e.g. 3.6 or 3.6.3).
# OS Support also exists for jessie & stretch (slim and full).
# See https://hub.docker.com/r/library/python/ for all supported Python
# tags from Docker Hub.
FROM python:3.7-slim-buster

# If you prefer miniconda:
#FROM continuumio/miniconda3

WORKDIR /app
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

COPY Modules/ Modules/
COPY parameters/parameters.json parameters/
COPY cone_remover.py .

CMD ["python3", "./cone_remover.py"]