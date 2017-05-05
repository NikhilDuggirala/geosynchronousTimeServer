import pickle
from GPS import *
from datetime import datetime
import asyncore
import socket
from random import randint
import time

p=randint(200,8000)
print "TO CHANGE THE GPS COM PORT MODIFY 'gps.txt' file"

#CLIENT THEARD MODULE                                     
def client(conn,msg,s):
   if(s=='FAILURE'):
      conn.send('f')
      conn.send('Device ERROR Try After Sometime........')
      conn.close()
   else:
      conn.send('s')
      pList=pickle.dumps(msg)                                                                   #SERIALIZE THE TIME DATA
      conn.send(pList)                                                                          #SEND THE SERIALIZED TIME DATA                                                #SEND THE SECONDARY DATA
      conn.close()  

class Server(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.port=port;
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        print "Server is Starting........." 

    def handle_accept(self):
        try:
            pair=self.accept()
            if pair is not None:
                c, addr = pair
                if(self.port==8000):
                    print 'Sending Telemetry:8000'
                    c.send(str(p))
                    c.close()
                else:
                    fobj=open("clients_Logs.txt",'a');                                                        #OPEN A CLIENT LOG FILE IN APPENDING MODE
                    info="Got Connection from " + str(addr)+" at "+str(datetime.now())
                    config=read_config()
                    #msg=gps_time(config[0],config[1])
                    msg=[11,12,3,31,23,59,59,00]
                    if (len(msg)==0):
                       status='FAILURE'
                       print 'Device ERROR!!!'
                       client(c,msg,status)
                    else:
                       status='SUCCESS'
                       print 'Sending Date-Time Data'
                       client(c,msg,status)
                    fobj.write(info + ' ' +status+ '\n')                                                      #WRITE THE STATUS TO THE FILE
                    fobj.close()
                    c.close()
        except socket.error as e:
            print str(e)

    def handle_close(self):
        self.close()


server_1 = Server('', 8000)
server_2 = Server('', p)
asyncore.loop()
