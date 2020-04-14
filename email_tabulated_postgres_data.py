import psycopg2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from tabulate import tabulate

DB = {
    'database': "***",
    'user': "***", 'password': "***",
    'host': "***",
    'port': "***"
}
conn = psycopg2.connect(database=DB['database'],
                        user=DB['user'],
                        password=DB['password'],
                        host=DB['host'],
                        port=DB['port'])

to_tabulate1 = {}
to_tabulate1['1_col'] = []
to_tabulate1['2_col'] = []
to_tabulate1['3_col'] = []

cur1 = conn.cursor()
cur1.execute("""select *** *** ***;""")
for item in cur1.fetchall():
    to_tabulate1['1_col'].append(item[0])
    to_tabulate1['2_col'].append(item[1])
    to_tabulate1['3_col'].append(item[2])
conn.commit()
conn.close()

print(tabulate(to_tabulate1))


login_email = '***'

from_email = "***"
to_email = ["***", "***", "***", "***"]
subject = "***"
body_text = "***"
html = """\
<html>
  <head>
  <style>
  table, th, td {{ border: 1px solid black; border-collapse: collapse; }}
  th, td {{ padding: 5px; }}
  </style>
  </head>
  <body>
    <br>
    {table1}
    <br>
    <p><br>Regards,<br>
    Mohit</p>
  </body>
</html>
""".format(table1 = tabulate(to_tabulate1, headers=['1_col', '2_col', '3_col'], tablefmt="html"))
attachment_path_list = ["***", "***"]

smtp_con = smtplib.SMTP("smtp.gmail.com")
smtp_con.starttls()
smtp_con.login(login_email, 'upwardsoffice')
msg = MIMEMultipart()
msg['From'] = from_email
msg['To'] = ','.join(to_email)
msg['Subject'] = subject
msg.attach(MIMEText(body_text, 'plain'))
msg.attach(MIMEText(html, 'html'))

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
            print("could not attach file")

smtp_con.sendmail(msg['From'], to_email, msg.as_string())
smtp_con.quit()

print("mail sent from:{} ;to:{}!".format(from_email, to_email))
