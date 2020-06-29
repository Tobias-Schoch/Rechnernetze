from socket import *
import base64

nachricht = input("Email Text")
absender = "MAIL FROM:<" + input("Absender") + ">\r\n"
empfaenger = "RCPT TO:<" + input("Empfänger") + ">\r\n"
betreff = "Subject: " + input("Betreff") + "\r\n\r\n"
ende = "\r\n.\r\n"

username = "rnetin"
password = "ntsmobil"

mailserver = ("asmtp.htwg-konstanz.de", 25)
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailserver)
recv = clientSocket.recv(1024)
recv = recv.decode()

EHLO = 'EHLO Luca\r\n'
clientSocket.send(EHLO.encode())
one = clientSocket.recv(1024)
one = one.decode()

bstr = ("\x00" + username + "\x00" + password).encode()
bstr = base64.b64encode(bstr)
authMsg = "AUTH PLAIN ".encode() + bstr + "\r\n".encode()
clientSocket.send(authMsg)
recv_auth = clientSocket.recv(1024)

clientSocket.send(absender.encode())
two = clientSocket.recv(1024)
two = two.decode()

clientSocket.send(empfaenger.encode())
three = clientSocket.recv(1024)
three = three.decode()

data = "DATA\r\n"
clientSocket.send(data.encode())
four = clientSocket.recv(1024)
four = four.decode()

clientSocket.send(betreff.encode())
clientSocket.send(nachricht.encode())
clientSocket.send(ende.encode())
recv_msg = clientSocket.recv(1024)

end = "QUIT\r\n"
clientSocket.send(end.encode())
recv5 = clientSocket.recv(1024)
clientSocket.close()
