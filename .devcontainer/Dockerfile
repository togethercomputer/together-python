FROM mcr.microsoft.com/devcontainers/python:3.11@sha256:1eb48ffd772f0618d66844eff8cbfd9914785be25f6a936d0756a1ddfc866cc3

ENV PYTHONUNBUFFERED=1

# Apply available OS security fixes, including the CA bundle (CVE-2026-111943)
RUN apt-get update \
    && apt-get upgrade -y --no-install-recommends \
    && apt-get install -y --no-install-recommends --only-upgrade ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN pipx install poetry==2.5.1

# Refresh the installer inherited from the base image, then install dev tooling.
RUN python -m pip install --no-cache-dir --upgrade pip setuptools wheel \
    && python -m pip install --no-cache-dir pre-commit
