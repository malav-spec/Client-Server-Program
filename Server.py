import socket
from sys import argv


Pair_dict = {}

def fileToDict():
    f = open("Pairs.txt", "r")
    Lines = f.readlines()

    for line in Lines:
        line = line.strip()
        pairs = line.split(':')
        key = pairs[0]
        value = pairs[1]
        Pair_dict[key] = value

    f.close()

def checkWordInDict(Word):
    if Word in Pair_dict.keys():
        return True
    else:
        return False

fileToDict()

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ("Socket successfully created")
except socket.error as err:
    print ("socket creation failed with error %s" %(err))

port = int(argv[1])
host = socket.gethostname()
server_binding = (socket.gethostname(), port)

try:
    s.bind(server_binding)
    print("Socket bind successfull")
except socket.error as err:
    print("Socket bind fail with error %s" %(err))

s.listen(1)

csockid, addr = s.accept()
print ("[S]: Got a connection request from a client at {}".format(addr))

while True:
    data = csockid.recv(1024).decode()

    if not data:
        break

    # print("from connected user: " + str(data))

    if checkWordInDict(str(data)) is True:
        msg = Pair_dict[str(data)]
    else:
        msg = "NOT FOUND"

    csockid.send(msg.encode('utf-8'))

s.close()
