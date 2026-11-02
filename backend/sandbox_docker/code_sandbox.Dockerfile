FROM python:3.11-slim

# Create isolated, unprivileged user
RUN useradd -m -u 1001 -s /bin/bash sentinel

# Install standard analytical packages
RUN pip install --no-cache-dir \
    numpy \
    pandas \
    matplotlib \
    requests \
    tabulate

WORKDIR /workspace
RUN chown -R sentinel:sentinel /workspace

USER sentinel

# Entrypoint default
CMD ["python", "entrypoint.py"]

