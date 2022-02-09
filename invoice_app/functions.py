from django.core.mail import EmailMessage
from django.conf import settings



def emailInvoiceClient(to_email, from_client, filepath):
    from_email = settings.EMAIL_HOST_USER
    subject = 'Devis'
    body = """
    Bonjours, vous trouverez ci-joint votre devis
    """.format(from_client)

    message = EmailMessage(subject, body, from_email, [to_email])
    message.attach_file(filepath)
    message.send()