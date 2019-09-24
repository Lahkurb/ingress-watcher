FROM python:alpine

# Create the workdir and copy the sources
RUN mkdir /app
WORKDIR /app
COPY . /app

# Pip install
RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev libressl-dev make && \
    pip install -r requirements.txt && \
    apk del .build-deps gcc musl-dev libffi-dev libressl-dev make

# Command
CMD [ "python", "./main.py" ]