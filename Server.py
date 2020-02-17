"""
This is a basic Server-Client chat.
* Uses sockets
* Uses UDP protocol
* Uses threads to receive messages
* Saves the chat history in txt fine after shutting down the server
"""

import socket
import time

host = '127.0.0.1'
port = 11029

# server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_socket.bind((host, port))

shutdown = False
client_list = []
print('--Server Started--')


def main():
    global shutdown
    while not shutdown:
        try:
            data, addr = server_socket.recvfrom(1024)
            if addr not in client_list:
                client_list.append(addr)
            cur_time = time.strftime('%Y, %m, %d - %H.%M.%S', time.localtime())
            with open('chathistory.txt', 'at') as f:
                f.write(f'{addr[0]}: {addr[1]} - {cur_time}  :: {data.decode("utf-8")} \n')
            # print(f'{addr[0]}: {addr[1]} - {cur_time}  ::', end='')
            # print(data.decode('utf-8'))
            for client in client_list:
                if addr != client:
                    server_socket.sendto(data, client)
        except OSError:
            print('--Server stopped--')
            shutdown = True
    server_socket.close()


if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    main()
