import socket
import select
import sys

SERVER = "127.0.0.1"
PORT = 9897
BUFF_SIZE = 1024

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))

    name = input("Введите ваше имя: ")
    client.send(name.encode())

    while True:
        # Мониторим изменения на сокете клиента и стандартном вводе
        readable, _, _ = select.select([client, sys.stdin], [], [])

        for s in readable:
            if s == client:
                # Если сокет готов к чтению, это сообщение от сервера
                message = s.recv(BUFF_SIZE).decode()
                if not message:
                    # Если сервер закрыл соединение
                    print("Соединение с сервером потеряно.")
                    sys.exit(0)
                print(message)
            else:
                # Иначе это ввод пользователя
                msg = input()
                client.send(msg.encode())


if __name__ == "__main__":
    main()
