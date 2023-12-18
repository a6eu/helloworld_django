FROM python:3.11

RUN pip install poetry==1.5.0

WORKDIR /app
COPY . .

RUN poetry install

ENTRYPOINT ["sh", "launch.sh"]