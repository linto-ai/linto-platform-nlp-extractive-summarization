FROM lintoai/linto-platform-nlp-core:latest
LABEL maintainer="gshang@linagora.com"

WORKDIR /app

COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY .envdefault /app/
COPY ./scripts /app/scripts
COPY ./components /app/components

HEALTHCHECK --interval=15s CMD curl -fs http://0.0.0.0/health || exit 1

ENTRYPOINT ["/opt/conda/bin/gunicorn", "scripts.main:app", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:80", "--access-logfile", "-", "--error-logfile", "-"]
CMD ["--workers", "1"]