FROM mcr.microsoft.com/vscode/devcontainers/base:0-jammy

RUN apt update && apt -y upgrade
RUN apt -y install python3-dev python3-pip python3-venv

# Bitwuzla & dependencies
RUN apt -y install autoconf build-essential cmake && \
    pip install cython
RUN curl https://gmplib.org/download/gmp/gmp-6.2.1.tar.xz | tar xJC /opt && \
	cd /opt/gmp-6.2.1 && \
    ./configure --enable-cxx --enable-fat && \
    make && make check && make install
RUN git clone https://github.com/bitwuzla/bitwuzla /opt/bitwuzla && \
    cd /opt/bitwuzla && \
    git checkout 1230d80a5275ddf525da9c218c2bcd29c3130e49 && \
    ./contrib/setup-cadical.sh && \
    ./contrib/setup-btor2tools.sh && \
    ./contrib/setup-symfpu.sh && \
    ./configure.sh --python && \
    cd build && make && make install && \
    mv /usr/local/lib/pybitwuzla.so /usr/lib/python3/dist-packages/ && \
    ldconfig
