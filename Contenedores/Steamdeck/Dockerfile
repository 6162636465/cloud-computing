FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir flask
COPY server.py .
EXPOSE 5000
CMD ["python","server.py"]
