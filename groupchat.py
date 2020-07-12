import struct
from socket import *
from _thread import start_new_thread
import pickle
import sys
import time

host = gethostbyname(gethostname())
port = 54302
sock = socket(AF_INET, SOCK_STREAM)
sock.bind((host, port))
sock.listen(10)
user = input("Enter username:")
count = 0

ip2 = ["192.168.2.101"]
otheruser = []
thread = True


class exec_message:
    msg = ""

    def __init__(self, msg):
        self.msg = msg


class join:
    name = ""

    def __init__(self, name):
        self.name = name


class Buddy:
    def __init__(self, name, conn, addr):
        self.name = name
        self.conn = conn
        self.addr = addr

    def __eq__(self, other):
        """Override the default Equals behavior"""
        return self.name == other.name and self.addr == other.addr


def user_join(name, conn, addr):
    i = Buddy(name, conn, addr)
    if i not in otheruser:
        otheruser.append(i)
        packet = pickle.dumps(join(user))
        length = struct.pack('!I', len(packet))
        packet = length + packet
        conn.send(packet)
    print(str(i.name) + " verbunden")


def user_message(msg, conn):
    name = ""
    for i in otheruser:
        if i.conn == conn:
            name = i.name
    print(str(name) + ": " + str(msg))


def user_exit(conn):
    i = 0
    for b in otheruser:
        if b.conn == conn:
            b.conn.close()
            del otheruser[i]
            break
        i += 1


def listen():
    while thread:
        (conn, addr) = sock.accept()
        start_new_thread(handle_connection, (conn, addr))
    sock.close()


def handle_connection(conn, addr):
    while thread:
        buf = b''
        while len(buf) < 4:
            try:
                time.sleep(1)
                buf += conn.recv(4 - len(buf))
            except WindowsError:
                pass
        length = struct.unpack('!I', buf)[0]

        text = conn.recv(length)

        text = pickle.loads(text)
        if type(text) is join:
            user_join(text.name, conn, addr)
        elif type(text) is exit:
            user_exit(conn)
        elif type(text) is exec_message:
            user_message(text.msg, conn)
        else:
            print(text)


def connect_port():
    try:
        for ip in ip2:
            scan_sock = socket(AF_INET, SOCK_STREAM)
            result = scan_sock.connect_ex((ip, port))
            if result == 0:
                print("verbunden mit: " + str(ip))
                send_join(join(user), (ip, port))
            scan_sock.close()

    except error:
        print("Verbindung zu Server konnte nicht aufgebaut werden")
        sys.exit()


def send_join(packet, addr):
    sock_remote = socket(AF_INET, SOCK_STREAM)
    packet = pickle.dumps(packet)
    length = struct.pack('!I', len(packet))
    packet = length + packet
    sock_remote.connect(addr)
    i = Buddy(user, sock_remote, addr)
    if i not in otheruser:
        sock_remote.send(packet)
        buf = b''
        while len(buf) < 4:
            try:
                time.sleep(0.2)
                buf += sock_remote.recv(4 - len(buf))
            except WindowsError:
                pass
        length = struct.unpack('!I', buf)[0]

        text = sock_remote.recv(length)

        text = pickle.loads(text)

        if type(text) is join:
            i = Buddy(text.name, sock_remote, addr)
            otheruser.append(i)


def send(packet, conn):
    packet = pickle.dumps(packet)
    length = struct.pack('!I', len(packet))
    packet = length + packet
    conn.send(packet)


start_new_thread(listen, ())

while True:
    count += 1
    if (count < 2):
        command = input("type h for help")
    else:
        command = input()
    if command == "h":
        print("s - Verbinden")
        print("l - andere User anzeigen")
        print("m - Nachricht senden")
        print("g - Nachricht an alle senden")
        print("q - Programm beenden")
    elif command == "s":
        connect_port()
    elif command == "l":
        for b in otheruser:
            if (b.name != user):
                print(str(b.name) + " ist verbunden über: " + str(b.addr) + "")
    elif command == "m":
        receiver = input("An wenn willst du eine Nachricht senden?")
        for b in otheruser:
            if receiver == b.name:
                msg = input("Nachricht:")
                send(exec_message(msg), b.conn)
                break
    elif command == "g":
        print("Nachricht an alle Senden")
        msg = input("Nachricht:")
        for b in otheruser:
            send(exec_message(msg), b.conn)
    elif command == "q":
        for b in otheruser:
            send(user + " hat den Chat verlassen", b.conn)
            b.conn.close()

        thread = False
        break
