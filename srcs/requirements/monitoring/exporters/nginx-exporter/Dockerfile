FROM alpine:latest

RUN apk add --no-cache wget

RUN wget https://github.com/nginxinc/nginx-prometheus-exporter/releases/download/v0.11.0/nginx-prometheus-exporter_0.11.0_linux_amd64.tar.gz && \
    tar xvf nginx-prometheus-exporter_0.11.0_linux_amd64.tar.gz && \
    mv nginx-prometheus-exporter /usr/local/bin/ && \
    rm nginx-prometheus-exporter_0.11.0_linux_amd64.tar.gz && \
    chmod +x /usr/local/bin/nginx-prometheus-exporter

EXPOSE 9113

ENTRYPOINT ["/usr/local/bin/nginx-prometheus-exporter"]
CMD ["--nginx.scrape-uri", "http://nginx:8081/nginx_status"]