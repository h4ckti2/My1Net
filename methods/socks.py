import socket

host = socket.gethostbyname(input("Host: "))
port = int(input("Port: "))
byte_s = int(input("Bytes: "))


def send_tcp_request(sockets, data):
    # Iterate through the list of sockets and send the request to each one
    for sock in sockets:
        try:
            sock.sendall(data)
            response = sock.recv(1024)
            print(f"Response from {sock.getpeername()}: {response}")
        except Exception as e:
            print(f"Failed to send/receive data to/from {sock.getpeername()}: {e}")


# Create a list of sockets
sockets = []
for i in range(byte_s):
    # Create a socket and connect to the server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sockets.append(sock)

# Example usage
send_tcp_request(sockets, f"GET / HTTP/1.1\r\nHost: {host}\r\n\r\n".encode())

# Close the sockets
for sock in sockets:
    sock.close()
