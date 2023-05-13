FROM python:3.7
WORKDIR /usr/src/app
RUN apt-get update
COPY ./requirements.txt /usr/src/app
RUN pip install -r requirements.txt
COPY ./ /usr/src/app
CMD uvicorn app.main:app --reload --host 0.0.0.0