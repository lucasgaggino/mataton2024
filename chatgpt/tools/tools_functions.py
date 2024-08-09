
import requests
import json


def query_prometheus(query, prometheus_url='http://localhost:9090'):
    url = f"{prometheus_url}/api/v1/query"
    params = {'query': query}
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to query Prometheus: {response.status_code}, {response.text}")
    

def get_pc_data():
    queries = {
        'CPU Usage': '100 - (avg by (instance) (rate(windows_cpu_time_total{mode="idle"}[1m])) * 100)',
        'Memory Usage': 'windows_cs_physical_memory_bytes - windows_os_physical_memory_free_bytes',
        'Memory Usage Percentage': '(1 - (windows_os_physical_memory_free_bytes / windows_cs_physical_memory_bytes)) * 100',
        'Network Received': 'rate(windows_net_bytes_received_total[1m])',
        'Network Transmitted': 'rate(windows_net_bytes_sent_total[1m])'
    }
    
    response = []
    for name, query in queries.items():
        result = query_prometheus(query)
        response.append({name:result})
    return json.dumps(response)
    
DEFAULT_DEVICE_NAME = "Cisco Router Model IOS"
DEFAULT_BOOT_COMMAND = "flash:/cisco-ios-image.bin" 
DEFAULT_INTERFACE_NAME = "GigabitEthernet0/1"
def remediation_action_do_nothing(device_name: str) -> str:
    return ""
def remediation_action_restart_interface(device_name: str) -> str:
    return f"""
enable
configure terminal
interface {DEFAULT_INTERFACE_NAME}
shutdown
no shutdown
exit
exit
write memory
"""

def remediation_action_restart_device(device_name: str) -> str:
    return """
enable
reload in 0
"""
def remediation_action_change_bsp_configuration(device_name: str) -> str:
    return f"""
enable
configure terminal
boot system {DEFAULT_BOOT_COMMAND}
exit
write memory
"""
def get_ip_interface_brief(device_name: str) -> str:
    return """
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0     192.168.1.1     YES manual up                    up
GigabitEthernet0/1     unassigned      YES unset  administratively down down
GigabitEthernet0/2     10.0.0.1        YES manual up                    up
"""
def show_running_config_interface(device_name: str) -> str:
    return """
Building configuration...

Current configuration : 86 bytes
!
interface GigabitEthernet0/0
ip address 192.168.1.1 255.255.255.0
duplex auto
speed auto
end
"""
 
def show_interfaces(device_name: str) -> str:
    return """
GigabitEthernet0/0 is up, line protocol is up
    Hardware is iGbE, address is 0011.2233.4455 (bia 0011.2233.4455)
    Internet address is 192.168.1.1/24
    MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
        reliability 255/255, txload 1/255, rxload 1/255
    Encapsulation ARPA, loopback not set
    Keepalive set (10 sec)
    Full-duplex, 1Gbps, media type is RJ45
    output flow-control is XON, input flow-control is XON
    5 minute input rate 1000 bits/sec, 1 packets/sec
    5 minute output rate 2000 bits/sec, 2 packets/sec
        1000 packets input, 200000 bytes, 0 no buffer
        Received 1000 broadcasts, 0 runts, 0 giants, 0 throttles
        0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
        0 watchdog, 0 multicast, 0 pause input
        0 input packets with dribble condition detected
        2000 packets output, 400000 bytes, 0 underruns
        0 output errors, 0 collisions, 0 interface resets
        0 babbles, 0 late collision, 0 deferred
        0 lost carrier, 0 no carrier, 0 PAUSE output
        0 output buffer failures, 0 output buffers swapped out
"""
def show_ip_route(device_name: str) -> str:
    return """
Codes: C - connected, S - static, R - RIP, M - mobile, B - BGP
            D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
            N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
            E1 - OSPF external type 1, E2 - OSPF external type 2
            i - IS-IS, L1 - IS-IS level-1, L2 - IS-IS level-2, ia - IS-IS inter area
            * - candidate default, U - per-user static route, o - ODR
            P - periodic downloaded static route, + - replicated route

     Gateway of last resort is not set

     C    192.168.1.0/24 is directly connected, GigabitEthernet0/0
     O    10.0.0.0/24 [110/2] via 10.0.0.2, 00:00:03, GigabitEthernet0/2
""" 
def ping(device_name: str) -> str:
    return """
Type escape sequence to abort.
     Sending 5, 100-byte ICMP Echos to 192.168.1.1, timeout is 2 seconds:
     !!!!!
     Success rate is 100 percent (5/5), round-trip min/avg/max = 1/1/2 ms
"""
def traceroute(device_name: str) -> str:
    return """
Type escape sequence to abort.
     Tracing the route to 8.8.8.8

      1  192.168.1.254  1 msec  1 msec  1 msec
      2  10.0.0.2  2 msec  2 msec  2 msec
      3  172.16.0.1  10 msec  10 msec  10 msec
      4  *  *  *
      5  *  *  *
      6  8.8.8.8  50 msec  50 msec  50 msec
"""
def show_logging(device_name: str) -> str:
    return """
Syslog logging: enabled (0 messages dropped, 0 flushes, 0 overruns)
       Console logging: disabled
       Monitor logging: level debugging, 0 messages logged
       Buffer logging: level debugging, 20 messages logged
       Trap logging: level informational, 0 message lines logged

     Log Buffer (4096 bytes):
     %LINK-3-UPDOWN: Interface GigabitEthernet0/0, changed state to up
     %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet0/0, changed state to up
     %LINK-3-UPDOWN: Interface GigabitEthernet0/1, changed state to down
     %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet0/1, changed state to down
"""

