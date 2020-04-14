import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime

login_email = ''

from_email = ""
to_email = [""]
subject = "test"
body_text = "Hi"
attachment_path_list = [r'C:\Users\____.zip']

smtp_con = smtplib.SMTP("smtp.gmail.com")
smtp_con.starttls()
smtp_con.login(login_email, '') # enter password
msg = MIMEMultipart()
msg['From'] = from_email
msg['To'] = ','.join(to_email)
msg['Subject'] = subject
msg.attach(MIMEText(body_text,'plain'))

if attachment_path_list is not None:
    for each_file_path in attachment_path_list:
        try:
            file_name=each_file_path.split("/")[-1]
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(each_file_path, "rb").read())

            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename=file_name)
            msg.attach(part)
        except:
            print("could not attache file")

smtp_con.sendmail(msg['From'], to_email, msg.as_string())
smtp_con.quit()
