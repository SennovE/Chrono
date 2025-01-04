FROM python:3.12

WORKDIR /backend

RUN pip install poetry

COPY /backend/pyproject.toml /backend/poetry.lock /backend

RUN poetry config virtualenvs.create false && poetry install --no-root

COPY /backend/app /backend/app

ENV PYTHONPATH=/backend

CMD ["poetry", "run", "sh", "-c", "cd app/db && alembic upgrade head && cd .. && python3 ./main.py"]
