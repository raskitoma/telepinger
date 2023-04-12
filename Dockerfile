FROM python:3.9-slim-buster
# Set the environment variables
ENV MINUTES_INTERVAL=1

# Set the working directory
WORKDIR /app

# install required packages
 RUN apt-get update && apt-get install -y cron iputils-ping

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN /usr/local/bin/python -m pip install --no-cache-dir -r requirements.txt

# Copy the script into the container
COPY telepinger.py .

# set up the cron job
RUN echo "*/$MINUTES_INTERVAL * * * * /usr/local/bin/python /app/telepinger.py -c $PING_PACKETS -i $PING_INTERVAL $PING_HOST > /proc/1/fd/1 2>&1" | crontab -

# Start cron in the foreground
CMD ["cron", "-f"]