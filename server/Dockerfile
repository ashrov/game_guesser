FROM python:latest
COPY requirements.txt .
RUN pip install -r requirements.txt

ADD . .

CMD ["python", "./main.py"]