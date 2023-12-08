import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

# Your email credentials
sender_email = 'kybrian20@gmail.com'
# sender_password = 'sE8W7UBqx^Ss!d!LX!LKpAd3UppoXzZpe4jUskJZKZ9%a%x32x'
sender_password = 'qiai vjea tlkv fyux'

# List of recipients
recipients = ['kybrian.se@gmail.com', 'micminn87@gmail.com','kamaugikure89@gmail.com',
'kamaugikure21@gmail.com']

# Email server settings
smtp_server = 'smtp.gmail.com'
smtp_port = 587


# Loop through recipients and send emails
for i, recipient in enumerate(recipients, start=1):
    ticket_file = f'Ticket {i}.png'
    
    print(recipient,i)
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient
    msg['Subject'] = 'Your Ticket'

    # Attach the ticket file
    with open(ticket_file, 'rb') as file:
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
