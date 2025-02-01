FROM prom/alertmanager:latest

ARG SMTP_TO SMTP_FROM SMTP_SMARTHOST SMTP_AUTH_USERNAME SMTP_AUTH_IDENTITY SMTP_AUTH_PASSWORD

COPY config/alertmanager.yml /etc/alertmanager/alertmanager.yml

RUN sed -i \
    -e "s|SMTP_TO|${SMTP_TO}|g" \
    -e "s|SMTP_FROM|${SMTP_FROM}|g" \
    -e "s|SMTP_SMARTHOST|${SMTP_SMARTHOST}|g" \
    -e "s|SMTP_AUTH_USERNAME|${SMTP_AUTH_USERNAME}|g" \
    -e "s|SMTP_AUTH_IDENTITY|${SMTP_AUTH_IDENTITY}|g" \
    -e "s|SMTP_AUTH_PASSWORD|${SMTP_AUTH_PASSWORD}|g" \
    /etc/alertmanager/alertmanager.yml

CMD ["--config.file=/etc/alertmanager/alertmanager.yml"]