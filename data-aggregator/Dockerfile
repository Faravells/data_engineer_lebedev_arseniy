FROM python:3.12-slim
WORKDIR /app
RUN pip install mysql-connector-python==9.6.0
COPY data-aggregator.py .
CMD python data-aggregator.py
