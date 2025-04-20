import socket
import select
from proxyTesting.config import BLACKLIST, BUFFER_SIZE

def is_blocked(host):
    for blocked_site in BLACKLIST:
        if blocked_site in host:
            return True
    return False

def forward(source, destination):
    while True:
        sockets = [source, destination]
        readable, _, _ = select.select(sockets, [], [])

        for sock in readable:
            data = sock.recv(BUFFER_SIZE)
            if not data:
                return
            other = destination if sock is source else source
            other.sendall(data)

def handle_client(client_socket):
    try:
        request = client_socket.recv(BUFFER_SIZE)
        if not request:
            client_socket.close()
            return

        first_line = request.split(b'\n')[0]
        first_line = first_line.decode()

        if first_line.startswith('CONNECT'):
            print("[+] Solicitud HTTPS detectada.")
            handle_https_tunnel(client_socket, first_line)
        else:
            print("[+] Solicitud HTTP detectada.")
            handle_http_request(client_socket, request)
    except Exception as e:
        print(f"[!] Error en manejar cliente: {e}")
        client_socket.close()

def handle_http_request(client_socket, initial_request):
    try:
        lines = initial_request.split(b"\r\n")
        host_line = [line for line in lines if line.lower().startswith(b"host:")]
        if not host_line:
            client_socket.close()
            return

        host = host_line[0].decode().split(":")[1].strip()
        port = 80

        if is_blocked(host):
            forbidden_response = b"HTTP/1.1 403 Forbidden\r\nContent-Type: text/html\r\n\r\n<h1>403 Forbidden</h1>"
            client_socket.sendall(forbidden_response)
            client_socket.close()
            return

        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((host, port))
        remote_socket.sendall(initial_request)

        forward(client_socket, remote_socket)
    except Exception as e:
        print(f"[!] Error en HTTP: {e}")
    finally:
        client_socket.close()

def handle_https_tunnel(client_socket, first_line):
    try:
        target = first_line.split(' ')[1]
        host, port = target.split(':')
        port = int(port)

        if is_blocked(host):
            forbidden_response = b"HTTP/1.1 403 Forbidden\r\nContent-Type: text/html\r\n\r\n<h1>403 Forbidden</h1>"
            client_socket.sendall(forbidden_response)
            client_socket.close()
            return

        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((host, port))

        client_socket.sendall(b"HTTP/1.1 200 Connection Established\r\n\r\n")

        forward(client_socket, remote_socket)
    except Exception as e:
        print(f"[!] Error en HTTPS: {e}")
    finally:
        client_socket.close()
