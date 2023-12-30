from datetime import date
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_birthday_email(receiver_email, subject, body):
    # Set up the email server
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  
    smtp_username = 'your_email@gmail.com'
    smtp_password = 'your_password'

    message = MIMEMultipart()

    message['From'] = smtp_username
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, receiver_email, message.as_string())

d = date.today()
month = str(d.month)
day = str(d.day)
total = day+"/"+month

birthdaydict = {
    "birthday_person1@gmail.com | Friend1": "22/4",
    "birthday_person2@gmail.com | Friend2": "19/2",
    "birthday_person3@gmail.com | Friend3": "4/5"
}
x = birthdaydict.values()

counter = 0
for i in x:
    if total == i:
        global y
        y = list(birthdaydict)[counter]
        receiver_email = y.split()[0]
        subject = 'Happy Birthday!'
        body = """
Dear """+y.split()[2]+""",

Happy Birthday! 🎉 This day rocks man!

Happy Birthday, """+y.split()[2]+"""! 🥳

With love,
Your Name
"""
        send_birthday_email(y.split()[0], subject, body)
        print("sent to this:", y.split()[2])
    else:
        pass
    counter+=1
