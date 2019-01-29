# import smtplib
# from email.mime.text import MIMEText
#
# subject="hi"
# content="<a href='http://127.0.0.1:8000'>可以激活账户了</a>"
# sender='wuying0423zj@163.com'
# recver="245672571@qq.com"
# password="zgsadntoucinbefa"
# message=MIMEText(content,'html','utf-8')
# message["Subject"] = subject #邮件的主题
# message["To"] = recver #收件人
# message["From"] = sender
#
# #发送邮件
# #实例化smtp服务器
# smtp = smtplib.SMTP_SSL("smtp.163.com",994)
# #登录自己的账户
# smtp.login(sender,password)
# smtp.sendmail(sender,[recver],message.as_string())
#     #as_string对message的消息进行了封装
# smtp.close()


list=[3,4,5,7,8,2,9]
print(sum(map(lambda x:x+3,list[1::2])))
print(sum(i+3 for i in list[1::2]))