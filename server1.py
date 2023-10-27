import socket
import select
from dadata import Dadata

token = "ваш token"
secret = "ваш secret"

SERVER = "0.0.0.0"
PORT = 9897
clients = {}
BUFF_SIZE = 1024


def dadata_lookup(ip_address):
    with Dadata(token, secret) as dadata:
        response = dadata.iplocate(ip_address)
    try:
        location = response.get('data')
        country = location.get('country')
        region_type = location.get('federal_district')
        region = location.get('region')
        city = location.get('city')

        return f"{country}, {region_type}, {region}, {city}"
    except:
        return "Ошибка при определении города по IP."


def broadcast(message):
    for client in clients:
        client.send(message.encode())


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER, PORT))
    server.listen(5)
    print(f"Сервер запущен на {SERVER}:{PORT}")

    inputs = [server]

    while True:
        readable, _, _ = select.select(inputs, [], [])
        for s in readable:
            if s is server:
                client, addr = server.accept()
                name = client.recv(BUFF_SIZE).decode()
                clients[client] = name
                broadcast(f"{name} присоединился к чату!")
                inputs.append(client)
            else:
                try:
                    msg = s.recv(BUFF_SIZE).decode()
                    if not msg:
                        raise Exception
                    if msg.startswith("Вычисли его по ip "):
                        ip_address = msg.split(" ")[-1]
                        broadcast("IP-бот: Вычисляю…")
                        result = dadata_lookup(ip_address)
                        broadcast(f"IP-бот: {result}")
                    else:
                        broadcast(f"{clients[s]}: {msg}")
                except:
                    # Клиент отключился
                    broadcast(f"{clients[s]} покинул чат.")
                    inputs.remove(s)
                    del clients[s]


if __name__ == "__main__":
    main()
