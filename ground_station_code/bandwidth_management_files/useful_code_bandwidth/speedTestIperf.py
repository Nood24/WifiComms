import iperf3

client = iperf3.Client()
client.duration = 1
client.server_hostname = '192.168.1.13'
client.port = 5201
client.protocol = 'udp'
result = client.run()
print(result.Mbps)
