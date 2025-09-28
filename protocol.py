def send(sock, data):
    size = str(len(data)).zfill(10)
    sock.sendall(size.encode())
    sock.sendall(data)


def reciveN(sock, n):
    data = b""
    while len(data) < n:
        datapart = sock.recv(n - len(data))
        if not datapart:
            return None
        data += datapart
    return data


def recv(sock):
    temporary = reciveN(sock, 10)
    if not temporary:
        return None
    try:
        first_recv = temporary.decode()
    except:
        sock.send(b"Invalid data in recv, first_recv  could not be decoded")
        return None
    if len(first_recv) == 0:
        sock.send(b"Invalid protocol in recv, first_recv (size of socket sent) is 0")
        return None
    if not first_recv.isdigit():
        sock.send(b"Invalid protocol in recv, first_recv (size of socket sent) is not an integer")
        return None
    size = int(first_recv)
    data = b""
    while len(data) < size:
        data += sock.recv(min(1024, size - len(data)))
    if not data.decode():
        sock.send(b"Invalid data in recv, data is empty")
        return None
    return data.decode()
