FROM python:3.14.0-alpine3.20 AS builder
RUN pip install uv && adduser -D -u 1000 appuser
WORKDIR /home/appuser
COPY --chown=appuser:appuser pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project

FROM python:3.14.0-alpine3.20 AS production
RUN pip install uv && adduser -D -u 1000 appuser
WORKDIR /home/appuser
COPY --from=builder /home/appuser/.venv/ .venv/
COPY --chown=appuser:appuser src/ ./src/
USER appuser
ENV PATH="/home/appuser/.venv/bin:$PATH"
EXPOSE 10000
CMD ["fastapi", "run", "src/randomizer/main.py", "--host", "0.0.0.0", "--port", "10000"]
