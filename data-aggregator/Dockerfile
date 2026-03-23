FROM python:3.12-slim
WORKDIR /app
RUN pip install mysql-connector-python==9.6.0
RUN pip install pandas==3.0.1
COPY data-aggregator.py date-interval.txt .
CMD python data-aggregator.py
