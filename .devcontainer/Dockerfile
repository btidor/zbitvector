FROM mcr.microsoft.com/vscode/devcontainers/base:0-jammy

RUN apt update && apt -y upgrade
RUN apt -y install python3-pip

RUN pip install black pydocstyle setuptools wheel twine
