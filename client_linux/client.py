#! /usr/bin/env python

import sys,os
import socket
import pickle
from time import *
from datetime import *
from getPort import *
import pytz

monthDict={1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
start=2


#UTC to Local TimeZone
def utc_to_local(utc_dt,zone):
    return utc_dt.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(zone))

#TIME SETTING MODULE
def change(s,l):
    global start
    string_date=" ".join(str(x) for x in l)
    list_date=string_date.split()
    year=int(list_date[0])
    if(list_date[0]=="00"):
        start+=1
    year=(start*1000)+year
    month=int(list_date[1])
    dayOfWeek=int(list_date[2])                                                                                                #CONVERT THE TIME VARIABLE INTO INTEGER VALUE
    day=int(list_date[3])
    hour=int(list_date[4])
    minute=int(list_date[5])
    second=int(list_date[6])
    microsecond=int(list_date[7])
    user_zone='UTC'
    local_tz=utc_to_local(datetime(year,month,day,hour,minute,second,microsecond),user_zone)
    if s == 1:
        month=monthDict[local_tz.month]
        print local_tz
        os.system('date -s "'+str(local_tz.day)+" "+month+" "+str(local_tz.year)+" "+str(local_tz.hour)+":"+str(local_tz.minute)+":"+str(local_tz.second)+'"')                                      #SET THE TIME IN LINUX MACHINE
    elif s == 2:
        try:
          import win32api
          import win32security
        except ImportError as e:
          print str(e)
          sys.exit(1)
        print local_tz
        priv_flags = win32security.TOKEN_ADJUST_PRIVILEGES | win32security.TOKEN_QUERY
        hToken = win32security.OpenProcessToken (win32api.GetCurrentProcess (),ntsecuritycon.MAXIMUM_ALLOWED)
        time_privilege = win32security.LookupPrivilegeValue (None,win32security.SE_TIME_ZONE_NAME)
        win32security.AdjustTokenPrivileges (hToken, 0,[(time_privilege, win32security.SE_PRIVILEGE_ENABLED)])
        win32api.SetTimeZoneInformation((0, u'GMT Standard Time',(2000,10,5,2,0,0,0,0), 0, u'GMT Daylight Time',(2000,5,3,1,0,0,0,0),-60))
        win32api.SetSystemTime(local_tz.year, local_tz.month , dayOfWeek , local_tz.day , local_tz.hour , local_tz.minute , local_tz.second , local_tz.microsecond )                           #SET THE TIME IN WINDOWS MACHINE
    else:print 'wrong param'



#OS CHECKING MODULE
def check_os(l):                                                                                                     #OS CHECK
    if sys.platform=='linux2':
        change(1,l)
    elif  sys.platform=='win32':
        change(2,l)
    else:
        print 'unknown system.Time cannot be Set'
        print 'Exiting......'
        sys.exit(1)


#MAIN FUNCTION
        
print "Requesting GPS Data"
param_list=[];                                                                      
end_msg=''  
socks=socket.socket(socket.AF_INET,socket.SOCK_STREAM)                                                                          #OPEN A SOCKET FOR TCP CONNECTION IN IPv4
port,host=por()
port=int(port)
socks.connect((host,port))
s=socks.recv(2048)                                                                                                      #ESTABILSH CONNECTION TO THE SERVER
if(s[:1]=='s'):                                     
    param_list=pickle.loads(s[1:len(s)])                                                                                   #DESERIALIZE THE TIME DATA
    check_os(param_list)                                                                                                       #CHECK THE TYPE OF OS
    print param_list
else:
    end_msg+=s[1:len(s)]
#print end_msg
#print "The msessage is Received "
print 'Closing connection........'
socks.close()                                                                                                                   #CLOSE THE SOCKET 
print "System time is set successfully"
sleep(2)
