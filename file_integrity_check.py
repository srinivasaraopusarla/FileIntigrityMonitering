import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime
import urllib.request
from email.utils import COMMASPACE, formatdate
from email import encoders
import hashlib
import time



def sendmail(alert):
   fromaddr = '#mailid of sender'
   toaddrs = '#mailid of receiver'

   msg = MIMEMultipart()
   msg['Date'] = formatdate(localtime=True)

   msg = MIMEMultipart('alternative')
   msg['Subject'] = "hashvalue"
   msg['From'] = fromaddr #like name
   msg['To'] = toaddrs

   body = MIMEText(str(alert))
   msg.attach(body)

   username = '#mailid of sender'
   password = '#password of sender'
   server = smtplib.SMTP_SSL('smtp.googlemail.com', 465)
   server.login(username, password)
   server.sendmail(fromaddr, toaddrs, msg.as_string())
   server.quit()




# hash funtion-----------------------------------------------------------------------------------
def hash_file(filename):

    # make a hash object
    h = hashlib.sha1()
    # open file for reading in binary mode
    with open(filename,'rb') as file:
    # loop till the end of the file
        chunk = 0
        while chunk != b'':
            # read only 1024 bytes at a time
            chunk = file.read(1024)
            h.update(chunk)
            # return the hex representation of digest        
    return h.hexdigest()




filelist=[]
orihashlist=[]
def traverseFolder(path,list):
    l=os.listdir(path)
    for i in l:
        if os.path.isdir(path+"\\"+i):
            traverseFolder(path+"\\"+i)
        else:
            filelist.append(i)
            a=hash_file(path+"\\"+i)
            list.append(a)


traverseFolder("#folder path which is to be monitered",orihashlist)

#print (hashlist)
a={key: [key, value] for key, value in zip(filelist, orihashlist)}
#print(a)
sendmail(a)

""""this infinet loop is to continusly calculate the hashvalues of the files in requrired folder
 and verify for intigrity with original hashvalues."""
 
while(True):
    hashchecklist=[]
    traverseFolder("same folderpath which is to monitered",hashchecklist)
    n=len(hashchecklist)

    t=len(orihashlist)
    if (n==t):
        for j in (0,n-1):
            if (orihashlist[j]==hashchecklist[j]):
                time.sleep(1)
            else:
                sendmail("intigrity of file: "+filelist[j]+" has changed, and hash value is changed from "+orihashlist[j]+"  to  "+hashchecklist[j])
        time.sleep(1)
        print("good")

    elif(n>t):
        sendmail("a new file is created")
    else:
        sendmail("some file is deleted")      

                        

                

    
    
     


  