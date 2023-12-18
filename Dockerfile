FROM python:3.11

RUN pip install poetry==1.5.0

WORKDIR /app
COPY . .

RUN poetry install

CMD ["poetry", "python", "manage.py", "migrate"]
CMD ["poetry", "python", "manage.py", "makemigrations"]

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:9000"]