# ISS Tracker
A script that runs in the background made for coding practice. Tracks the
position of the International Space Station over Earth and sends the user an
email if it is within 5 degrees of the user's latitude and longitude and it is
dark outside.

Required environment variables:
- `LATITUDE`: The user's latitude
- `LONGITUDE`: The user's longitude
- `SMTP_SERVER`: The hostname of the server used to send the email
- `SMTP_PORT`: Optional: The port number for the SMTP server. Default is 0.
- `SENDER_EMAIL`: The email address used to send the notification.  
- `SENDER_EMAIL_PASSWORD`: The password for the sender's email account. Your 
  email provider may not allow you to use your email password directly, but may 
  be able to provide you with an application password. (This is true of GMail.)
- `RECIPIENT_EMAIL`: The email address the notification should be sent to.  