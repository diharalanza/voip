import socket
import pyaudio

CHUNK_SIZE = 1024  # bytes
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100  # Hz
RECORD_SECONDS = 10

def start_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Get local machine name and a random port
    host = socket.gethostname()
    port = 12345

    # Bind the socket to a specific address and port
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(1)
    print(f"Server started and listening on {host}:{port}")

    # Accept a connection from a client
    client_socket, address = server_socket.accept()
    print(f"Connection established from {address[0]}:{address[1]}")

    # Create an instance of PyAudio
    audio = pyaudio.PyAudio()

    # Open a new stream for the client
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        output=True,
                        frames_per_buffer=CHUNK_SIZE)

    # Receive audio data from the client and play it
    while True:
        data = client_socket.recv(CHUNK_SIZE)
        if not data:
            break
        stream.write(data)

    # Clean up resources
    stream.stop_stream()
    stream.close()
    audio.terminate()
    client_socket.close()
    server_socket.close()
    print("Server shut down successfully.")

if __name__ == '__main__':
    start_server()
