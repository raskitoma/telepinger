import os
import subprocess
import platform
import re
import argparse
import influxdb_client
import socket
import logging
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime

parser = argparse.ArgumentParser(description='Ping a host and return the results')
parser.add_argument('host', help='The host to ping')
parser.add_argument('-c', '--count', help='The number of packets to send', type=int, default=5)
parser.add_argument('-i', '--interval', help='The interval between packets', type=float, default=0.5)

args = parser.parse_args()

# setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.info("Starting Telepinger")
logger.info('Getting environment variables')

bucket = os.environ.get('INFLUXDB_BUCKET')
org = os.environ.get('INFLUXDB_ORG')
token = os.environ.get('INFLUXDB_TOKEN')
url = os.environ.get('INFLUXDB_URL')
notify_always = os.environ.get('NOTIFY_ALWAYS', 'True')
notify_always = notify_always.lower() in ['true', '1', 'yes']

if not all([bucket, org, token, url]):
    print("Missing InfluxDB configuration. Please check environment variables.")
    logger.info('Missing InfluxDB configuration. Please check environment variables.')
    exit(1)

hostname = socket.gethostname()

os_name = platform.system()

logger.info(f'Running PING on {os_name} to {args.host}')

if os_name == 'Linux':
    PING_CMD =  f'ping -q -c {args.count} -i {args.interval} {args.host}'
elif os_name == 'Windows':
    PING_CMD = f'ping -n {args.count} -w {args.interval * 1000} {args.host}'

ping_result = subprocess.check_output(PING_CMD, shell=True, text=True)

packets_sent = 0
packets_received = 0
packet_loss = 0
min_ms = 0
max_ms = 0
avg_ms = 0

if os_name == 'Windows':
    packets_sent = int(re.search(r'Packets: Sent = (\d+)', ping_result).group(1))
    packets_received = int(re.search(r'Received = (\d+)', ping_result).group(1))
    packet_loss = float(re.search(r'Lost = (\d+)', ping_result).group(1))
    min_ms = float(re.search(r'Minimum = (\d+)ms', ping_result).group(1))
    max_ms = float(re.search(r'Maximum = (\d+)ms', ping_result).group(1))
    avg_ms = float(re.search(r'Average = (\d+)ms', ping_result).group(1))
elif os_name == 'Linux':
    packets_sent = int(re.search(r'(\d+) packets transmitted', ping_result).group(1))
    packets_received = int(re.search(r'(\d+) received', ping_result).group(1))
    packet_loss = float(re.search(r'(\d+)% packet loss', ping_result).group(1))
    min_ms = float(re.search(r'rtt min/avg/max/mdev = ([\d.]+)/', ping_result).group(1))
    max_ms = float(re.search(r'rtt min/avg/max/mdev = [\d.]+/([\d.]+)/', ping_result).group(1))
    avg_ms = float(re.search(r'rtt min/avg/max/mdev = [\d.]+/[\d.]+/([\d.]+)/', ping_result).group(1))
 
if notify_always or packet_loss > 0:
    logger.info('Sending to InfluxDB')
    if packet_loss > 0:
        logger.warning('Packet loss detected!')
    # open Influx
    client = influxdb_client.InfluxDBClient(
        url=url,
        token=token,
        org=org
    )

    write_api = client.write_api(write_options=SYNCHRONOUS)

    p = influxdb_client.Point("ping") \
        .tag("host", hostname) \
        .tag("dest", args.host) \
        .field("trx", packets_sent) \
        .field("rcx", packets_received) \
        .field("loss", packet_loss) \
        .field("min", min_ms) \
        .field("max", max_ms) \
        .field("avg", avg_ms)
    write_api.write(bucket=bucket, org=org, record=p)

current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

message = f'{current_time} - Pinged {args.host} from {hostname} and got {packets_received} packets back out of {packets_sent} sent with {packet_loss}% packet loss. Min: {min_ms}ms, Max: {max_ms}ms, Avg: {avg_ms}ms'
print(message)
logger.info(message)