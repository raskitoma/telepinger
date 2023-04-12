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

# set up the cron job
RUN echo "*/$MINUTES_INTERVAL * * * * /usr/local/bin/python /app/telepinger.py -c $PING_PACKETS -i $PING_INTERVAL $PING_HOST > /proc/1/fd/1 2>&1" | crontab -
RUN crontab -l

# Start cron in the foreground
CMD ["cron", "-f"]