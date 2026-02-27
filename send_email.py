import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email credentials
SENDER_EMAIL = 'hamzawork5588@gmail.com'
SENDER_PASSWORD = 'tnhe sexy qobq bgyf'
RECEIVER_EMAIL = 'muhammad28980@gmail.com'

# Email content
subject = 'Node Details: DAL1-1716'
body = '''Node: DAL1-1716
IP Address: 38.255.55.87
Username: Administrator
Password: j5QNzUJS6^q(FuNc2!Wx)zV
UUID: 391603'''

msg = MIMEMultipart()
msg['From'] = SENDER_EMAIL
msg['To'] = RECEIVER_EMAIL
msg['Subject'] = subject

msg.attach(MIMEText(body, 'plain'))

try:
    # Connect to Gmail's SMTP server
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    
    # Send the email
    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
    server.quit()
    print(f'Email sent successfully to {RECEIVER_EMAIL}')
except Exception as e:
    print(f'Failed to send email: {e}')
