# Stage 1: Build SvelteKit frontend
FROM node:22-slim AS frontend
WORKDIR /app
RUN npm install -g pnpm
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
RUN pnpm install --frozen-lockfile
COPY svelte.config.js vite.config.ts tsconfig.json ./
COPY src ./src
COPY static ./static
RUN pnpm build

# Stage 2: Python backend + built frontend
FROM python:3.13-slim AS backend
WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Python deps
COPY pyproject.toml uv.lock ./
RUN uv sync --no-group dev

# App code
COPY main.py ./
COPY poker ./poker

# Frontend build output (SvelteKit outputs to 'build/')
COPY --from=frontend /app/build ./build

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
