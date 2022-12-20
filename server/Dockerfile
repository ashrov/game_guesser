FROM python:3.10
COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR ./server
ADD . .

CMD ["python", "./main.py"]