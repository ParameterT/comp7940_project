FROM ubuntu:20.04

# Install dependencies
RUN apt update
RUN apt install -y python3
RUN apt install -y pip


RUN pip install pymysql
RUN pip install requests
RUN pip install cryptography

# Copy the application folder inside the container
RUN mkdir /app
COPY *.py /app
WORKDIR /app

# Expose the port

# Run the command to start uWSGI
CMD ["python3", "app.py"]
