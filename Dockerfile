# ----------------------------------------------------
# In stage one, we're using the docker image that
# has some pip packages already installed.
# ----------------------------------------------------
FROM tunedmystic/uvicorn AS stage-one



# ----------------------------------------------------
# Install dbmate.
# ----------------------------------------------------

RUN apk add --no-cache curl; \
    curl -fsSL -o /usr/local/bin/dbmate "https://github.com/amacneil/dbmate/releases/download/v1.7.0/dbmate-linux-musl-amd64"; \
    chmod +x /usr/local/bin/dbmate;



# ----------------------------------------------------
# In stage two, we're installing the local pip
# packages. Dev dependencies will also be installed
# if ENV is 'dev' or 'test'.
# ----------------------------------------------------

FROM stage-one AS stage-two

ARG ENV

# Set the python path, so that pip can find the installed packages from the stage-one image.
ENV PYTHONPATH=/packages/lib/python3.8/site-packages

# Install system-level packages for psycopg2.
RUN apk add --no-cache gcc musl-dev postgresql-dev python3-dev

COPY requirements.txt /tmp/

RUN DEPS_FILE=/tmp/deps.txt; \
    cp /tmp/requirements.txt $DEPS_FILE; \
    if [ "$ENV" = "dev" ] || [ "$ENV" = "test" ]; then \
        echo "Installing packages + dev"; \
        sed 's/# dev //g' /tmp/requirements.txt > $DEPS_FILE; \
    else \
        echo "Installing packages"; \
    fi; \
    pip install \
        --no-cache-dir \
        --disable-pip-version-check \
        --no-warn-script-location \
        --prefix=/local-deps \
        -r $DEPS_FILE; \
    rm $DEPS_FILE;



# ----------------------------------------------------
# In the final stage, we're copying the source and
# the installed packages from the other stages.
# ----------------------------------------------------

FROM python:3.8.2-alpine3.11 AS final-stage

ENV APP_NAME=app \
    APP_PATH=/usr/src \
    PATH=/install/bin:$PATH \
    PYTHONPATH=/install/lib/python3.8/site-packages \
    PYTHONUNBUFFERED=1

WORKDIR $APP_PATH

RUN apk add --no-cache bash make

# Copy dbmate.
COPY --from=stage-one /usr/local/bin/dbmate /usr/local/bin/

# Copy system-level dependencies for psycopg2.
COPY --from=stage-two /usr/lib/libpq* /usr/lib/libldap_r* /usr/lib/liblber* /usr/lib/libsasl2* /usr/lib/

# Copy the installed packages.
COPY --from=stage-two /local-deps /install
COPY --from=stage-one /packages /install

# Copy source.
COPY . $APP_PATH

EXPOSE 8000

CMD ["/usr/src/bin/entrypoint.sh"]
