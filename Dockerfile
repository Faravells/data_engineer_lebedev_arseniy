FROM python:3.12-slim
WORKDIR /app
RUN pip install mysql-connector-python==9.6.0
COPY data-generator.py .
CMD ["python", "data-generator.py"]
