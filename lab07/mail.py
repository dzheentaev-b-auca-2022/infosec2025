#!/usr/bin/env python3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Email server details (for example, Gmail's SMTP)
smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = ""  # Replace with your email address
sender_password = ""     # Replace with your email password or app-specific password
receiver_email = ""  # Replace with the recipient's email

# HTML email content
subject = "Подтвердите платежные данные для отправки заказа"
body = "Это тестовое письмо"


# Set up the MIME
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject


# Attach the body with the HTML content
message.attach(MIMEText(body, "html"))


# Send the email
try:
   # Establish a secure session with the server
   server = smtplib.SMTP(smtp_server, smtp_port)
   server.starttls()  # Secure the connection
   server.login(sender_email, sender_password)  # Log into the email server
   text = message.as_string()
   server.sendmail(sender_email, receiver_email, text)  # Send the email
   print("Email sent successfully!")
except Exception as e:
   print(f"Error sending email: {e}")
finally:
   server.quit()  # Close the connection
