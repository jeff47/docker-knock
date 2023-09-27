FROM alpine:3.18 AS builder

RUN apk add g++ \
    pugixml-dev \
    openssl-dev \
    curl-dev \
    libzip-dev \
    make \
    bash \
    git

COPY ./libgourou /usr/src/libgourou

RUN cd /usr/src/libgourou \
  && make BUILD_STATIC=1

FROM alpine:3.18

ENV PYTHONPATH=/usr/local/lib/python3.11

RUN apk add --no-cache \
    libcurl \
    libzip \
    libmagic \
    pugixml \
    bash \
    python3 \
    py3-pip

RUN pip3 install click \
    xdg \
    python-magic \
    audible

COPY --from=builder /usr/src/libgourou/utils/acsmdownloader \
                    /usr/src/libgourou/utils/adept_activate \
                    /usr/src/libgourou/utils/adept_remove \
                    /usr/local/bin/

COPY ./knock/bin/knock.py /usr/local/bin
RUN mkdir -p /usr/local/lib/python3.11/
COPY ./knock/lib/* /usr/local/lib/python3.11/

COPY ./rmdrm/* /usr/local/bin
RUN chmod +x /usr/local/bin/*

WORKDIR /home/knock

ENTRYPOINT ["knock.py"]
