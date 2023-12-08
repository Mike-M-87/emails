
import smtplib
import time

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Your email credentials
sender_email = 'email'
sender_password = 'app password from gmail' # not ordinary password

# Email server settings
smtp_server = 'smtp.gmail.com'
smtp_port = 587

# Read the CSV file with email addresses
csv_file_path = 'emails2.csv'  # Replace with the actual path

# Folder with ticket files
tickets_folder = 'tickets'  # Replace with the actual path
with open(csv_file_path, 'r') as file:
    emails = file.read().splitlines()
# Loop through each row in the CSV

for index, recipient in enumerate(emails, start=1):
    # Assuming tickets are named in a consistent way (e.g., Ticket 1.png, Ticket 2.png)
    # time.sleep(0.1)

    ticket_number = index + 454
   
    ticket_file = f'Ticket 100 ({ticket_number}).png'
    ticket_path = f'{tickets_folder}/{ticket_file}'

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = 'Your Ticket'

    print(ticket_path,recipient)
    
    # continue

    with open(ticket_path, 'rb') as file:
        attachment = MIMEApplication(file.read(), _subtype="png")
        attachment.add_header('Content-Disposition', f'attachment; filename={ticket_file}')
        msg.attach(attachment)

    # You can also include a message in the body of the email
    body = f"Dear recipient, please find your ticket ({ticket_file}) attached."
    msg.attach(MIMEText(body, 'plain'))

    # Connect to the email server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient, msg.as_string())
        server.quit()
