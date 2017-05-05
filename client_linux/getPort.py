import socket
def por():
    socks=socket.socket(socket.AF_INET,socket.SOCK_STREAM)                                                                          #OPEN A SOCKET FOR TCP CONNECTION IN IPv4
    host=raw_input('Enter the Server ip: ')                                                                                         #GET THE SERVER IP FROM THE USER
    socks.connect((host,8000))
    port=socks.recv(1024)
    socks.close()
    return port,host
