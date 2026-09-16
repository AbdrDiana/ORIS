import socket
import threading

from protocol import send_message, recv_message

HOST = "127.0.0.1"
PORT = 9000

clients = {}
lock = threading.Lock()


def broadcast(text, exclude=None):
    with lock:
        sockets = list(clients.keys())

    for s in sockets:
        if s is exclude:
            continue

        try:
            send_message(s, "TEXT", text.encode())
        except (BrokenPipeError, ConnectionResetError, OSError):
            pass


def handle_client(conn, addr):
    username = None

    try:
        while True:
            msg = recv_message(conn)

            if msg is None:
                break

            command, payload = msg

            if command == "JOIN":
                name = payload.decode().strip()

                if not name:
                    send_message(conn, "ERR", b"Empty username")
                    continue

                with lock:
                    if name in clients.values():
                        send_message(conn, "ERR", b"Username already taken")
                        continue

                    clients[conn] = name

                username = name
                broadcast(f"[SERVER] {username} joined", exclude=conn)

            elif command == "TEXT":
                if username is None:
                    send_message(conn, "ERR", b"Join first")
                    continue

                text = payload.decode()
                broadcast(f"{username}: {text}", exclude=conn)

            elif command == "LIST":
                with lock:
                    names = "\n".join(clients.values())

                send_message(conn, "LIST", names.encode())

            elif command == "QUIT":
                break

            else:
                send_message(conn, "ERR", b"Unknown command")

    except ConnectionResetError:
        print(f"{addr} disconnected unexpectedly")

    except ConnectionError:
        print(f"{addr} connection lost")

    finally:
        with lock:
            if conn in clients:
                left = clients.pop(conn)
                broadcast(f"[SERVER] {left} left")

        conn.close()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server.bind((HOST, PORT))
    server.listen()

    print(f"Server started: {HOST}:{PORT}")

    try:
        while True:
            conn, addr = server.accept()
            print("Connected:", addr)

            threading.Thread(
                target=handle_client,
                args=(conn, addr),
                daemon=True
            ).start()

    except KeyboardInterrupt:
        print("Server stopped")

    finally:
        server.close()


if __name__ == "__main__":
    main()