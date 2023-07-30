FROM python:3.10-slim

ENV POETRY_VERSION = 1.2.1

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /code

COPY ./poetry.lock ./pyproject.toml /code/

RUN poetry config virtualenvs.create false

RUN poetry install --no-interaction --no-root --without dev

ADD ./originations originations

EXPOSE 80

CMD ["uvicorn", "originations.main:app", "--host", "0.0.0.0", "--port", "80"]