FROM python:3.10

WORKDIR /machine_learning_client

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5002

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=5002"]

