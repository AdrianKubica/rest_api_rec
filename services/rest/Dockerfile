FROM python:3.7-alpine
LABEL maintainer="adrian.kubica.ak@gmail.com"

ENV PYTHOUNBUFFERED 1

RUN apk update
RUN apk add --no-cache python3 python3-dev gcc musl-dev zlib-dev libffi-dev openssl-dev ca-certificates
ENV TZ Europe/Warsaw

ENV DJANGO_DEBUG_MODE False
ENV DJANGO_SECRET_KEY -^26!&88py4!ogzqv)isxhtl7_^m+-impj8ol99)(*!y39#0q*

WORKDIR /rest
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv
RUN pipenv install --system
COPY ./ ./

RUN adduser -D produser
USER produser

CMD ["gunicorn", "--config", "gunicorn_config.py", "app.wsgi"]