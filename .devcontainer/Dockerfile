FROM mcr.microsoft.com/vscode/devcontainers/base:0-jammy

RUN apt update && apt -y upgrade
RUN apt -y install python3-pip python3-venv

# Bitwuzla & dependencies
RUN pip install cython && \
    apt -y install build-essential cmake libgmp-dev
RUN git clone https://github.com/bitwuzla/bitwuzla /opt/bitwuzla && \
    cd /opt/bitwuzla && \
    git checkout 1230d80a5275ddf525da9c218c2bcd29c3130e49 && \
    ./contrib/setup-cadical.sh && \
    ./contrib/setup-btor2tools.sh && \
    ./contrib/setup-symfpu.sh && \
    ./configure.sh --shared && \
    cd build && make && make install && ldconfig

# Linters
RUN pip install black pydocstyle

# Packaging toolchain
RUN pip install build twine wheel
