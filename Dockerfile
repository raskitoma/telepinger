FROM python:3.9-slim-buster
LABEL MAINTAINER="Raskitoma.com/EAJ"
LABEL VERSION="1.0"
LABEL LICENSE="GPLv3"
LABEL DESCRIPTION="Raskitoma-Telepinger"

# Set the environment variables
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV TZ=America/New_York
ENV MINUTES_INTERVAL=1
ENV PING_HOST=8.8.8.8
ENV PING_PACKETS=5
ENV PING_INTERVAL=0.5

# Set the working directory
WORKDIR /app

# install required packages
RUN apt update && apt install --no-install-recommends -y cron iputils-ping

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN /usr/local/bin/python -m pip install --no-cache-dir -r requirements.txt

# Copy the script into the container
COPY telepinger.py .
COPY config.py .

# Copy the entrypoint script into the container
COPY entrypoint.sh .

RUN chmod +x entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]