FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /backend

RUN pip install pipenv
COPY Pipfile Pipfile.lock /backend/
RUN pipenv install --system --dev

COPY . /backend

EXPOSE 8000