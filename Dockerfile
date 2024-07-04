FROM --platform=linux/amd64 python:3.11-slim

RUN apt-get -y update && apt-get -y upgrade && apt-get install -y \ 
    ffmpeg \
    poppler-utils \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 3000

CMD ["reflex", "run"]
