FROM python:3.10

# Set the working directory
WORKDIR /app

# install required packages
 RUN apt-get update && apt-get install -y cron iputils-ping

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Copy the script into the container
COPY telepinger.py .

# Make the script executable
RUN chmod +x telepinger.py

# Set the environment variables
ENV MINUTES_INTERVAL=1
ENV INFLUXDB_BUCKET=my-bucket
ENV INFLUXDB_ORG=my-org
ENV INFLUXDB_TOKEN=my-token
ENV INFLUXDB_URL=http://localhost:8086
ENV PING_HOST=8.8.8.8
ENV PING_PACKETS=5
ENV PING_INTERVAL=0.5
ENV NOTIFY_ALWAYS=true

# set up the cron job
RUN echo "*/$MINUTES_INTERVAL * * * * /app/telepinger.py -c $PING_PACKETS -i $PING_INTERVAL $PING_HOST > /proc/1/fd/1 2>&1" | crontab -

# Start cron in the foreground
CMD ["cron", "-f"]