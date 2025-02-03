FROM alpine:latest as builder

ARG PROMETHEUS_PASSWORD=$PROMETHEUS_PASSWORD

RUN apk add --no-cache python3 py3-pip py3-virtualenv

RUN mkdir -p /etc/prometheus/auth

COPY passw-gen.py /passw-gen.py

RUN python3 -m venv /venv && . /venv/bin/activate && pip install bcrypt

RUN . /venv/bin/activate && \
    python3 /passw-gen.py ${PROMETHEUS_PASSWORD} > /etc/prometheus/auth/hashed_password

FROM prom/prometheus:latest

USER root

RUN mkdir -p /etc/prometheus/auth /etc/prometheus/ssl

COPY --from=builder /etc/prometheus/auth /etc/prometheus/auth
COPY prometheus.yml /etc/prometheus/prometheus.yml
COPY web.yml /etc/prometheus/web.yml
COPY alert_rules.yml /etc/prometheus/alert_rules.yml

RUN chown -R nobody:nobody /etc/prometheus

RUN HASHED_PASSWORD=$(cat /etc/prometheus/auth/hashed_password) && \
    sed -i 's|hashed_password|'"$HASHED_PASSWORD"'|g' /etc/prometheus/web.yml

USER nobody