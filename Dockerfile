FROM python:3.11-alpine

ADD requirements.txt cleanup_gitlab_runner.py /app/

RUN apk add --no-cache --virtual .build-deps gcc musl-dev && \
  pip install -r /app/requirements.txt && \
  apk del .build-deps gcc musl-dev

ENTRYPOINT ["python", "/app/cleanup_gitlab_runner.py"]
