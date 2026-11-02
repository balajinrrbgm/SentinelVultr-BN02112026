FROM mcr.microsoft.com/playwright:v1.45.0-jammy

# Create non-root user
RUN useradd -m -u 1002 -s /bin/bash browseragent

# Install dependencies
RUN pip install --no-cache-dir playwright

WORKDIR /workspace
RUN chown -R browseragent:browseragent /workspace

USER browseragent
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

CMD ["python", "browser_task.py"]

