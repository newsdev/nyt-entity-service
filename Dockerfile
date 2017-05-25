FROM python:3.5

ENV KUBERNETES_SECRET_ENV_VERSION=0.0.2
RUN \
  mkdir -p /etc/secret-volume && \
  cd /usr/local/bin && \
  curl -sfLO https://github.com/newsdev/kubernetes-secret-env/releases/download/$KUBERNETES_SECRET_ENV_VERSION/kubernetes-secret-env && \
  chmod +x kubernetes-secret-env

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uwsgi

COPY requirements.txt /usr/src/app/
RUN pip install -r /usr/src/app/requirements.txt
COPY . /usr/src/app/

ENV PYTHONPATH=/usr/src/app/entitysvc

EXPOSE 80
CMD ["kubernetes-secret-env", "/usr/local/bin/uwsgi", "--ini", "/usr/src/app/entitysvc/config/prd/docker.ini"]
