FROM python:3-slim as initializer

COPY run.sh /run.sh
COPY wolbox /wolbox
COPY setup.py /setup.py
COPY setup.cfg /setup.cfg

RUN /run.sh init

FROM python:3-slim

ENV WOLBOX_URL "localhost:8080"

# hadolint ignore=DL3008
RUN addgroup --system --gid 1337 wolbox \
 && adduser --system --uid 1337 --gid 1337 wolbox \
 && apt-get update \
 && apt-get install -y --no-install-recommends \
    nmap \
    wakeonlan \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

COPY --from=initializer /run.sh /run.sh
COPY --from=initializer /wolbox /wolbox
COPY --from=initializer /venv /venv

EXPOSE 8080/tcp
USER wolbox
WORKDIR /
ENTRYPOINT ["/run.sh"]
