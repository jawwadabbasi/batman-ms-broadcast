import concurrent.futures
import json
import uuid
import inspect
import settings

from includes.db import Db
from services.justiceleague import JusticeLeague
from services.logger import Logger
from v1.relay import Relay
from v1.template import Template

class Email:

    def Send(purpose,meta):

        api_data = {}
        api_data['ApiHttpResponse'] = 500
        api_data['ApiMessages'] = []
        api_data['ApiResult'] = []

        try:
            purpose = str(purpose)

        except:
            api_data['ApiHttpResponse'] = 400
            api_data['ApiMessages'] += ['ERROR - Invalid arguments']

            return api_data
        
        if meta and type(meta) != dict:
            api_data['ApiHttpResponse'] = 400
            api_data['ApiMessages'] += ['ERROR - Invalid meta']

            return api_data
        
        tn = Email.Translate(purpose,meta if meta else {})

        if not tn:
            api_data['ApiHttpResponse'] = 400
            api_data['ApiMessages'] += ['ERROR - Unsupported template']

            return api_data
        
        response = Relay.SendEmail(tn)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(
                Email.Track,
                tn['Sender'],
                tn['BCCRecipients'],
                purpose,
                tn['Subject'],
                tn['Message'],
                tn['ReplyTo'],
                tn['CCRecipients'],
                True if response else False,
            )

        if not response:
            api_data['ApiHttpResponse'] = 500
            api_data['ApiMessages'] += ['ERROR - Could not deliver email']

            return api_data
        
        api_data['ApiHttpResponse'] = 201
        api_data['ApiMessages'] += ['Request processed successfully']

        return api_data
    
    def Track(sender,bcc_recipients,purpose,subject,message,reply_to,cc_recipients,delivered):

        query = """
            INSERT INTO emails
            SET email_id = %s,
                sender = %s,
                bcc_recipients = %s,
                purpose = %s,
                subject = %s,
                message = %s,
                reply_to = %s,
                cc_recipients = %s,
                delivered = %s,
                date = NOW()
        """

        inputs = (
            str(uuid.uuid4()),
            sender,
            json.dumps(bcc_recipients),
            purpose,
            subject,
            message,
            json.dumps(reply_to),
            json.dumps(cc_recipients),
            delivered,
        )

        return Db.ExecuteQuery(query,inputs,True)
    
    def Translate(purpose,meta):

        if purpose == 'batman-batsignal':
            return Email.TemplateBatsignal(purpose,meta)
        
        if purpose == 'test-batsignal':
            return Email.TemplateTestAnnouncement(purpose,meta)
        
        return False
    
    def TemplateBatsignal(purpose,meta):

        try:
            emails = JusticeLeague.GetMembers()

            if not emails:
                return False

            return {
                "Sender": settings.BATMAIL,
                "Password": settings.BATPASSWORD,
                "Subject": meta.get('Subject', 'Batsignal'),
                "BCCRecipients": emails,
                "CCRecipients": meta.get('CCRecipients', []),
                "Purpose": purpose,
                "Message": Template.EmailBatsignal(meta),
                "ReplyTo": meta.get('ReplyTo', []),
            }
        
        except Exception as e:
            Logger.CreateExceptionLog(inspect.stack()[0][3], str(e), 'ERROR - Failed to create batsignal template')

            return False
        
    def TemplateTestAnnouncement(purpose,meta):

        try:
            emails = [
                'jawwad@kodelle.com',
            ]

            return {
                "Sender": settings.BATMAIL,
                "Password": settings.BATPASSWORD,
                "Subject": meta['Subject'],
                "BCCRecipients": emails,
                "CCRecipients": meta.get('CCRecipients', []),
                "Purpose": purpose,
                "Message": Template.EmailBatsignal(meta),
                "ReplyTo": meta.get('ReplyTo', []),
            }
        
        except Exception as e:
            Logger.CreateExceptionLog(inspect.stack()[0][3], str(e), 'ERROR - Failed to create test batsignal template')

            return False