def send_email(mail_msg):
    import smtplib

    gmail_user = "testuser@gmail.com"
    gmail_pwd = "testpass"
    FROM = 'testuser@gmail.com'
    TO = ['myemail@live.com']
    SUBJECT = "mysubject"
    TEXT = str(mail_msg)

    # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        # server = smtplib.SMTP(SERVER)
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        #server.quit()
        server.close()
        print 'successfully sent the mail'
    except:
        print "failed to send mail"

