# Python support can be specified down to the minor or micro version
# (e.g. 3.6 or 3.6.3).
# OS Support also exists for jessie & stretch (slim and full).
# See https://hub.docker.com/r/library/python/ for all supported Python
# tags from Docker Hub.
FROM python:3.7-slim-buster

# If you prefer miniconda:
#FROM continuumio/miniconda3

LABEL Name=discord-rddt-bot Version=1.0.0

WORKDIR /app
COPY Modules/ Modules/
COPY parameters/parameters.json parameters/
COPY requirements.txt .
COPY discord_listener.py .

# Using pip:
RUN python3 -m pip install -r requirements.txt
CMD ["python3", "./discord_listener.py"]