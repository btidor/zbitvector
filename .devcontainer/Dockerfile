# syntax = btidor/syntax

FROM mcr.microsoft.com/devcontainers/base:noble
COPY *.sources /etc/apt/sources.list.d/

# Bitwula: libgmp
ADD --apt autoconf build-essential cmake
ADD --checksum=sha256:a3c2b80201b89e68616f4ad30bc66aee4927c3ce50e33929ca819d5c43538898 \
    https://gmplib.org/download/gmp/gmp-6.3.0.tar.xz /opt
RUN tar xJf /opt/gmp-*.tar.xz -C /opt && rm /opt/gmp-*.tar.xz

WORKDIR /opt/gmp-6.3.0
RUN ./configure --enable-cxx --enable-fat
RUN make -j && make -j check && make install

# Python
ADD --apt python3.8 python3.8-dev python3.8-venv python3-pip
RUN ln -sf /usr/bin/python3.8 /usr/bin/python3
RUN pip install --upgrade cython

# Bitwuzla
RUN git clone https://github.com/bitwuzla/bitwuzla /opt/bitwuzla
WORKDIR /opt/bitwuzla
RUN git checkout 1230d80a5275ddf525da9c218c2bcd29c3130e49
RUN ./contrib/setup-cadical.sh
RUN ./contrib/setup-btor2tools.sh
RUN ./contrib/setup-symfpu.sh
RUN ./configure.sh --python

WORKDIR /opt/bitwuzla/build
RUN make -j && make install
RUN mv /usr/local/lib/pybitwuzla.so /usr/lib/python3/dist-packages/
RUN ldconfig
