FROM python:3.13-slim

# === System deps ===
RUN apt-get update && apt-get install -y \
  build-essential \
  && rm -rf /var/lib/apt/lists/*

# ===
COPY --from=ghcr.io/astral-sh/uv:0.8.24 /uv /uvx /bin/

# === Disable development dependencies ===
ENV UV_NO_DEV=1

# === Specify working dir ===
WORKDIR /app

# === Copy all files and directories ===
COPY . .

# === Install deps using uv ===
RUN uv sync --locked

# === Run entrypoint script ===
RUN chmod +x docker/entrypoint.sh

ENTRYPOINT ["docker/entrypoint.sh"]
