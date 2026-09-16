import struct

MAX_MESSAGE_SIZE = 10 * 1024 * 1024


def recv_exact(sock, size):
    data = bytearray()

    while len(data) < size:
        chunk = sock.recv(size - len(data))

        if chunk == b"":
            raise ConnectionError("Connection closed")

        data.extend(chunk)

    return bytes(data)


def send_message(sock, command: str, payload: bytes):
    if len(command) > 4:
        raise ValueError("Command must contain максимум 4 символа")

    cmd = command.encode("ascii").ljust(4, b"\x00")
    header = cmd + struct.pack("!I", len(payload))

    sock.sendall(header + payload)


def recv_message(sock):
    first = sock.recv(1)

    if first == b"":
        return None

    cmd = first + recv_exact(sock, 3)
    length = struct.unpack("!I", recv_exact(sock, 4))[0]

    if length > MAX_MESSAGE_SIZE:
        raise ConnectionError("Message too large")

    payload = recv_exact(sock, length)

    command = cmd.rstrip(b"\x00").decode("ascii")

    return command, payload