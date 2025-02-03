FROM alpine:latest as builder

RUN apk add --no-cache openssl

RUN mkdir -p /etc/ssl \
    && mkdir -p /ssl

RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
	-keyout /ssl/certificate.key -out /ssl/certificate.crt \
	-subj "/C=TH/ST=Bangkok/L=Bangkok/O=42/OU=42/CN=localhost"

RUN cp /ssl/certificate.* /etc/ssl/ \
    && chmod 666 /etc/ssl/*

FROM grafana/grafana:latest

COPY ./grafana.ini /etc/grafana/grafana.ini

COPY --from=builder /etc/ssl /etc/ssl

CMD ["grafana-server", "--config=/etc/grafana/grafana.ini"]