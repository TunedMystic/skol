FROM tunedmystic/python-async-deps as base



# -------------------------------------
# Build the base image, installing pip dependencies.
# -------------------------------------

FROM base AS base-build

ARG REQUIREMENTS_FILE

# Modify Python path, to be able to get packages from the base image.
ENV PATH=/opt/local/bin:$PATH PYTHONPATH=/opt/local/lib/python3.8/site-packages

RUN mkdir -p /opt/local

# Copy requirements and install.
COPY requirements.txt requirements-dev.txt /tmp/

RUN pip install --prefix=/opt/local --disable-pip-version-check --no-warn-script-location -r /tmp/${REQUIREMENTS_FILE:-requirements.txt}



# -------------------------------------
# Build the final image, setting envs and copying over pip dependencies.
# -------------------------------------

FROM python:3.8.2-alpine3.11 AS final-build

# Install system dependencies.
RUN apk add --no-cache bash

# Copy requirements from builder image.
COPY --from=base-build /opt/local /opt/local

ENV APP_NAME=app APP_PATH=/usr/src PATH=/opt/local/bin:$PATH PYTHONPATH=/opt/local/lib/python3.8/site-packages:/usr/src/app PYTHONUNBUFFERED=1

WORKDIR $APP_PATH

COPY . $APP_PATH

EXPOSE 8000

CMD ["/usr/src/entrypoint.sh"]
