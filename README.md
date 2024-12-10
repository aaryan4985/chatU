# chatU

**chatU** is a simple graphical user interface (GUI) chat application built using Python and Tkinter. It enables real-time messaging between multiple clients connected to a server, making it an excellent starting point for understanding networking and GUI programming in Python.

---

## Features

- **Real-Time Messaging**: Seamlessly exchange messages with multiple clients in real-time.
- **User-Friendly Interface**: A clean and simple GUI built using Tkinter.
- **Multi-Client Support**: Connect multiple clients to the server simultaneously.
- **Message Feedback**: Sent and received messages are displayed in the chat window.
- **Customizable**: Easy to extend and modify for additional features.

---

## How It Works

### Server-Client Architecture
- A central **server** handles connections and message broadcasting to all connected clients.
- Each **client** connects to the server, enabling real-time communication.

---

## Prerequisites

- Python 3.10 or later installed on your system.
- Basic understanding of Python programming.

---

## Installation and Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/chatU.git
cd chatU
```

### Step 2: Start the Server
Run the following command to start the server:
```bash
python server.py
```

### Step 3: Start the Client
Run the following command to start a client:
```bash
python gui_chat_client.py
```
Repeat this step for additional clients.

---

## Usage

1. **Launch the Server**: Start the `server.py` script.
2. **Launch the Clients**: Open multiple instances of the `gui_chat_client.py` script.
3. **Chat**: Type your messages in the input field and click "Send" to communicate.

---

## File Structure

```
chatU/
├── auth_chatroom_server.py            # Server-side script
├── gui_chat_client.py   # GUI-based client-side script
├── README.md            # Project documentation
```

---

## Enhancements

Consider adding the following features to expand the functionality of chatU:
- **User Authentication**: Add login/signup functionality.
- **Message Encryption**: Implement encryption for secure communication.
- **Media Support**: Allow sending of images, files, or other media.
- **Custom Themes**: Add options for light/dark mode or theme customization.

---

## Technologies Used

- **Python**: Programming language for server and client logic.
- **Tkinter**: GUI library for creating the client interface.
- **Socket Programming**: For handling server-client communication.

---

## Contributing

Contributions are welcome! If you have ideas or want to improve the project:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "Add feature"`).
4. Push the branch (`git push origin feature-name`).
5. Open a Pull Request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

Inspired by the simplicity of Python's socket programming and Tkinter's GUI capabilities.

--- 

Feel free to modify this **README.md** to include your personal GitHub link or any additional information!
