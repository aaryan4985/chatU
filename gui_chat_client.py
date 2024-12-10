import socket
import threading
import tkinter as tk
from tkinter import messagebox

class ChatClient:
    def __init__(self, master):
        self.master = master
        self.master.title("ChatU")
        
        self.chat_history = None  # Placeholder for chat history widget
        self.client_socket = None
        
        # Connect to the server
        self.connect_to_server()

        # Set up the GUI
        self.setup_gui()

        # Start the thread to receive messages
        self.start_receive_thread()

        # Handle window close
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    def connect_to_server(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect(("localhost", 12345))  # Change the host and port if needed
        except ConnectionError:
            messagebox.showerror("Connection Error", "Unable to connect to the server.")
            self.master.destroy()

    def setup_gui(self):
        self.chat_frame = tk.Frame(self.master)
        self.chat_frame.pack(pady=10, padx=10)

        # Chat history
        self.chat_history = tk.Text(self.chat_frame, width=50, height=20, state="disabled", wrap="word")
        self.chat_history.grid(row=0, column=0, padx=10, pady=10)

        # Input field
        self.message_entry = tk.Entry(self.chat_frame, width=40)
        self.message_entry.grid(row=1, column=0, padx=10, pady=10)

        # Send button
        self.send_button = tk.Button(self.chat_frame, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=5, pady=5)

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
        message = self.message_entry.get().strip()
        if message:  # Check if the message is not empty
            self.client_socket.send(message.encode())  # Send the message to the server
            self.update_chat_history(f"You: {message}")  # Display sent message
            if message.lower() == "exit":
                self.master.destroy()
        self.message_entry.delete(0, tk.END)  # Clear the input field

    def update_chat_history(self, message):
        if self.chat_history:  # Ensure chat_history is initialized
            self.chat_history.config(state="normal")
            self.chat_history.insert("end", message + "\n")
            self.chat_history.config(state="disabled")
            self.chat_history.see("end")

    def on_close(self):
        try:
            self.client_socket.send("exit".encode())
        except:
            pass
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()
