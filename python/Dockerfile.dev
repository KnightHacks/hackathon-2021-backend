FROM python:3.9.0-slim

WORKDIR /home/backend/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "python" ]
CMD [ "-m", "src", "--host=0.0.0.0", "--port=5000" ]