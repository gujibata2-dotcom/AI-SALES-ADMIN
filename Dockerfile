FROM python:3.12-slim
WORKDIR /app
COPY app /app/app
COPY tests /app/tests
ENV PYTHONUNBUFFERED=1 PORT=8080 AI_DB_PATH=/data/ai_business.sqlite3
RUN mkdir -p /data
EXPOSE 8080
CMD ["python","-m","app.api.customer_runtime.server"]
