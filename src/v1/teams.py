import concurrent.futures
import json
import uuid
import inspect
import settings

from includes.db import Db
from services.logger import Logger
from v1.relay import Relay
from v1.template import Template

class Teams:

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
        
        tn = Teams.Translate(purpose,meta if meta else {})

        if not tn:
            api_data['ApiHttpResponse'] = 400
            api_data['ApiMessages'] += ['ERROR - Unsupported template']

            return api_data
        
        response = Relay.SendTeamsMessage(tn)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(
                Teams.Track,
                tn['Channel'],
                purpose,
                tn['Subject'],
                tn['Message'],
                True if response else False,
            )

        if not response:
            api_data['ApiHttpResponse'] = 500
            api_data['ApiMessages'] += ['ERROR - Could not send message on teams']

            return api_data
        
        api_data['ApiHttpResponse'] = 201
        api_data['ApiMessages'] += ['Request processed successfully']

        return api_data
    
    def Track(channel,purpose,subject,message,delivered):

        query = """
            INSERT INTO teams
            SET teams_id = %s,
                channel = %s,
                purpose = %s,
                subject = %s,
                message = %s,
                delivered = %s,
                date = NOW()
        """

        inputs = (
            str(uuid.uuid4()),
            channel,
            purpose,
            subject,
            json.dumps(message),
            delivered,
        )

        return Db.ExecuteQuery(query,inputs,True)
    
    def Translate(purpose,meta):

        if purpose == 'batman-incident':
            return Teams.TemplateBatmanIncident(purpose,meta)
        
        if purpose == 'batman-notification':
            return Teams.TemplateBatmanNotification(purpose,meta)
        
        if purpose == 'batman-message':
            return Teams.TemplateBatmanMessage(purpose,meta)
        
        return False
    
    def TemplateBatmanIncident(purpose,meta):

        try:
            return {
                "Webhook": settings.BATMAN_TEAMS_INCIDENT_WEBHOOK,
                "Channel": 'batman-incidents',
                "Subject": meta.get('Subject', 'Batman Incident'),
                "Purpose": purpose,
                "Message": Template.TeamsBatmanIncident(meta),
            }
        
        except Exception as e:
            Logger.CreateExceptionLog(inspect.stack()[0][3], str(e), 'ERROR - Failed to create teams incident template')

            return False
        
    def TemplateBatmanNotification(purpose,meta):

        try:
            return {
                "Webhook": settings.BATMAN_TEAMS_NOTIFICATION_WEBHOOK,
                "Channel": 'batman-notifications',
                "Subject": meta.get('Subject','Batman Notification'),
                "Purpose": purpose,
                "Message": Template.TeamsBatmanNotification(meta),
            }
        
        except Exception as e:
            Logger.CreateExceptionLog(inspect.stack()[0][3], str(e), 'ERROR - Failed to create teams notification template')

            return False
        
    def TemplateBatmanMessage(purpose,meta):

        try:
            return {
                "Webhook": settings.BATMAN_TEAMS_MESSAGE_WEBHOOK,
                "Channel": 'batman-messages',
                "Subject": meta.get('Subject','Batman Message'),
                "Purpose": purpose,
                "Message": Template.TeamsBatmanMessage(meta),
            }
        
        except Exception as e:
            Logger.CreateExceptionLog(inspect.stack()[0][3], str(e), 'ERROR - Failed to create teams message template')

            return False