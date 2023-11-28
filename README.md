# DNS Configurator

This script performs various network performance tests such as speed test, packet loss test, throughput test, latency test, DNS resolution test, server response test, and bandwidth test. It then allows the user to change their DNS settings and performs the tests again to compare the results.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/DNS-Configurator.git
    cd DNS-Configurator
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the script with Python:
```bash
python dns_config.py
```
1. The script will first perform a series of network performance tests and print the results.
2. It will then ask if you want to change your DNS settings. If you choose to change your DNS settings, it will set your primary DNS to 1.1.1.1 and your secondary DNS to 1.0.0.1 (Cloudflare's DNS servers).
3. The script will run one last network performance test and print a table comparing the results of the tests before and after the DNS change.

## Note
This script uses several command line tools such as `ping`, `iperf3`, `dig`, `curl`, and `speedtest-cli`, and changes the DNS settings using the networksetup command. These commands may not be available or may work differently depending on your operating system. This script is designed to work on `macOS`, `Linux`, and `Windows`. If you're using a different operating system, you may need to modify the script.
