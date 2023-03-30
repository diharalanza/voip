import socket
import pyaudio

CHUNK_SIZE = 1024  # bytes
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100  # Hz
RECORD_SECONDS = 10

def start_client():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Get the server's hostname and port
    host = socket.gethostname()
    port = 12345

    # Connect to the server
    client_socket.connect((host, port))

    # Create an instance of PyAudio
    audio = pyaudio.PyAudio()

    # Open a new stream for sending audio to the server
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK_SIZE)

    # Send audio data to the server
    while True:
        data = stream.read(CHUNK_SIZE)
        client_socket.sendall(data)

    # Clean up resources
    stream.stop_stream()
    stream.close()
    audio.terminate()
    client_socket.close()
    print("Client shut down successfully.")

if __name__ == '__main__':
    start_client()
