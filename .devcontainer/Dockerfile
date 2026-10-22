FROM mcr.microsoft.com/devcontainers/python:3.11

ENV PYTHONUNBUFFERED=1

# Pick up the fixed CA bundle (CVE-2026-111943)
RUN apt-get update \
    && apt-get install -y --no-install-recommends --only-upgrade ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN pipx install poetry==2.5.1

# Refresh the installer inherited from the base image, then install dev tooling.
RUN python -m pip install --no-cache-dir --upgrade pip setuptools wheel \
    && python -m pip install --no-cache-dir pre-commit
