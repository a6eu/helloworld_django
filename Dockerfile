FROM python:3.10 as requirements-stage

WORKDIR /tmp
RUN pip install poetry==1.5.0
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


FROM python:3.10

WORKDIR /code
COPY --from=requirements-stage /tmp/requirements.txt .
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
COPY . .


ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8000", "site_market.wsgi:application ", "--access-logfile", "-", "--access-logformat", "%(h)s %(l)s %(u)s %(t)s '%(r)s' %(s)s %(b)s '%(f)s' '%(a)s'"]
