import boto3

from src.config import settings


class EmailService:
    def __init__(self):
        self.client = boto3.client(
            "ses",
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

    def send_email(self, to_email: str, subject: str, message: str):
        return self.client.send_email(
            Source=settings.SES_EMAIL_FROM,
            Destination={
                "ToAddresses": [to_email],
            },
            Message={""
                     "Subject":
                         {"Data": subject,
                          "Charset": "UTF-8"
                          },
                     "Body": {
                         "Text": {
                             "Data": message,
                             "Charset": "UTF-8"
                         }
                },
            },
        )

