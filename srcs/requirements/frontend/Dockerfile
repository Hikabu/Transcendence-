FROM node:20 AS build

LABEL org.opencontainers.image.authors="Lera, Dima, Wolf, Jeremy"

WORKDIR /usr/src/app

COPY package.json yarn.lock ./

RUN yarn config set network-timeout 1000000
RUN yarn install
COPY . .
RUN yarn build

CMD ["echo", "Frontend build completed successfully"]
