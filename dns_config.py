import speedtest
from ping3 import ping
import subprocess
import platform
import re  
import json  

def perform_speed_test():
    try:
        s = speedtest.Speedtest()
        s.get_best_server()

        print('Performing download test...')
        download_speed = s.download() / 10**6  # Convert bytes to megabits
        print(f'Download: {download_speed:.2f} Mbps')

        print('Performing upload test...')
        upload_speed = s.upload() / 10**6  # Convert bytes to megabits
        print(f'Upload: {upload_speed:.2f} Mbps')

        print('Performing ping test...')
        ping_time = ping('www.google.com')  # Ping Google's main page as a test
        print(f'Ping: {ping_time:.2f} ms')  # Print the ping in milliseconds

        return download_speed, upload_speed, ping_time
    except Exception as e:
        print(f'Error: {e}. Firewall may be preventing the speed test.')
        return None, None, None

def perform_packet_loss_test():
    try:
        print('Performing packet loss test...')
        packet_loss = subprocess.check_output(['ping', '-c', '10', 'www.google.com']).decode()
        packet_loss_percentage = float(packet_loss.split('% packet loss')[0].split()[-1])
        print(f'Packet Loss: {packet_loss_percentage}%')

        return packet_loss_percentage
    except Exception as e:
        print(f'Error: {e}. Firewall may be preventing the packet loss test.')
        return None

def perform_throughput_test():
    try:
        print('Performing throughput test...')
        throughput = subprocess.check_output(['iperf3', '-c', 'iperf.he.net', '-J']).decode()
        throughput_json = json.loads(throughput)
        throughput_value = throughput_json['end']['sum_received']['bits_per_second'] / 10**6  # Convert bits to megabits
        print(f'Throughput: {throughput_value:.2f} Mbps')

        return throughput_value
    except Exception as e:
        print(f'Error: {e}. Firewall may be preventing the throughput test.')
        return None

def perform_latency_test():
    try:
        print('Performing latency test...')
        latency = subprocess.check_output(['ping', '-c', '10', 'www.google.com']).decode()
        latency_values = re.findall(r'time=(\d+\.\d+)', latency)
        latency_average = sum(map(float, latency_values)) / len(latency_values)
        print(f'Latency: {latency_average:.2f} ms')

        return latency_average
    except Exception as e:
        print(f'Error: {e}. Firewall may be preventing the latency test.')
        return None

def perform_dns_resolution_test():
    try:
        print('Performing DNS resolution test...')
        dns_resolution_time = subprocess.check_output(['dig', 'www.google.com', '+stats']).decode()
        dns_resolution_time_value = float(re.search(r'Query time: (\d+)', dns_resolution_time).group(1))
        print(f'DNS Resolution Time: {dns_resolution_time_value:.2f} ms')

        return dns_resolution_time_value
    except Exception as e:
        print(f'Error: {e}. Firewall may be preventing the DNS resolution test.')
        return None

def perform_server_response_test():
    try:
        print('Performing server response test...')
        server_response_time = subprocess.check_output(['curl', '-o', '/dev/null', '-s', '-w', '%{time_total}', 'www.google.com']).decode()
        server_response_time_value = float(server_response_time) * 1000  # Convert seconds to milliseconds
        print(f'Server Response Time: {server_response_time_value:.2f} ms')

        return server_response_time_value
    except Exception as e:
        print(f'Error: {e}. Firewall may be preventing the server response test.')
        return None

def perform_bandwidth_test():
    try:
        print('Performing bandwidth test...')
        bandwidth = subprocess.check_output(['speedtest-cli', '--simple']).decode()
        bandwidth_values = bandwidth.split('\n')
        download_bandwidth = float(bandwidth_values[0].split()[1])
        upload_bandwidth = float(bandwidth_values[1].split()[1])
        print(f'Download Bandwidth: {download_bandwidth:.2f} Mbps')
        print(f'Upload Bandwidth: {upload_bandwidth:.2f} Mbps')

        return download_bandwidth, upload_bandwidth
    except Exception as e:
        print(f'Error: {e}. Firewall may be preventing the bandwidth test.')
        return None, None

def set_dns(primary_dns, secondary_dns):
    try:
        if platform.system() == 'Darwin':  # macOS
            # Get a list of all network services
            services = subprocess.check_output(['/usr/sbin/networksetup', '-listallnetworkservices']).decode().split('\n')
            services = [s for s in services if not s.startswith('*') and s and not s.startswith('An asterisk')]

            # Set DNS for each service
            for service in services:
                # Set primary and secondary DNS
                subprocess.run(['/usr/sbin/networksetup', '-setdnsservers', service, primary_dns, secondary_dns])

                # Get the current DNS settings for the service
                dns_settings = subprocess.check_output(['/usr/sbin/networksetup', '-getdnsservers', service]).decode().strip()
                print(f'DNS settings for {service}: {dns_settings}')

        elif platform.system() == 'Linux':  # Linux
            # Get a list of all network connections
            connections = subprocess.check_output(['nmcli', 'con', 'show']).decode().split('\n')
            connections = [c.split(':')[0] for c in connections if '802-3-ethernet' in c]

            # Set DNS for each connection
            for connection in connections:
                # Set primary and secondary DNS
                subprocess.run(['nmcli', 'con', 'mod', connection, 'ipv4.dns', f'{primary_dns} {secondary_dns}'])
                subprocess.run(['nmcli', 'con', 'up', connection])

                # Get the current DNS settings for the connection
                dns_settings = subprocess.check_output(['nmcli', 'con', 'show', connection, 'ipv4.dns']).decode().strip()
                print(f'DNS settings for {connection}: {dns_settings}')

        elif platform.system() == 'Windows':  # Windows
            # Get a list of all network interfaces
            interfaces = subprocess.check_output(['netsh', 'interface', 'ipv4', 'show', 'interface']).decode().split('\n')
            interfaces = [i.split(' ')[-1].strip() for i in interfaces if 'Up' in i]

            # Set DNS for each interface
            for interface in interfaces:
                # Set primary and secondary DNS
                subprocess.run(['netsh', 'interface', 'ipv4', 'set', 'dnsservers', interface, 'static', primary_dns, 'primary'])
                subprocess.run(['netsh', 'interface', 'ipv4', 'add', 'dnsservers', interface, secondary_dns])

                # Get the current DNS settings for the interface
                dns_settings = subprocess.check_output(['netsh', 'interface', 'ipv4', 'show', 'dnsservers', interface]).decode().strip()
                print(f'DNS settings for {interface}: {dns_settings}')

        else:
            print('Unsupported platform')

    except Exception as e:
        print(f'Error: {e}. Firewall may be preventing the DNS settings change.')

# Perform speed test before changing DNS
download_speed_before, upload_speed_before, ping_before = perform_speed_test()
packet_loss_before = perform_packet_loss_test()
throughput_before = perform_throughput_test()
latency_before = perform_latency_test()
dns_resolution_time_before = perform_dns_resolution_test()
server_response_time_before = perform_server_response_test()
download_bandwidth_before, upload_bandwidth_before = perform_bandwidth_test()

response = input("Do you want to change DNS settings? (y/n): ") 
if response == 'y':
    set_dns('1.1.1.1', '1.0.0.1') # Set Cloudflare's DNS servers
    print("DNS settings changed.")
else:
    print("DNS settings unchanged.")

# Perform speed test after changing DNS
download_speed_after, upload_speed_after, ping_after = perform_speed_test()
packet_loss_after = perform_packet_loss_test()
throughput_after = perform_throughput_test()
latency_after = perform_latency_test()
dns_resolution_time_after = perform_dns_resolution_test()
server_response_time_after = perform_server_response_test()
download_bandwidth_after, upload_bandwidth_after = perform_bandwidth_test()

# Calculate the differences
download_speed_difference = download_speed_after - download_speed_before if download_speed_after is not None and download_speed_before is not None else None
upload_speed_difference = upload_speed_after - upload_speed_before if upload_speed_after is not None and upload_speed_before is not None else None
ping_difference = ping_after - ping_before if ping_after is not None and ping_before is not None else None
packet_loss_difference = packet_loss_after - packet_loss_before if packet_loss_after is not None and packet_loss_before is not None else None
throughput_difference = throughput_after - throughput_before if throughput_after is not None and throughput_before is not None else None
latency_difference = latency_after - latency_before if latency_after is not None and latency_before is not None else None
dns_resolution_time_difference = dns_resolution_time_after - dns_resolution_time_before if dns_resolution_time_after is not None and dns_resolution_time_before is not None else None
server_response_time_difference = server_response_time_after - server_response_time_before if server_response_time_after is not None and server_response_time_before is not None else None
download_bandwidth_difference = download_bandwidth_after - download_bandwidth_before if download_bandwidth_after is not None and download_bandwidth_before is not None else None
upload_bandwidth_difference = upload_bandwidth_after - upload_bandwidth_before if upload_bandwidth_after is not None and upload_bandwidth_before is not None else None

# Print the results in a formatted table
print('-------------------------------------------------------')
print('| Metric                 | Before     | After      | Difference |')
print('-------------------------------------------------------')
def format_metric(metric_name, before_value, after_value, difference_value):
    if before_value is None or after_value is None or difference_value is None:
        return f'| {metric_name:<23} | Firewall/Network Issue | Firewall/Network Issue | Firewall/Network Issue |'
    else:
        return f'| {metric_name:<23} | {before_value:.2f} Mbps | {after_value:.2f} Mbps | {difference_value:.2f} Mbps |'



# Calculate the maximum width for each column
metric_width = max(len(metric_name) for metric_name in ['Download Speed', 'Upload Speed', 'Ping', 'Packet Loss', 'Throughput', 'Latency', 'DNS Resolution Time', 'Server Response Time', 'Download Bandwidth', 'Upload Bandwidth'])
value_width = max(len(str(value)) for value in [download_speed_before, download_speed_after, download_speed_difference, upload_speed_before, upload_speed_after, upload_speed_difference, ping_before, ping_after, ping_difference, packet_loss_before, packet_loss_after, packet_loss_difference, throughput_before, throughput_after, throughput_difference, latency_before, latency_after, latency_difference, dns_resolution_time_before, dns_resolution_time_after, dns_resolution_time_difference, server_response_time_before, server_response_time_after, server_response_time_difference, download_bandwidth_before, download_bandwidth_after, download_bandwidth_difference, upload_bandwidth_before, upload_bandwidth_after, upload_bandwidth_difference])
print('-------------------------------------------------------'.ljust(metric_width + 2))
print('| Metric                 | Before     | After      | Difference |'.ljust(metric_width + 2))
print('-------------------------------------------------------'.ljust(metric_width + 2))
# Format and print each row
def format_metric(metric_name, before_value, after_value, difference_value):
    if before_value is None or after_value is None or difference_value is None:
        return f'| {metric_name.ljust(metric_width)} | Firewall/Network Issue'.ljust(value_width+2) + '| Firewall/Network Issue'.ljust(value_width+2) + '| Firewall/Network Issue'.ljust(value_width+2) + '|'
    else:
        return f'| {metric_name.ljust(metric_width)} | {str(before_value).ljust(value_width)} Mbps'.ljust(value_width+2) + f'| {str(after_value).ljust(value_width)} Mbps'.ljust(value_width+2) + f'| {str(difference_value).ljust(value_width)} Mbps'.ljust(value_width+2) + '|'

print(format_metric('Download Speed', download_speed_before, download_speed_after, download_speed_difference))
print(format_metric('Upload Speed', upload_speed_before, upload_speed_after, upload_speed_difference))
print(format_metric('Ping', ping_before, ping_after, ping_difference))
print(format_metric('Packet Loss', packet_loss_before, packet_loss_after, packet_loss_difference))
print(format_metric('Throughput', throughput_before, throughput_after, throughput_difference))
print(format_metric('Latency', latency_before, latency_after, latency_difference))
print(format_metric('DNS Resolution Time', dns_resolution_time_before, dns_resolution_time_after, dns_resolution_time_difference))
print(format_metric('Server Response Time', server_response_time_before, server_response_time_after, server_response_time_difference))
print(format_metric('Download Bandwidth', download_bandwidth_before, download_bandwidth_after, download_bandwidth_difference))
print(format_metric('Upload Bandwidth', upload_bandwidth_before, upload_bandwidth_after, upload_bandwidth_difference))
print('-------------------------------------------------------'.ljust(metric_width + 2))
