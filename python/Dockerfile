# set base image (host OS)
FROM python:3.7.9-slim


# set the working directory in the container
WORKDIR /home/backend/app

# copy the content of the local src directory to the working directory
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ . 

ENTRYPOINT [ "python" ]
CMD [ "-m", "src", "run", "--host=0.0.0.0", "--port=80" ]
