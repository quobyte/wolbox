FROM python:3-slim as initializer

COPY run.sh /run.sh
COPY wolbox /wolbox
COPY setup.py /setup.py
COPY setup.cfg /setup.cfg

RUN /run.sh init

FROM python:3-slim

ENV WOLBOX_URL "localhost:8080"

COPY --from=initializer /run.sh /run.sh
COPY --from=initializer /wolbox /wolbox
COPY --from=initializer /venv /venv

EXPOSE 8080/tcp

ENTRYPOINT ["/run.sh"]
