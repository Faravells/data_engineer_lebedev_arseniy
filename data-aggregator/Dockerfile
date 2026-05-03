FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY data-aggregator.py date-interval.txt .
CMD python data-aggregator.py
