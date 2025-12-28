import socket
import os

host = "db.turgapierpswzokwnqvq.supabase.co"

print(f"Testing resolution for: {host}")

try:
    ip = socket.gethostbyname(host)
    print(f"socket.gethostbyname returned: {ip}")
except Exception as e:
    print(f"socket.gethostbyname failed: {e}")

try:
    info = socket.getaddrinfo(host, 5432)
    print("socket.getaddrinfo returned:")
    for res in info:
        print(res)
except Exception as e:
    print(f"socket.getaddrinfo failed: {e}")
