import socket
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("Chat Application")
        
        # Login/Register
        self.username = None
        self.client_socket = None
        self.connect_to_server()

        # Chat window
        self.chat_frame = tk.Frame(self.master)
        self.chat_frame.pack(pady=10, padx=10)

        # Initialize chat history
        self.chat_history = tk.Text(self.chat_frame, width=50, height=20, state="disabled", wrap="word")
        self.chat_history.grid(row=0, column=0, padx=10, pady=10)
        
        self.message_entry = tk.Entry(self.chat_frame, width=40)
        self.message_entry.grid(row=1, column=0, padx=10, pady=10)
        
        self.send_button = tk.Button(self.chat_frame, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=5, pady=5)

        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    def connect_to_server(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect(("localhost", 12345))
            self.start_receive_thread()
            self.show_login_register()
        except ConnectionError:
            messagebox.showerror("Connection Error", "Unable to connect to the server.")
            self.master.destroy()

    def show_login_register(self):
        choice = simpledialog.askstring("Authentication", "Do you want to (1) Login or (2) Register?")
        if choice not in ("1", "2"):
            messagebox.showwarning("Invalid Choice", "Please enter 1 or 2.")
            self.show_login_register()
            return
        
        if choice == "1":
            self.username = simpledialog.askstring("Login", "Enter your username:")
            password = simpledialog.askstring("Login", "Enter your password:", show="*")
            self.client_socket.send(choice.encode())
            self.client_socket.send(self.username.encode())
            self.client_socket.send(password.encode())
        else:
            self.username = simpledialog.askstring("Register", "Enter your desired username:")
            password = simpledialog.askstring("Register", "Enter your desired password:", show="*")
            self.client_socket.send(choice.encode())
            self.client_socket.send(self.username.encode())
            self.client_socket.send(password.encode())
        
        response = self.client_socket.recv(1024).decode()
        if "successful" not in response.lower():
            messagebox.showerror("Error", response)
            self.show_login_register()

    def start_receive_thread(self):
        thread = threading.Thread(target=self.receive_messages)
        thread.daemon = True
        thread.start()

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if message:
                    self.update_chat_history(message)
            except ConnectionError:
                self.update_chat_history("Disconnected from the server.")
                break

    def send_message(self):
        message = self.message_entry.get()
        if message.strip():
            self.client_socket.send(message.encode())
            if message.lower() == "exit":
                self.master.destroy()
        self.message_entry.delete(0, tk.END)

    def update_chat_history(self, message):
        self.chat_history.config(state="normal")
        self.chat_history.insert("end", message + "\n")
        self.chat_history.config(state="disabled")
        self.chat_history.see("end")

    def on_close(self):
        self.client_socket.send("exit".encode())
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()
