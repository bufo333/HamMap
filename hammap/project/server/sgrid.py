# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import From, To, Subject, PlainTextContent, HtmlContent, Mail, Content, Email


def sendmail(dest_address, token):
    from_email = From('support@hammap.org')
    to_emails = dest_address
    subject = Subject('HamMap Password Reset')
    htmlc = f'''<!doctype html><html><body><strong>A password reset request has been 
    submitted on your behalf.</strong>
        <p> Please click the following link to reset your password.</p>
        <a href="https://{os.environ.get('HOSTNAME')}/resetpw?token={token}">Reset Password</a>
        <p>Please note your password reset token is valid for 5 Minutes.</p>


        </body></html>'''
    html_content = HtmlContent(htmlc)
    pcontent = f'''A password reset request has been submitted on your behalf.
        Please click the following link to reset your password

        https://{os.environ.get('HOSTNAME')}/resetpw?token={token}

        Your password reset token will be valid for 5 minutes.'''
    content = Content('text/plain',  pcontent)
    message = Mail(from_email, to_emails, subject, content, html_content)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
