from django.core.mail import EmailMessage


class Utils:

    @staticmethod
    def send_email(data):
        send_to = data['to_email']
        email = EmailMessage(
            data['subject'], 
            data['body'], 
            'contact.fbpublisher@gmail.com', 
            [f'{send_to}',]

            )
        email.send()