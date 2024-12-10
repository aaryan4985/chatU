import socket
import threading
import json
import os

# Global variables
clients = {}
chatrooms = {}
message_history = {}  # {chatroom_name: [messages]}

# File to store user credentials
USER_DATA_FILE = "users.json"

# Load user data
def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    return {}

# Save user data
def save_users(users):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(users, file)

# Function to handle authentication
def authenticate(client_socket):
    users = load_users()

    while True:
        client_socket.send("Do you want to (1) Login or (2) Register? ".encode())
        choice = client_socket.recv(1024).decode().strip()

        if choice == "1":  # Login
            client_socket.send("Enter your username: ".encode())
            username = client_socket.recv(1024).decode().strip()

            client_socket.send("Enter your password: ".encode())
            password = client_socket.recv(1024).decode().strip()

            if username in users and users[username] == password:
                client_socket.send("Login successful!".encode())
                return username
            else:
                client_socket.send("Invalid username or password. Try again.".encode())

        elif choice == "2":  # Register
            client_socket.send("Enter your desired username: ".encode())
            username = client_socket.recv(1024).decode().strip()

            if username in users:
                client_socket.send("Username already exists. Try a different one.".encode())
            else:
                client_socket.send("Enter your desired password: ".encode())
                password = client_socket.recv(1024).decode().strip()
                users[username] = password
                save_users(users)
                client_socket.send("Registration successful! You can now log in.".encode())

# Function to handle client communication
def handle_client(client_socket):
    username = authenticate(client_socket)
    clients[client_socket] = username

    client_socket.send("Enter a chatroom name to join or create: ".encode())
    chatroom_name = client_socket.recv(1024).decode().strip()

    if chatroom_name not in chatrooms:
        chatrooms[chatroom_name] = []
        message_history[chatroom_name] = []

    chatrooms[chatroom_name].append(client_socket)

    # Send message history to the client
    if message_history[chatroom_name]:
        client_socket.send("Message history:\n".encode())
        for message in message_history[chatroom_name]:
            client_socket.send(f"{message}\n".encode())

    welcome_message = f"{username} has joined the chatroom '{chatroom_name}'!"
    print(welcome_message)
    broadcast(chatroom_name, welcome_message, client_socket)

    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message.lower() == "exit":
                goodbye_message = f"{username} has left the chatroom '{chatroom_name}'."
                print(goodbye_message)
                broadcast(chatroom_name, goodbye_message, client_socket)
                break

            formatted_message = f"{username}: {message}"
            message_history[chatroom_name].append(formatted_message)  # Save to history
            broadcast(chatroom_name, formatted_message, client_socket)
        except:
            break

    chatrooms[chatroom_name].remove(client_socket)
    if not chatrooms[chatroom_name]:
        del chatrooms[chatroom_name]
        del message_history[chatroom_name]
    del clients[client_socket]
    client_socket.close()

# Function to broadcast messages in a chatroom
def broadcast(chatroom_name, message, sender_socket=None):
    for client in chatrooms.get(chatroom_name, []):
        if client != sender_socket:
            client.send(message.encode())

# Main server function
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 12345))
    server_socket.listen(5)
    print("Server is running on port 12345...")

    while True:
        client_socket, _ = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    start_server()
