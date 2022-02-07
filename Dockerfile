FROM ubuntu

ENV PYTHONPATH=/usr/local/lib/python3.8/local

RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive TZ="America/New_York" \
  apt-get install -y \
  python3 \
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

RUN cd /usr/src \ 
  && git clone https://github.com/BentonEdmondson/knock \
  && cp /usr/src/knock/src/knock.py /usr/local/bin \
  && mkdir -p /usr/local/lib/python3.8/local \
  && cp /usr/src/knock/lib/* /usr/local/lib/python3.8/local \
  && rm -r /usr/src/knock/

RUN cd /usr/src \
  && git clone https://github.com/BentonEdmondson/rmdrm/ \
  && cp /usr/src/rmdrm/rmdrm-* /usr/local/bin \
  && chmod +x /usr/local/bin/rmdrm-* \
  && rm -r /usr/src/rmdrm

RUN cd /usr/src \
  && git clone git://soutade.fr/libgourou.git \
  && cd libgourou \
  && make \
  && cp /usr/src/libgourou/libgourou.so         /usr/local/lib \
  && cp /usr/src/libgourou/utils/acsmdownloader /usr/local/bin \
  && cp /usr/src/libgourou/utils/adept_activate /usr/local/bin \
  && cp /usr/src/libgourou/utils/adept_remove   /usr/local/bin \
  && cd /home/knock \
  && rm -r /usr/src/libgourou \
  && ldconfig

COPY ./acsm /root/.config/knock/acsm

#CMD for file in *.acsm; do knock "$(pwd)"/$file; done

ENTRYPOINT ["knock.py"]
