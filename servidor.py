import socket
import threading
import os
def Handler(name, sock,line):
    opcion = sock.recv(1024)[1:]
    print(opcion)
    if opcion==b'1':
        SearchFile(name,sock)
    if opcion==b'2':
        CreateFile(name,sock)
    if opcion==b'3':
        RetrFile(name,sock)
def RetrFile(name, sock,line):
    sock.send(b"ingrese el nombre del archivo")
    filename = sock.recv(1024).decode('utf-8')
    print(filename)
    path = line[2]
    paso=False
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(filename):
                paso=True
    if paso:
        sock.send(bytes("EXIST" + str(os.path.getsize(filename)),'utf-8'))
        userResponse = sock.recv(1024)
        if userResponse==b'OK':
            with open(str(filename), 'rb') as f:
                bytesToSend = f.read(1024)
                sock.send(bytesToSend)
                while bytesToSend != "":
                    bytesToSend = f.read(1024)
                    sock.send(bytesToSend)

    else:
        sock.send(b"ERR")

    sock.close()

def CreateFile(name, sock,line):
    filename = sock.recv(1024).decode("utf-8")
    path = line[2]
    paso = False
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(filename):
                paso = True
    if paso:
        sock.send(bytes("Ya existe un archivo con este nombre","utf-8"))
    else:
        sock.send(b"ok")
        f = open('new_' + filename, 'wb')
        filesize = int(sock.recv(1024).decode("utf-8"))
        sock.send(b"nice")
        data=sock.recv(1024)
        totalRecv = len(data)
        f.write(data)
        while totalRecv < filesize:
            print(3)
            print(1)
            data = sock.recv(1024)
            totalRecv += len(data)
            f.write(data)

        sock.send(b"Download Complete")
        f.close()


def SearchFile(name, sock, line):
    filename = sock.recv(1024).decode("utf-8")
    path = line[2]
    paso = False
    coso=""
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(filename):

                coso+="- "+ str(os.path.join(file))
                sock.send(bytes(paso),"utf-8")

def Main():
    file=open("Configuracion.txt",'r')
    line=file.read().split(",")
    file.close()
    host = line[0]
    print(host)
    port = int(line[1])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host,port))

    s.listen(5)

    print("server Started")
    while True:
        c, addr = s.accept()
        print("client connected ip: "+str(addr))
        t= threading.Thread(target=Handler, args=(addr,c,line))
        t.start()
if __name__=="__main__":
    Main()