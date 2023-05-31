FROM mcr.microsoft.com/vscode/devcontainers/base:0-jammy

COPY *.gpg /usr/share/keyrings/
COPY *.list /etc/apt/sources.list.d/

RUN apt update && apt -y upgrade

# Python
RUN apt -y install python3.8 python3.8-dev python3.8-venv python3-pip
RUN ln -sf /usr/bin/python3.8 /usr/bin/python3
RUN pip install --upgrade pip

# Bitwuzla: system dependencies
RUN apt -y install autoconf build-essential cmake
RUN pip install --upgrade cython

# Bitwula: libgmp
RUN curl https://gmplib.org/download/gmp/gmp-6.2.1.tar.xz | tar xJC /opt
WORKDIR /opt/gmp-6.2.1
RUN ./configure --enable-cxx --enable-fat
RUN make -j4 && make -j4 check && make install

# Bitwuzla
RUN git clone https://github.com/bitwuzla/bitwuzla /opt/bitwuzla
WORKDIR /opt/bitwuzla
RUN git checkout 1230d80a5275ddf525da9c218c2bcd29c3130e49
RUN ./contrib/setup-cadical.sh
RUN ./contrib/setup-btor2tools.sh
RUN ./contrib/setup-symfpu.sh
RUN ./configure.sh --python

WORKDIR /opt/bitwuzla/build
RUN make -j4 && make install
RUN mv /usr/local/lib/pybitwuzla.so /usr/lib/python3/dist-packages/
RUN ldconfig
