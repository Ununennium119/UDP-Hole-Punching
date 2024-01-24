import socket
import sys


class StunServer:
    BUFFER_SIZE: int = 1024

    def __init__(self, host: str, port: int):
        self.address: tuple[str, int] = host, port
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ids_map: dict[int, int] = {}
        self.id_address_map: dict[int, tuple[str, int]] = {}

    def run(self):
        self.socket.bind(self.address)

        while True:
            try:
                print(f'--------------------------------------------------------------------------------')
                print('Waiting for a request... ')
                data, address = self.socket.recvfrom(self.BUFFER_SIZE)
                source_id, dest_id = int.from_bytes(data[0:4], 'big'), int.from_bytes(data[4:8], 'big')
                print(f'Received source id: {source_id} and dest id: {dest_id} from address: {address}')

                self.id_address_map[source_id] = address
                if self.ids_map.get(dest_id) == source_id:
                    print(f'Sending ips to ids {source_id} and {dest_id}')
                    self.socket.sendto(
                        f'{self.id_address_map[dest_id][0]}|{self.id_address_map[dest_id][1]}'.encode(),
                        self.id_address_map[source_id]
                    )
                    self.socket.sendto(
                        f'{self.id_address_map[source_id][0]}|{self.id_address_map[source_id][1]}'.encode(),
                        self.id_address_map[dest_id]
                    )
                    self.ids_map.pop(dest_id)
                else:
                    print(f'Saving source id: {source_id} and dest id: {dest_id}')
                    self.ids_map[source_id] = dest_id
            except Exception as e:
                print(e)
                break

        self.socket.close()


def main():
    port = int(sys.argv[1])
    stun_server = StunServer('0.0.0.0', port)
    stun_server.run()


if __name__ == '__main__':
    main()
