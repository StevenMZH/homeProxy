import socket
import threading
from django.utils.timezone import now


BUFFER_SIZE = 4096

# Lista de IPs a bloquear (Ejemplo: Añadir IPs de YouTube)
blacklist_ips = [
    '216.58.210.14',  # Esta IP puede cambiar; necesitas una lista actualizada
    # Agregar más IPs aquí si las obtuviste o quieres bloquear más
]

def handle_client(client_socket):
    
    # 1. Leer solicitud inicial
    try:
        request = client_socket.recv(BUFFER_SIZE).decode()
        print("[*] Received:", request)
    except Exception as e:
        print("[!] Failed to read request:", e)
        client_socket.close()
        return

    # 2. Extraer host y puerto
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

    # 3. Obtener IP del host
    try:
        host_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print(f"[!] No se pudo resolver {host}")
        client_socket.close()
        return

    # 4. Comprobar si la IP está en la blacklist
    if host_ip in blacklist_ips:
        print(f"[!] Bloqueado intento de acceso a {host} ({host_ip})")
        client_socket.sendall(b"HTTP/1.1 403 Forbidden\r\n\r\nBlocked by proxy\r\n")
        client_socket.close()
        return

    # 5. Registrar log del proxy
    log = ProxyLog(
        client_ip=client_socket.getpeername()[0],
        target_host=host,
        target_ip=host_ip,
        status="200 Connection Established",
        request_data=request
    )
    log.save()

    # 6. Conectar al servidor de destino
    try:
        remote_socket = socket.create_connection((host, port))
    except Exception as e:
        print("[!] Connection failed:", e)
        client_socket.close()
        return

    # 7. Decirle al cliente que la conexión está OK
    client_socket.sendall(b"HTTP/1.1 200 Connection Established\r\n\r\n")

    # 8. Reenviar datos
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

def start_proxy(listen_port=8888):
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy_socket.bind(('0.0.0.0', listen_port))
    proxy_socket.listen(100)
    print(f"[*] HTTPS Proxy listening on port {listen_port}")

    while True:
        client_sock, addr = proxy_socket.accept()
        print(f"[*] Accepted connection from {addr}")
        threading.Thread(target=handle_client, args=(client_sock,)).start()
        
if __name__ == '__main__':
    start_proxy()