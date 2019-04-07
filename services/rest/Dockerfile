FROM python:3.7
LABEL maintainer="adrian.kubica.ak@gmail.com"

ENV PYTHOUNBUFFERED 1

RUN apt-get update
ENV TZ Europe/Warsaw

ENV DJANGO_DEBUG_MODE False
ENV DJANGO_SECRET_KEY -^26!&88py4!ogzqv)isxhtl7_^m+-impj8ol99)(*!y39#0q*

WORKDIR /rest
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv
RUN pipenv install --system
COPY ./ ./

RUN adduser --system --disabled-password produser
USER produser

CMD ["gunicorn", "--config", "gunicorn_config.py", "app.wsgi"]