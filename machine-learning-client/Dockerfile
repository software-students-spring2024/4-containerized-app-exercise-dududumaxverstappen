FROM python:3.8-slim

WORKDIR /machine_learning_client

COPY machine_learning_client/ ./

RUN pip install --upgrade pip \
    && pip install -r requirements.txt && apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

EXPOSE 5002

CMD ["python3", "flask", "run", "--port=5002"]