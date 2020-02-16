FROM tunedmystic/python-async-deps as base



FROM base AS base-build

ARG EXTRA_REQUIREMENTS

# Modify Python path, to be able to get packages from the base image.
ENV PATH=/opt/local/bin:$PATH \
    PYTHONPATH=/opt/local/lib/python3.7/site-packages

RUN mkdir -p /opt/local

# Copy requirements and install.
COPY requirements.txt requirements-dev.txt /tmp/
RUN echo $EXTRA_REQUIREMENTS
RUN pip install \
    --prefix=/opt/local \
    --disable-pip-version-check \
    --no-warn-script-location \
    -r /tmp/${EXTRA_REQUIREMENTS:-requirements.txt}



FROM python:3.7.3-alpine3.9 AS final-build

# Install system dependencies.
RUN apk add --no-cache bash

# Copy requirements from builder image.
COPY --from=base-build /opt/local /opt/local

ENV APP_NAME=markette \
    APP_PATH=/app \
    DATABASE_DSN=postgresql://postgres:postgres@db:5432/postgres \
    PATH=/opt/local/bin:$PATH \
    PYTHONPATH=/opt/local/lib/python3.7/site-packages:/app/markette \
    PYTHONUNBUFFERED=1

WORKDIR $APP_PATH

# Copy application source.
COPY . $APP_PATH

EXPOSE 8000

CMD ["/app/bin/entrypoint.sh"]
