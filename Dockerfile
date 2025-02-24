# Build stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY bot /app/bot

# Final stage
FROM gcr.io/distroless/python3-debian12:nonroot
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /app /app
WORKDIR /app
ENV PYTHONPATH=/usr/local/lib/python3.11/site-packages
CMD ["-m", "bot"]