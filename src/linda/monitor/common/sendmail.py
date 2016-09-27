# -*- coding:utf-8 -*-
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.MIMEImage import MIMEImage
 
from email.utils import COMMASPACE,formatdate
from email import encoders

from tornado import log

def send_mail(host, user, passwd, mail_from, mail_to, subject, text):
    server={'name': host, 'user': user, 'passwd': passwd}
    
    msg = MIMEMultipart() 
    msg['From'] = mail_from
    msg['Subject'] = subject 
    msg['To'] = COMMASPACE.join(mail_to) #COMMASPACE==', ' 
    msg['Date'] = formatdate(localtime=True) 
    
    #text2 = r'%s<br>' % text
    #msg.attach(MIMEText(text2,'html','gbk')) 
    msg.attach(MIMEText(text,'html','utf-8')) 
    
    import smtplib 
    smtp = smtplib.SMTP(server['name']) 
    smtp.login(server['user'], server['passwd']) 
    smtp.sendmail(mail_from, mail_to, msg.as_string()) 
    smtp.close()
    
if __name__=="__main__":
    try:
        mail_host = 'mail.funshion.com'
        mail_user = 'spider'
        mail_passwd = 'fxsp123!'
        mail_from = 'spider@funshion.com'
        mail_to = ['qiaojw@fun.tv']
        mail_subject = u'爬虫视频统计'
        content = 'hello world'
        send_mail(mail_host, mail_user, mail_passwd, mail_from, mail_to, mail_subject, content)
    except Exception as e:
        log.app_log.error("Exception: %s" % traceback.format_exc())
