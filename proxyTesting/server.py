import socket
import threading
from proxyTesting.handler import handle_client
from proxyTesting.config import PROXY_HOST, PROXY_PORT

def start_proxy():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((PROXY_HOST, PROXY_PORT))
    server.listen(100)

    print(f"[+] Proxy escuchando en {PROXY_HOST}:{PROXY_PORT}")

    while True:
        client_socket, addr = server.accept()
        print(f"[+] Nueva conexión desde {addr}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()
