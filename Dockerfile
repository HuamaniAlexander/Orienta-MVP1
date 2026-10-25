FROM node:22-alpine AS web
WORKDIR /web
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml uv.lock ./
COPY packages/ ./packages/
RUN pip install --no-cache-dir uv && uv sync --frozen --no-dev
COPY backend/ ./backend/
COPY data/ ./data/
COPY --from=web /web/dist ./frontend/dist
ENV PYTHONPATH=/app/backend
RUN useradd --create-home app && chown -R app:app /app
USER app
EXPOSE 8000
CMD [".venv/bin/uvicorn","main:app","--host","0.0.0.0","--port","8000"]
