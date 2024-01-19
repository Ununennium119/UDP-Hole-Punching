import socket
import sys
import threading


class Client:
    BUFFER_SIZE: int = 1024

    def __init__(
            self,
            host: str,
            port: int,
            stun_host: str,
            stun_port: int,
            self_id: int,
            dest_id: int,
            dest_port: int
    ):
        self.address: tuple[str, int] = (host, port)
        self.stun_address: tuple[str, int] = (stun_host, stun_port)
        self.self_id: int = self_id
        self.dest_id: int = dest_id
        self.dest_port: int = dest_port
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def run(self):
        self.socket.bind(self.address)

        try:
            print('Sending request to stun server')
            send_data = bytearray()
            send_data.extend(self.self_id.to_bytes(4, 'big'))
            send_data.extend(self.dest_id.to_bytes(4, 'big'))
            self.socket.sendto(send_data, self.stun_address)

            print('Waiting for response from stun server...')
            receive_data, address = self.socket.recvfrom(self.BUFFER_SIZE)
            dest_ip = receive_data.decode()

            self.socket.sendto("", (dest_ip, self.dest_port))

            send_message_thread = threading.Thread(target=self.send_message, args=dest_ip)
            listen_message_thread = threading.Thread(target=self.listen_message)
            send_message_thread.start()
            listen_message_thread.start()
            send_message_thread.join()
            listen_message_thread.join()
        except Exception as e:
            print(e)

        self.socket.close()

    def send_message(self, dest_ip: str):
        while True:
            message = input('Enter message: \n')
            self.socket.sendto(message, (dest_ip, self.dest_port))

    def listen_message(self):
        while True:
            data, address = self.socket.recvfrom(self.BUFFER_SIZE)
            print(f'Received data {data} from address {address}')


def main():
    port = int(sys.argv[1])
    stun_host = sys.argv[2]
    stun_port = int(sys.argv[3])
    self_id = int(sys.argv[4])
    dest_id = int(sys.argv[5])
    dest_port = int(sys.argv[6])
    client = Client('localhost', port, stun_host, stun_port, self_id, dest_id, dest_port)
    client.run()


if __name__ == '__main__':
    main()
