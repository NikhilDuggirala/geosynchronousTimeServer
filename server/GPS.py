import serial
import time

def read_config():                             # function to read from config file
    file_object = open("gps.txt","r")          # open config file
    out_my = file_object.readline()
    my_com = out_my.split('=',1)
    com_get = my_com[1]
    com_value = com_get.split('\n' ,1)
    com_val=com_value[0]                        #get com port , baud rate , display options , mode and sleep interval
    out_my = file_object.readline()
    my_baud= out_my.split('=',1)
    baud_val=my_baud[1].split('\n',1)
    file_object.close()
    config = [com_val,baud_val[0]]
    return(config)

def gps_time(com,baud):
    serialData = serial.Serial(com,baud,timeout=1)
    l=[]
    while True:
        my_str= serialData.readline()
        my_weekday = int(time.strftime("%w"))
        if (my_str[:6] == '$GPRMC'):                    
            my_list = my_str.split(',',10)
            y = my_list[9]
            x = my_list[1]
            z= my_list[2]
            my_hour = int(x[:2])
            my_minutes = int( x[2:4])
            my_seconds = int( x[4:6])
            my_day = int(y[:2])
            my_month = int( y[2:4])
            my_year = int( y[4:6])
            if(my_list[2] =='V'):
                break;
            else:
                l=[my_year,my_month,my_weekday,my_day,my_hour,my_minutes,my_seconds,00]
                break
    serialData.close()
    return l
    
