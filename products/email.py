from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

def send_order_email(name, email, order, email_file):
    context = {
        'name':name,
        'order':order,
    }

    email_subject = 'thank you for youre order'
    email_body = render_to_string(email_file, context)
    email = EmailMessage(
        email_subject, 
        email_body,
        settings.DEFAULT_FORM_EMAIL, 
        [email, ],
    )
    
    return email.send(fail_silently=False)