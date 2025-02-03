import requests
import json
import inspect

from services.logger import Logger
from exchangelib import Credentials, Account, Configuration, DELEGATE, Message, HTMLBody

class Relay:

    def SendEmail(data):

        try:
            credentials = Credentials(data['Sender'],data['Password'])

            config = Configuration(
                credentials=credentials,
                max_connections=10,
                service_endpoint='https://outlook.office365.com/EWS/Exchange.asmx'
            )

            account = Account(
                primary_smtp_address=data['Sender'],
                config=config,
                autodiscover=False,
                access_type=DELEGATE
            )

        except Exception as e:
            Logger.CreateExceptionLog(inspect.stack()[0][3], str(e), f"ERROR - Could not connect with mailbox {data['Sender']}")

            return False

        try:
            message = Message(
                account=account,
                folder=account.sent,
                subject=data['Subject'],
                body=HTMLBody(data['Message']),
                bcc_recipients=data['BCCRecipients'],
                cc_recipients=data['CCRecipients'],
                reply_to=data['ReplyTo']
            )
        
        except Exception as e:
            Logger.CreateExceptionLog(inspect.stack()[0][3], str(e), 'ERROR - Failed to create message')

            return False

        try:
            message.send_and_save()

            return True

        except Exception as e:
            Logger.CreateExceptionLog(inspect.stack()[0][3], str(e), 'ERROR - Failed to send email to users')

            return False
        
    def SendTeamsMessage(data):

        headers = {
            'Content-Type': 'application/json'
        }

        try:
            result = requests.post(data['Webhook'],headers=headers,data=json.dumps(data['Message']))

            return True if result.ok else False

        except Exception as e:
            Logger.CreateExceptionLog(inspect.stack()[0][3], str(e), f"ERROR - Failed to send message on teams: {data['Webhook']}")

            return False