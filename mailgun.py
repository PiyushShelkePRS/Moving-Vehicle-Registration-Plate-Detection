import os
os.environ['KMP_DUPLICATE_LIB_OK']= 'TRUE'
import smtplib,ssl

sender_email = "raspberrycar2017@gmail.com"
password = "hfmrwbwuhxdmxmwa"

# sender_email = "piyushshelke8810@gmail.com"
# password = "Piyush@7890"

receiver_email = "piyushshelke8810@gmail.com"

def mail(subject, text):


    message = f"""From: <{sender_email}>
To: <{receiver_email}>
Subject: {subject}


{text}
"""

    context = ssl.create_default_context()
    print("Sending mail to", receiver_email)
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo() 
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

