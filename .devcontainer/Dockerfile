FROM mcr.microsoft.com/vscode/devcontainers/base:0-jammy

RUN apt update && apt -y upgrade
RUN apt -y install python3-pip python3-venv

# Bitwuzla & dependencies
RUN pip install cython && \
    apt -y install build-essential cmake libgmp-dev
RUN git clone https://github.com/bitwuzla/bitwuzla && \
    cd bitwuzla && \
    ./contrib/setup-cadical.sh && \
    ./contrib/setup-btor2tools.sh && \
    ./contrib/setup-symfpu.sh && \
    ./configure.sh --python && \
    cd build && make && make install && ldconfig

# Linters
RUN pip install black pydocstyle

# Packaging toolchain
RUN pip install build twine wheel
