from twilio.rest import Client
import os
from dotenv import load_dotenv
from smtplib import SMTP
load_dotenv()
class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self._sid = os.getenv("TWILIO_SID")
        self._token = os.getenv("TWILIO_TOKEN")
        self._client = Client(self._sid, self._token)
        self._email = os.getenv("SMTP_EMAIL")
        self._password = os.getenv("STMP_PASSWORD")
        self.connection = SMTP(os.getenv("STMP_ADDRESS"), 587)

    def send_message(self, price, departure_code, arrival_code, out_date, in_date):
        message = self._client.messages.create(
            body=f"Low price alert! Only £{price} to fly from {departure_code} to {arrival_code}, on {out_date} until {in_date}",
            from_= os.getenv("SENDER_NUMBER"),
            to=os.getenv("RECEIVER_NUMBER")
        )
        print(message.sid)

    def send_emails(self, email_list, body):
        with self.connection:
            self.connection.starttls()
            self.connection.login(user=self._email, password=self._password)
            for email in email_list:
                print(email)
                self.connection.sendmail(from_addr=self._email,
                                to_addrs=email,
                                msg= f"Subject:Cheapest FLight Daily\n\n{body}".encode('utf-8')
                                )

