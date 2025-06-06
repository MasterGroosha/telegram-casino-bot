## Build stage
FROM ghcr.io/astral-sh/uv:bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_PYTHON_INSTALL_DIR=/python UV_PYTHON_PREFERENCE=only-managed
RUN uv python install 3.11
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev --no-editable
COPY ./bot /app/bot
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-editable


## Final stage
FROM gcr.io/distroless/python3-debian12:nonroot
COPY --from=builder --chown=nonroot:nonroot /python /python
WORKDIR /app
COPY --from=builder --chown=nonroot:nonroot /app/ /app

ENV PYTHONPATH="/app/.venv/lib/python3.11/site-packages:$PYTHONPATH"
CMD ["-m", "bot"]
