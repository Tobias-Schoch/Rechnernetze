# This script runs on Python 3
import socket, threading


def TCP_connect(ip, port_number, delay, output):
    TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPsock.settimeout(delay)
    try:
        TCPsock.connect((ip, port_number))
        output[port_number] = 'Listening'
    except:
        output[port_number] = ''

def UDP_connect(ip, port_number, delay, output):
    UDPsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDPsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    UDPsock.settimeout(delay)
    try:
        UDPsock.connect((ip, port_number))
        output[port_number] = 'Listening'
    except:
        output[port_number] = ''


def scan_ports(host_ip, delay):

    threads = []
    output = {}

    for i in range(50):
        t = threading.Thread(target=UDP_connect, args=(host_ip, i, delay, output))
        threads.append(t)

    for i in range(50):
        threads[i].start()

    for i in range(50):
        threads[i].join()

    for i in range(50):
        if output[i] == 'Listening':
            print(str(i) + ': ' + output[i])



def main():
    host_ip = input("Enter host IP: ")
    delay = int(input("How many seconds the socket is going to wait until timeout: "))
    scan_ports(host_ip, delay)

if __name__ == "__main__":
    main()