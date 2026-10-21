FROM mcr.microsoft.com/devcontainers/python:3.10

ENV PYTHONUNBUFFERED 1

# Pick up the fixed CA bundle (CVE-2026-111943)
RUN apt-get update \
    && apt-get install -y --no-install-recommends --only-upgrade ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN pipx install poetry==1.8.3

# Install pre-commit
RUN pip install pre-commit
