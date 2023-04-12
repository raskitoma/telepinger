# Telepinger

Telepinger is a simple tool that pings a specified host and sends the results to an InfluxDB database.

## Getting Started

To get started with Telepinger, first clone this repository:

```bash
git clone https://github.com/raskitoma/telepinger.git
```

Then, navigate to the `telepinger` directory and build the Docker image:

```bash
cd telepinger docker-compose build
```

Next, create a copy of the `docker-compose.sample.yml` file and update it with your own configuration:

```bash
cp docker-compose.sample.yml docker-compose.yml nano docker-compose.yml
```

Finally, start the Telepinger container using `docker-compose`:

```bash
docker-compose up -d
```

Telepinger will now start pinging the specified host and sending the results to your InfluxDB database at the specified interval.

## Configuration

Telepinger can be configured using the following environment variables:

- `MINUTES_INTERVAL`: The number of minutes between each ping (default: `1`).
- `INFLUXDB_BUCKET`: The name of the InfluxDB bucket to send data to.
- `INFLUXDB_ORG`: The name of the InfluxDB organization.
- `INFLUXDB_TOKEN`: The InfluxDB authentication token.
- `INFLUXDB_URL`: The URL of the InfluxDB server.
- `PING_HOST`: The host to ping.
- `PING_PACKETS`: The number of ping packets to send (default: `5`).
- `PING_INTERVAL`: The interval between ping packets in seconds (default: `0.5`).

These environment variables can be set in the `environment` section of your `docker-compose.yml` file.