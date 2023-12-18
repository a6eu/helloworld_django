FROM python:3.11

RUN pip install poetry==1.5.0

WORKDIR /app
COPY . .

RUN poetry install

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN chmod +x ./scripts/launch.sh
EXPOSE $PORT

ENTRYPOINT ["sh", "launch.sh"]