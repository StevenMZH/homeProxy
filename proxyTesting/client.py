import socket
import ssl

# Configuraciones
PROXY_HOST = '127.0.0.1'  # El proxy está corriendo localmente
PROXY_PORT = 8888

DEST_HOST = 'www.google.com'
DEST_PORT = 443  # HTTPS estándar

def main():
    # Conectarse al proxy
    client_socket = socket.create_connection((PROXY_HOST, PROXY_PORT))
    print("[+] Conectado al proxy")

    # Pedimos al proxy que haga un túnel hacia el servidor destino
    connect_request = f"CONNECT {DEST_HOST}:{DEST_PORT} HTTP/1.1\r\nHost: {DEST_HOST}\r\n\r\n"
    client_socket.sendall(connect_request.encode())

    # Leemos la respuesta del proxy
    response = client_socket.recv(4096)
    if b"200 Connection Established" not in response:
        print("[!] Error al establecer túnel")
        client_socket.close()
        return

    print("[+] Túnel HTTPS establecido")

    # Ahora envolvemos el socket en SSL
    context = ssl.create_default_context()
    secure_socket = context.wrap_socket(client_socket, server_hostname=DEST_HOST)

    # Hacemos una solicitud HTTPS
    https_request = f"GET / HTTP/1.1\r\nHost: {DEST_HOST}\r\nConnection: close\r\n\r\n"
    secure_socket.sendall(https_request.encode())

    # Recibimos la respuesta
    response_data = b""
    while True:
        data = secure_socket.recv(4096)
        if not data:
            break
        response_data += data

    print("[+] Respuesta recibida:")
    print(response_data.decode(errors='ignore'))

    secure_socket.close()

if __name__ == "__main__":
    main()
