FROM prom/prometheus:latest

ARG PROMETHEUS_PASSWORD
ENV PROMETHEUS_PASSWORD=${PROMETHEUS_PASSWORD}

# copy configuration files
COPY prometheus.yml /etc/prometheus/prometheus.yml
COPY web.yml /etc/prometheus/web.yml
COPY alert_rules.yml /etc/prometheus/alert_rules.yml

# set up auth with password
COPY gen-pass.py /tmp/gen-pass.py
RUN apt-get update && apt-get install -y python3 python3-pip && \
    pip3 install bcrypt && \
    python3 /tmp/gen-pass.py "${PROMETHEUS_PASSWORD}" > /etc/prometheus/auth/password && \
    sed -i "s|hashed_password|$(cat /etc/prometheus/auth/password)|g" /etc/prometheus/web.yml && \
    rm -rf /tmp/gen-pass.py /var/lib/apt/lists/*

# set up SSL with proper permissions
RUN mkdir -p /etc/prometheus/ssl && \
    chown -R nobody:nobody /etc/prometheus/ssl
COPY ../../secrets/ssl /etc/prometheus/ssl/
RUN chmod 600 /etc/prometheus/ssl/*

USER nobody

EXPOSE 9090

CMD [ "--config.file=/etc/prometheus/prometheus.yml", \
      "--web.config.file=/etc/prometheus/web.yml" ]