import time
from collections import defaultdict, deque
from scapy.all import *

# Configuration Variables
THRESHOLD = 100  # Threshold for packet count from a single IP to trigger an alert
TIME_WINDOW = 10  # Time window in seconds to monitor packets

# Data Structures
packet_counts = defaultdict(int)  # Tracks packet counts per IP
timestamps = deque()  # Keeps track of timestamps of each packet


def monitor_packet(pkt):
    if IP in pkt:
        src_ip = pkt[IP].src
        current_time = time.time()
        timestamps.append((src_ip, current_time))
        packet_counts[src_ip] += 1

        # Maintain the deque and packet count
        while timestamps and timestamps[0][1] < current_time - TIME_WINDOW:
            old_ip = timestamps.popleft()[0]
            packet_counts[old_ip] -= 1
            if packet_counts[old_ip] == 0:
                del packet_counts[old_ip]

        # Check if the threshold is exceeded
        if packet_counts[src_ip] > THRESHOLD:
            print(f"High traffic detected from {src_ip}! Possible DoS attack.")


def main():
    print("Starting DoS detection...")
    sniff(prn=monitor_packet)  # Using Scapy to sniff network traffic


if __name__ == '__main__':
    main()
