FROM python:3.8

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script into the container
COPY telepinger.py .

# Set the environment variables
ENV MINUTES_INTERVAL=1
ENV INFLUXDB_BUCKET=my-bucket
ENV INFLUXDB_ORG=my-org
ENV INFLUXDB_TOKEN=my-token
ENV INFLUXDB_URL=http://localhost:8086
ENV PING_HOST=8.8.8.8
ENV PING_PACKETS=5
ENV PING_INTERVAL=0.5

# Install cron and set up the cron job
RUN apt-get update && apt-get install -y cron
RUN echo "*/$MINUTES_INTERVAL * * * * python /app/telepinger.py -c $PING_PACKETS -i $PING_INTERVAL $PING_HOST" | crontab -

# Start cron in the foreground
CMD ["cron", "-f"]