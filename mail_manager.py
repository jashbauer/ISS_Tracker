import smtplib


class Mailer:

    def __init__(self, email, password):
        self.my_email = email
        self.password = password

    def send_mail(self, message):
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(user=self.my_email, password=self.password)
                connection.sendmail(from_addr=self.my_email, to_addrs=self.my_email,
                                    msg=f"Subject:ISS Position\n\n{message}")
        except:
            print("Unable to send e-mail. Please, review send data.")
