import socket
import threading

import requests
from datetime import datetime


BUFFER_SIZE = 4096

# Configuraciones globales
proxy_running = True
log_enabled = True
blacklist_enabled = True
blacklist_domains = [
    'wikipedia.org',
    'facebook.com', 
    'fbcdn.net',
    'googleapis.com'
]

def log_request(client_ip, target_host, target_ip, status, request_data):
    # Log normalization
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "client_ip": client_ip,
        "target_host": target_host,
        "target_ip": target_ip,
        "status": status,
        "request_data": request_data
    }

    # Post http request to send Logs to the Backend
    try:
        response = requests.post( "http://127.0.0.1:8000/proxy/logs/", json=log_entry, timeout=3 )
        
        if response.status_code == 201:
            print("[*] Log enviado exitosamente al backend.")
        else:
            print(f"[!] Error enviando log al backend: {response.status_code}")
    
    except Exception as e:
        print(f"[!] Fallo al enviar log: {e}")


# Manejo del cliente proxy
def handle_client(client_socket):
    global proxy_running, log_enabled, blacklist_enabled

    if not proxy_running:
        client_socket.close()
        return

    try:
        request = client_socket.recv(BUFFER_SIZE).decode()
        if log_enabled:
            print("[*] Received:", request)
    except Exception as e:
        print("[!] Failed to read request:", e)
        client_socket.close()
        return

    lines = request.split('\n')
    if not lines:
        client_socket.close()
        return

    first_line = lines[0]
    if not first_line.startswith('CONNECT'):
        client_socket.close()
        return

    target = first_line.split()[1]
    host, port = target.split(':')
    port = int(port)

    client_ip = client_socket.getpeername()[0]  # get_clientIp

    # Comprobación de blacklist por dominio
    if blacklist_enabled and any(black_domain in host for black_domain in blacklist_domains):
        print(f"[!] Bloqueado intento de acceso a {host}")
        client_socket.sendall(b"HTTP/1.1 403 Forbidden\r\n\r\nBlocked by proxy\r\n")
        
        if log_enabled:
            log_request(
                client_ip=client_ip,
                target_host=host,
                target_ip='0.0.0.0',  # No resolvimos IP real
                status="BLOCKED",
                request_data=first_line
            )
        
        client_socket.close()
        return

    try:
        remote_socket = socket.create_connection((host, port))
        target_ip = remote_socket.getpeername()[0]
    except Exception as e:
        print("[!] Connection failed:", e)
        client_socket.close()
        return

    client_socket.sendall(b"HTTP/1.1 200 Connection Established\r\n\r\n")

    if log_enabled:
        log_request(
            client_ip=client_ip,
            target_host=host,
            target_ip=target_ip,
            status="CONNECTED",
            request_data=first_line
        )

    def forward(src, dst):
        while True:
            try:
                data = src.recv(BUFFER_SIZE)
                if not data:
                    break
                dst.sendall(data)
            except:
                break

    threading.Thread(target=forward, args=(client_socket, remote_socket)).start()
    threading.Thread(target=forward, args=(remote_socket, client_socket)).start()


# Setting Management
def control_server(control_port=9999):
    global proxy_running, log_enabled, blacklist_enabled

    control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    control_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    control_socket.bind(('127.0.0.1', control_port))
    control_socket.listen(5)
    print(f"[*] Control Server listening on port {control_port}")

    while True:
        client, addr = control_socket.accept()
        print(f"[*] Control connection from {addr}")
        data = client.recv(1024).decode().strip()
        print(f"[*] Control Command Received: {data}")

        if data == 'START_PROXY':
            proxy_running = True
            client.sendall(b'OK')  
        elif data == 'STOP_PROXY':
            proxy_running = False
            client.sendall(b'OK')  
        elif data == 'ENABLE_LOG':
            log_enabled = True
            client.sendall(b'OK') 
        elif data == 'DISABLE_LOG':
            log_enabled = False
            client.sendall(b'OK') 
        elif data == 'ENABLE_BLACKLIST':
            blacklist_enabled = True
            client.sendall(b'OK') 
        elif data == 'DISABLE_BLACKLIST':
            blacklist_enabled = False
            client.sendall(b'OK')  
        elif data == 'GET_LOGS':
            try:
                with open('proxy.log', 'r') as log_file:
                    logs = log_file.read()
                client.sendall(logs.encode('utf-8'))
            except FileNotFoundError:
                client.sendall(b'NO_LOGS')

        else:
            client.sendall(b'OK') 

        client.close()

# Iniciar todo
def start_proxy(listen_port=8888):
    threading.Thread(target=control_server, daemon=True).start()

    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy_socket.bind(('0.0.0.0', listen_port))
    proxy_socket.listen(100)
    print(f"[*] HTTPS Proxy listening on port {listen_port}")

    while True:
        client_sock, addr = proxy_socket.accept()
        print(f"[*] Accepted connection from {addr}")
        threading.Thread(target=handle_client, args=(client_sock,)).start()

if __name__ == "__main__":
    start_proxy()
