FROM python:3.8.11 as base
RUN apt-get update && python -m pip install --upgrade pip

ARG WORKDIR=/usr/src/app
ARG project

ENV PROJECT=${project}
ENV WORKDIR=${WORKDIR}
ENV PYTHONPATH "${PYTHONPATH}:${WORKDIR}:${WORKDIR}/${PROJECT}"

WORKDIR ${WORKDIR}

COPY framework framework

# test/lint stage
FROM base as test

COPY projects/${PROJECT}/src ${PROJECT}
COPY projects/${PROJECT}/requirements.txt ${PROJECT}/requirements.txt

COPY setup.cfg setup.cfg
RUN pip install --no-cache-dir -r framework/requirements_dev.txt
ENTRYPOINT ["./framework/bin/entrypoint.sh"]

# train stage
FROM base as train

COPY projects/${PROJECT}/src ${PROJECT}
COPY projects/${PROJECT}/requirements.txt ${PROJECT}/requirements.txt

RUN pip install --no-cache-dir -r framework/requirements.txt \
    && pip install --no-cache-dir -r ${PROJECT}/requirements.txt

ENTRYPOINT ["./framework/bin/entrypoint.sh"]

# serve stage
FROM base as serve

COPY projects/${PROJECT}/src/api ${PROJECT}/api
COPY projects/${PROJECT}/requirements.txt ${PROJECT}/requirements.txt

RUN pip install --no-cache-dir -r framework/requirements.txt \
    && pip install --no-cache-dir -r ${PROJECT}/api/requirements.txt

EXPOSE 8080
ENTRYPOINT ["./framework/bin/entrypoint.sh"]