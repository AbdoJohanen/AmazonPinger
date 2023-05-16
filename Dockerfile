FROM python:3.10-slim
RUN apt-get update && apt-get install -y chromium \
&& \
apt-get clean && \
rm -rf /var/lib/apt/lists/*
RUN mkdir /app
ADD . /app 
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "main.py"]