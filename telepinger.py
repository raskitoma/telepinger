import subprocess
import platform
import re
import argparse
import influxdb_client
import socket
from config import INFLUXDB_BUCKET, INFLUXDB_ORG, INFLUXDB_TOKEN, INFLUXDB_URL, NOTIFY_ALWAYS
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime

parser = argparse.ArgumentParser(description='Ping a host and return the results')
parser.add_argument('host', help='The host to ping')
parser.add_argument('-c', '--count', help='The number of packets to send', type=int, default=5)
parser.add_argument('-i', '--interval', help='The interval between packets', type=float, default=0.5)

args = parser.parse_args()

print(f'==================== Starting Telepinger to {args.host}...')

starttime = datetime.now()

hostname = socket.gethostname()

os_name = platform.system()

print(f'Running {os_name} PING from {hostname} to {args.host} with {args.count} packets and {args.interval} interval')

if os_name == 'Linux':
    PING_CMD =  f'ping -q -c {args.count} -i {args.interval} {args.host}'
elif os_name == 'Windows':
    PING_CMD = f'ping -n {args.count} -w {args.interval * 1000} {args.host}'

ping_result = subprocess.check_output(PING_CMD, shell=True, text=True)

# set defaults
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
 
print(f'Pinged {args.host}: {packets_received} packets back out of {packets_sent} sent with {packet_loss}% packet loss. Min: {min_ms}ms, Max: {max_ms}ms, Avg: {avg_ms}ms') 

if NOTIFY_ALWAYS or packet_loss > 0:
    if packet_loss > 0:
        print('Packet loss detected!')

    if INFLUXDB_BUCKET=='telepinger-no-bucket':
        print('InfluxDB details have not been specified, not sending to InfluxDB')
    else:
        # open Influx
        print(f'Sending to InfluxDB: {INFLUXDB_URL}, {INFLUXDB_BUCKET}')
        client = influxdb_client.InfluxDBClient(
            url=INFLUXDB_URL,
            token=INFLUXDB_TOKEN,
            org=INFLUXDB_ORG
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
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=p)

endtime = datetime.now()

totaltime = endtime - starttime

print(f'Total time: {totaltime}')

print('==================== Telepinger finished')

