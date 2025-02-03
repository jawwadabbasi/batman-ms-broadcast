import concurrent.futures
import uuid

from includes.common import Common
from includes.db import Db
from v1.email import Email
from v1.relay import Relay
from v1.wrapper import Wrapper

class Batsignal:

    def Send(user_id,purpose,meta):

        api_data = {}
        api_data['ApiHttpResponse'] = 500
        api_data['ApiMessages'] = []
        api_data['ApiResult'] = []

        try:
            user_id = str(user_id)
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

        query = """
            INSERT INTO batsignal
            SET batsignal_id = %s,
                sender = %s,
                created_by = %s,
                user_id = %s,
                purpose = %s,
                subject = %s,
                content = %s,
                broadcast = %s,
                date = NOW()
        """

        inputs = (
            str(uuid.uuid4()),
            tn['Sender'],
            meta.get('CreatedBy'),
            user_id,
            purpose,
            tn['Subject'],
            meta.get('Content'),
            meta.get('Broadcast', False),
        )

        result = Db.ExecuteQuery(query,inputs,True)

        if result is False:
            api_data['ApiHttpResponse'] = 500
            api_data['ApiMessages'] += ['ERROR - Could not insert record']

            return api_data

        if result and not meta.get('Broadcast'):
            api_data['ApiHttpResponse'] = 201
            api_data['ApiMessages'] += ['Request processed successfully']

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
                True if response else False
            )

        if not response:
            api_data['ApiHttpResponse'] = 500
            api_data['ApiMessages'] += ['ERROR - Could not broadcast announcement']

            return api_data

        api_data['ApiHttpResponse'] = 201
        api_data['ApiMessages'] += ['Request processed successfully']

        return api_data
    
    def List(limit,offset,datetime):

        api_data = {}
        api_data['ApiHttpResponse'] = 500
        api_data['ApiMessages'] = []
        api_data['ApiResult'] = []

        try:
            datetime = str(datetime) if datetime else Common.Datetime()
            limit = int(limit) if limit else 10
            offset = int(offset) if offset else 1

        except:
            api_data['ApiHttpResponse'] = 400
            api_data['ApiMessages'] += ['INFO - Invalid arguments']

            return api_data

        query = """
            SELECT 
                t1.batsignal_id,
                t1.sender,
                t1.created_by,
                t1.user_id,
                t1.subject,
                t1.content,
                t1.broadcast,
                t1.date
            FROM batsignal t1
            WHERE date < %s 
            ORDER BY date DESC
            LIMIT %s
            OFFSET %s
        """

        inputs = (
            datetime,
            limit, 
            (offset - 1) * limit
        )

        result = Db.ExecuteQuery(query,inputs)

        if result is False:
            api_data['ApiHttpResponse'] = 500
            api_data['ApiMessages'] += ['ERROR - Could not retrieve records']

            return api_data

        if not result:
            api_data['ApiHttpResponse'] = 200
            api_data['ApiMessages'] += ['No records found']

            return api_data
        
        api_data['ApiHttpResponse'] = 200
        api_data['ApiMessages'] += ['INFO - Request processed successfully']
        api_data['ApiResult'] = Wrapper.Package(result,'list-batsignal')

        return api_data