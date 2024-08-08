
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
    return response