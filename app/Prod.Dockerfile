
###########
# BUILDER #
###########

# pull official base image
FROM python:3.12.10-slim-bookworm

# set work directory
ARG APP_HOME=/usr/src/django_jardin
WORKDIR ${APP_HOME}

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set up poetry
RUN pip install --upgrade pip
RUN pip install poetry
COPY pyproject.toml poetry.lock* ./

# Export dependencies as requirements.txt for the wheels
RUN poetry export -f requirements.txt > requirements.txt
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.12.10-slim-bookworm

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir -p $APP_HOME/staticfiles
RUN chown app:app $APP_HOME/staticfiles
RUN chmod 750 $APP_HOME/staticfiles
WORKDIR $APP_HOME

# install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat-openbsd && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false

# copy poetry configuration
COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-interaction --no-ansi --no-root

# copy entrypoint.prod.sh
COPY app/entrypoint.prod.sh .
RUN sed -i 's/\r$//g' $APP_HOME/entrypoint.prod.sh
RUN chmod +x $APP_HOME/entrypoint.prod.sh

# copy project
COPY app/ $APP_HOME/
RUN python manage.py collectstatic --no-input --clear

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

# run entrypoint.prod.sh
ENTRYPOINT ["/home/app/web/entrypoint.prod.sh"]