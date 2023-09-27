FROM ubuntu:20.04

ENV PYTHONPATH=/usr/local/lib/python3.8/local

RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive TZ="America/New_York" \
  apt-get install -y \
  python3=3.8.2 \
  pip \
  bash \
  git \
  wget \
  tzdata \
  build-essential \
  libzip-dev \
  libssl-dev \
  qtbase5-private-dev \ 
  && apt-get autoclean \
  && rm -rf /var/lib/apt/lists/*

RUN pip install click \
  xdg  \
  python-magic \
  audible

WORKDIR /home/knock

COPY ./knock/bin/knock.py /usr/local/bin
RUN mkdir -p /usr/local/lib/python3.8/local
COPY ./knock/lib/* /usr/local/lib/python3.8/local \
  

COPY ./rmdrm/* /usr/local/bin
RUN chmod +x /usr/local/bin/rmdrm-*

COPY ./libgourou /usr/src/libgourou

RUN cd /usr/src/libgourou \
  && make \
  && cp /usr/src/libgourou/libgourou.so         /usr/local/lib \
  && cp /usr/src/libgourou/utils/acsmdownloader /usr/local/bin \
  && cp /usr/src/libgourou/utils/adept_activate /usr/local/bin \
  && cp /usr/src/libgourou/utils/adept_remove   /usr/local/bin \
  && cd /home/knock \
  && rm -r /usr/src/libgourou
  && ldconfig

COPY ./acsm /root/.config/knock/acsm

ENTRYPOINT ["knock.py"]
