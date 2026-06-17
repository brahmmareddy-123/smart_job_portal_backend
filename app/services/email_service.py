import smtplib
from email.mime.text import MIMEText


EMAIL = "23eg110c07@anurag.edu.in"
PASSWORD = "ttbg lmxo cscf cvqd"

def send_email(to_email, subject, body):

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = to_email

    server = smtplib.SMTP("smtp.gmail.com", 587)

    server.starttls()

    server.login(EMAIL, PASSWORD)

    server.send_message(msg)

    server.quit()