FROM python:3.13.3-alpine

WORKDIR /server

COPY requirements.txt requirements.txt

RUN \
    apk add --no-cache python3 postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev postgresql-dev && \
    python3 -m pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps

COPY . .

EXPOSE 10000

ENTRYPOINT [ "/server/start.sh" ]