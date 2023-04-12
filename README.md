# Telepinger

Telepinger is a simple tool that pings a specified host and sends the results to an InfluxDB database.

## Getting Started

To get started with Telepinger, first clone this repository:

```bash
git clone https://github.com/raskitoma/telepinger.git
```

Then, navigate to the `telepinger` directory:

```bash
cd telepinger 
```

Next, create a copy of the `docker-compose.sample.yml` file and update it with your own configuration:

```bash
cp docker-compose.sample.yml docker-compose.yml
nano docker-compose.yml
```

Do the same for config options, copy `config.sample.py` as `config.py`  and update it with your own configuration:

```bash
cp config.sample.py config.py
nano config.py
```

Build the Docker image:

```bash
docker compose build
```

Finally, start the Telepinger container using `docker compose`:

```bash
docker compose up -d
```

Telepinger will now start pinging the specified host and sending the results to your InfluxDB database at the specified interval.

## Configuration

Telepinger can be configured using the following environment variables:

- `MINUTES_INTERVAL`: The number of minutes between each ping (default: `1`).
- `PING_HOST`: The host to ping.
- `PING_PACKETS`: The number of ping packets to send (default: `5`).
- `PING_INTERVAL`: The interval between ping packets in seconds (default: `0.5`).

These environment variables can be set in the `environment` section of your `docker-compose.yml` file.

The rest of the configuration must be stored into `config.py` file:

- `INFLUXDB_BUCKET`: The name of the InfluxDB bucket to send data to.
- `INFLUXDB_ORG`: The name of the InfluxDB organization.
- `INFLUXDB_TOKEN`: The InfluxDB authentication token.
- `INFLUXDB_URL`: The URL of the InfluxDB server.
- `NOTIFY_ALWAYS`: `True` to send always results to inluxdb, `False` to send only when packet loss is detected (default: `True`).

`config.py` content must look like `config.sample.py` provided with this repo.
