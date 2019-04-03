FROM python:3.7
LABEL maintainer="adrian.kubica.ak@gmail.com"

ENV PYTHOUNBUFFERED 1

WORKDIR /rest
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv
RUN pipenv install --system
COPY ./ ./

RUN adduser -D prod_user
USER prod_user

CMD ["gunicorn", "--config", "gunicorn_config.py", "app.wsgi"]