FROM ubuntu:latest

# Build instructions...
RUN apt-get update -y && apt-get install python3 -y
COPY app /app/
WORKDIR /app
RUN pip3 install -r requirements.txt

# Boot command
ENV FLASK_APP=hello.py
ENV FLASK_ENV=development
CMD ["flask", "run", "--host", "0.0.0.0"]

