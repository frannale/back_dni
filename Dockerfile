# 
FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive

# 
WORKDIR /app

# 
COPY ./requirements.txt /app/requirements.txt

# 
RUN apt-get update
RUN apt-get -y install curl
RUN apt-get -y install python3-pip
RUN apt-get -y install unixodbc-dev
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# 
COPY ./ /app

EXPOSE 80

HEALTHCHECK  --interval=1m --timeout=5s \
  CMD curl --fail http://localhost:80/cursos || exit 1

# 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
