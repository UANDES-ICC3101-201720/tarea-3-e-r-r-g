import socket
import os
def Main():
    host = socket.gethostname()
    port = 5000

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((host, port))
    while True:
        opcion = input("\t1. Search file\n\t2. Upload file\n\t3. Download file")
        while opcion not in ['0', '1', '2', '3']:
            opcion = input("\t1. Search file\n\t2. Upload file\n\t3. Download file")
        if opcion == '3':
            s.send(b'\x11' + bytes(opcion, "utf-8"))
            data =s.recv(1024)
            print(str(data))
            filename=input("filename: ")
            s.send(bytes(filename,'utf-8'))
            data =s.recv(1024).decode("utf-8")
            print(data)
            if data[:5]=="EXIST":
                filesize= int(data[5:])
                message = input("File Exists, "+str(filesize) + "Bytes, download? (Y,N)?:")
                if message == "Y":
                    s.send(b'OK')
                    f= open('new_'+filename, 'wb')
                    data = s.recv(1024)
                    totalRecv = len(data)
                    f.write(data)

                    while totalRecv < filesize:
                        data = s.recv(1024)
                        totalRecv += len(data)
                        f.write(data)
                        print("{0:.2f}".format((totalRecv/float(filesize))*100)+"% Done")

                    print("Download Complete")
                    f.close()
            else:
                print("File does not exist")

        if opcion=='2':
            s.send(b'\x11' + bytes(opcion, "utf-8"))
            filename = input("filename: ")
            if not os.path.isfile((filename)):
                print("File does not exist")
                continue
            s.send(bytes(filename, 'utf-8'))
            data = s.recv(1024).decode("utf-8")
            if data=="Ya existe un archivo con este nombre":
                print(data)
                continue
            s.send(bytes(str(os.path.getsize(filename)), 'utf-8'))
            data = s.recv(1024).decode("utf-8")
            if data=='nice':
                with open(str(filename), 'rb') as f:
                    bytesToSend = f.read(1024)
                    s.send(bytesToSend)
                    while bytesToSend != b"":
                        bytesToSend = f.read(1024)
                        s.send(bytesToSend)
            data=s.recv(1024).decode("utf-8")
            print(data)

        if opcion==3:
            s.send(b'\x11' + bytes(opcion, "utf-8"))
            for file in os.listdir("/mydir"):
                    print(os.path.join("/mydir", file))



if __name__ == "__main__":
    Main()