from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.MIMEImage import MIMEImage
 
from email.utils import COMMASPACE,formatdate
from email import encoders
import os
import sys

#########################################################
def send_mail(subject, text, receiver): 
    server={}
    server['name'] = 'mail.funshion.com'
    server['user'] = 'lihh'
    server['passwd'] = 'Storm@013'
    to = receiver
    fro = 'lihh@funshion.com' 
    
    msg = MIMEMultipart() 
    msg['From'] = fro 
    msg['Subject'] = subject 
    msg['To'] = COMMASPACE.join(to) #COMMASPACE==', ' 
    msg['Date'] = formatdate(localtime=True) 
    
    text2 = r'%s<br>' % text
    msg.attach(MIMEText(text2,'html','gbk')) 
    
    import smtplib 
    smtp = smtplib.SMTP(server['name']) 
    smtp.login(server['user'], server['passwd']) 
    smtp.sendmail(fro, to, msg.as_string()) 
    smtp.close()
    
def read_file(filename):
    with open (filename, "r") as myfile:
        return myfile.read()
    return ""

if __name__=="__main__":
    subject = sys.argv[1]
    receiver = sys.argv[2].split(";")
    content = read_file(sys.argv[3])
    content = content.replace("\n", "<br>")
    send_mail(subject, content, receiver)
