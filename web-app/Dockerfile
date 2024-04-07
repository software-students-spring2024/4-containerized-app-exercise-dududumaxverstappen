FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt ./
RUN pip install -r requirements.txt

ADD . .

EXPOSE 4999

CMD ["python3", "python", "-m", "flask", "run", "--port=5002"]