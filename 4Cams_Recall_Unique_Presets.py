import socket

IPADDR1 = '192.168.10.97'

PORTNUM = 1259
COMMAND1 = '8101040737FF'


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

s.connect((IPADDR1, PORTNUM))

data = bytes.fromhex(COMMAND1)

s.send(data)

s.close()


