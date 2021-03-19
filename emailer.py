#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib, ssl

def reminder(receiver_email, message):

    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = "email"
    password = "password"
    
    # Create a secure SSL context
    context = ssl.create_default_context()
    
    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(sender_email, password)
        # Send email here
        for email in receiver_email:
            server.sendmail(sender_email, email, message)
            
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit() 