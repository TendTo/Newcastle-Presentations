FROM quay.io/jupyter/datascience-notebook

USER root

COPY requirements.txt /tmp/
RUN pip install --no-cache-dir --requirement /tmp/requirements.txt

