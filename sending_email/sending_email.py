import smtplib
import ssl

port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = "nam95thptlk@gmail.com"
receiver_email = "doankhuc123@gmail.com"
password = input("Type your password and press enter: ")

context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.ehlo()  # Can be omitted
    server.starttls(context=context)
    server.ehlo()  # Can be omitted
    server.login(sender_email, password)
    for i in range(10):
        message = """\
        Subject: Dm may

        Hello Doan Lon""" + str(i)
        server.sendmail(sender_email, receiver_email, message)
print("Sent.")
