from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from datetime import date

#this script sends the data textfile as an attatchement to an email
#this email is mailed to the teamliftirrigationtest@gmail.com email
fromaddr = "pranavrajan568@gmail.com"
toaddr = "teamliftirrigationtest@gmail.com"

msg = MIMEMultipart()

msg['From'] = fromaddr
msg['To'] = toaddr
#gets the current date as a string to signify when the data was recorded
date_today= (date.today()).strftime("%B %d, %y")
msg['Subject'] = "Readout Data For " + date_today
body = "This is the Data for  " + date_today

msg.attach(MIMEText(body, 'plain'))

filename = "data.txt"
#data.txt file is added as an attatchment
attachment = open(filename, "rb")

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

msg.attach(part)
#connection is started and established for email to be transmitted
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, "sidcxmariegfnwpe")
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
#email server closed
server.quit()