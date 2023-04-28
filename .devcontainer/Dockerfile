ARG VARIANT=3-bullseye
FROM mcr.microsoft.com/vscode/devcontainers/python:${VARIANT}

ENV PYTHONUNBUFFERED=1 \
  PYTHONDONTWRITEBYTECODE=1

# ENV PIP_CERT= \
#   REQUESTS_CA_BUNDLE= \
#   NODE_EXTRA_CA_CERTS=

# COPY requirements.txt /tmp/pip-tmp/
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
#   && rm -rf /tmp/pip-tmp \
#   && apt-get update && export DEBIAN_FRONTEND=noninteractive \
#   && apt-get -y install --no-install-recommends <your-package-list-here>
