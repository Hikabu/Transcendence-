FROM grafana/grafana:9.5.5

COPY grafana.ini /etc/grafana/grafana.ini
COPY dashboards /var/lib/grafana/dashboards
COPY provisioning /etc/grafana/provisioning

RUN mkdir -p /etc/grafana/ssl && \
    chown -R grafana:grafana /etc/grafana/ssl
COPY ../../secrets/ssl /etc/grafana/ssl
RUN chmod 600 /etc/grafana/ssl/*

EXPOSE 3000

USER grafana

CMD ["grafana-server", "--config=/etc/grafana/grafana.ini"]
