import socket
import threading
import redis


r = redis.Redis(host='localhost', port=6379, db=0)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 12345))
server_socket.listen(5)

clients = []

def handle_client(client_socket, address):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(f"Received message from {address}: {message}")
                r.rpush('chat_messages', message)
                broadcast(message, client_socket)
        except:
            clients.remove(client_socket)
            client_socket.close()
            break

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                clients.remove(client)
                client.close()

def start_server():
    print("Server is listening on port 12345...")
    while True:
        client_socket, address = server_socket.accept()
        clients.append(client_socket)
        print(f"Accepted connection from {address}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, address))
        client_handler.start()

if __name__ == "__main__":
    start_server()
