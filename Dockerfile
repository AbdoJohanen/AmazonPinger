FROM python:3.10-slim
RUN mkdir /app
ADD . /app 
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "main.py"]