# pull official base image
FROM python:3.12.10-slim-bookworm

# set work directory
ARG APP_HOME=/usr/src/app
WORKDIR ${APP_HOME}

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-interaction --no-ansi --no-root

# copy entrypoint.sh
COPY app/entrypoint.sh .
RUN sed -i 's/\r$//g' ${APP_HOME}/entrypoint.sh
RUN chmod +x ${APP_HOME}/entrypoint.sh
RUN cp ${APP_HOME}/entrypoint.sh /entrypoint.sh

# copy project
COPY app/ .

# run entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
