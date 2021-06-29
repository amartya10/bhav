FROM python:3.8

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install --upgrade pip && pip install pipenv

COPY Pipfile* ./

RUN pipenv install --system --dev && rm -rf /root/.cache/pip

COPY ./ ./

RUN pylint app/

EXPOSE 8000

ENTRYPOINT ["entrypoint.sh"]
