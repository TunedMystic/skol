# ----------------------------------------------------
# In stage one, we're using the docker image that
# has async pip packages already installed.
# ----------------------------------------------------

FROM tunedmystic/python-async-deps as stage-one



# ----------------------------------------------------
# In stage two, we're installing the local pip
# packages. Dev dependencies will also be installed
# if ENV is 'dev' or 'test'.
# ----------------------------------------------------

FROM stage-one AS stage-two

ARG ENV

ENV PYTHONPATH=/async-deps/lib/python3.8/site-packages

COPY requirements.txt /tmp/

RUN DEPS_FILE=/tmp/deps.txt; \
	cp /tmp/requirements.txt $DEPS_FILE; \
	if [ "$ENV" = "dev" ] || [ "$ENV" = "test" ]; then \
		echo "Installing dev dependencies"; \
		sed 's/# dev //g' /tmp/requirements.txt > $DEPS_FILE; \
	else \
		echo "Installing dependencies"; \
	fi; \
	pip install \
        --no-cache-dir \
        --disable-pip-version-check \
        --no-warn-script-location \
        --prefix=/local-deps \
        -r $DEPS_FILE; \
    rm $DEPS_FILE;



# ----------------------------------------------------
# In stage three, we're copying the source and
# the installed packages from the other stages.
# ----------------------------------------------------

FROM python:3.8.2-alpine3.11 AS stage-three

ENV APP_NAME=app \
    APP_PATH=/usr/src \
    PATH=/install/bin:$PATH \
    PYTHONPATH=/install/lib/python3.8/site-packages \
    PYTHONUNBUFFERED=1

WORKDIR $APP_PATH

RUN apk add --no-cache bash make

COPY --from=stage-two /async-deps /install
COPY --from=stage-two /local-deps /install
COPY . $APP_PATH

EXPOSE 8000

CMD ["/usr/src/bin/entrypoint.sh"]
