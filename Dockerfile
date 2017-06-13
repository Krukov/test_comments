FROM python:3.5-alpine
RUN apk --update --no-cache add postgresql-dev gcc musl-dev libxml2-dev libxslt-dev

ADD requirements/ /tmp/requirements
RUN pip install -U pip \
    && pip install --compile --no-cache-dir -r /tmp/requirements/docker.txt \
    && rm -rf /tmp/requirements

ADD . /app
EXPOSE 8080
WORKDIR /app
