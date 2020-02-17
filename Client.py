import socket
import threading
import time

host = '127.0.0.1'
port = 0

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # This is for UDP.
client_socket.bind((host, port))
client_socket.setblocking(False)

server = ('127.0.0.1', 11029)
shutdown = False
join = False


def receive_message(thr_name, clientsocket):
    global shutdown
    while not shutdown:
        while True:   # If it wasn't for this loop, the whole message receiving is not working.
            try:
                data, addr = clientsocket.recvfrom(1024)  # recv for tcp, recvfrom for udp
                print(data.decode('utf-8'))
                time.sleep(0.2)
            except OSError:
                break


if __name__ == '__main__':
    nickname = input('Enter your nickname ->')
    rec_thread = threading.Thread(target=receive_message, args=('Recv_thread', client_socket))
    rec_thread.start()
    while not shutdown:
        if not join:
            client_socket.sendto(f'{nickname} joined the chat'.encode('utf-8'), server)
            join = True
        else:
            try:
                message = input('>>')
                if message:
                    client_socket.sendto(f'{nickname} :: {message}'.encode('utf-8'), server)
                time.sleep(0.2)
            except OSError:
                client_socket.sendto(f'{nickname} left the chat'.encode('utf-8'), server)
                shutdown = True
    rec_thread.join()
    client_socket.close()
