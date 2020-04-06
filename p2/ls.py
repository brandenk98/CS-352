# Michael Rizzo
# Branden Kushnir
# Load-Balancing Server for Project 2
import sys
import socket as mysoc

def newSocket():
    try: 
        ret_socket = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print ("[LS]: Server socket created")
    except mysoc.error as err: 
        print ("[LS]: Could not create socket \n Error: " + str(err))
    return ret_socket

def argCheck(size, expected):
    if size is not expected:
        raise TypeError("Expected %d arguments, got %d" % (expected, size))
        exit()

def ls():
    argCheck(len(sys.argv), 6)

    lsSocket = newSocket()
    ts1Socket = newSocket()
    ts2Socket = newSocket()

    lsBind = ("", int(sys.argv[1])) 
    ts1Bind = (str(sys.argv[2]),int(sys.argv[3]))
    ts2Bind = (str(sys.argv[4]),int(sys.argv[5]))
    
    lsSocket.bind(lsBind)
    ts1Socket.connect(ts1Bind)
    ts2Socket.connect(ts2Bind)

    lsSocket.listen(5)
    ts1Socket.settimeout(5)
    ts2Socket.settimeout(5)

    clientSocket, addr = lsSocket.accept()
    print('[LS}: Got a connection request from: ' , addr)

    while True:
        data = clientSocket.recv(4096).decode("utf-8").strip()
        if not data:
            break
        print("[LS]: Received from Client: " + data)

        ts1Socket.send(data.encode("utf-8"))
        ts2Socket.send(data.encode("utf-8"))

        try:
            ts1Data = ts1Socket.recv(4096).decode("utf-8")
            print("[LS]: Data from [TS1]: " + ts1Data)
            clientSocket.send(ts1Data.encode('utf-8'))
        except mysoc.timeout:
            print("[LS]: No response from [TS1]")
            try:
                ts2Data = ts2Socket.recv(4096).decode("utf-8")
                print("[LS]: Data from [TS2]: " + ts2Data)
                clientSocket.send(ts2Data.encode("utf-8"))
            except mysoc.timeout:
                print("[LS]: No response from [TS2]")
                err_str = data + " - Error:HOST NOT FOUND"
                clientSocket.send(err_str.encode("utf-8"))

    lsSocket.close()
    ts1Socket.close()
    ts2Socket.close()
    exit()

ls()