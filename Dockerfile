FROM python:3.12-slim
WORKDIR /app
RUN pip install mysql-connector-python==9.6.0
RUN pip install numpy==2.4.3
COPY data-generator.py .
CMD ["python", "data-generator.py"]
