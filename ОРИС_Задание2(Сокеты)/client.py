import socket
import threading

from protocol import send_message, recv_message

HOST = "127.0.0.1"
PORT = 9000

stop = threading.Event()


def receiver(sock):
    while not stop.is_set():
        try:
            msg = recv_message(sock)

            if msg is None:
                print("\nServer closed connection")
                stop.set()
                break

            command, payload = msg
            text = payload.decode()

            if command == "TEXT":
                print(f"\n{text}")

            elif command == "LIST":
                print("\nUsers:")
                if text:
                    for name in text.splitlines():
                        print("-", name)
                else:
                    print("No users")

            elif command == "ERR":
                print(f"\nError: {text}")

            print("> ", end="", flush=True)

        except ConnectionResetError:
            print("\nConnection reset by server")
            stop.set()

        except ConnectionError:
            print("\nConnection lost")
            stop.set()

        except OSError:
            stop.set()


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    name = input("Username: ").strip()

    if not name:
        print("Empty username")
        return

    send_message(sock, "JOIN", name.encode())

    threading.Thread(target=receiver, args=(sock,), daemon=True).start()

    print("Commands:")
    print("/list - users")
    print("/quit - exit")

    try:
        while not stop.is_set():
            line = input("> ")

            if line == "/quit":
                send_message(sock, "QUIT", b"")
                break

            elif line == "/list":
                send_message(sock, "LIST", b"")

            elif line:
                send_message(sock, "TEXT", line.encode())

    except BrokenPipeError:
        print("Broken pipe")

    except ConnectionResetError:
        print("Server disconnected")

    finally:
        stop.set()
        sock.close()


if __name__ == "__main__":
    main()