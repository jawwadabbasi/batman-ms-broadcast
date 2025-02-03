import inspect

from services.logger import Logger
from v1.batsignal import Batsignal
from v1.email import Email
from v1.teams import Teams

class Ctrl_v1:

    def Response(endpoint, request_data=None, api_data=None, log=True):

        if log is True:
            Logger.CreateServiceLog(endpoint, request_data, api_data)

        return api_data

    def BadRequest(endpoint, request_data=None):

        api_data = {}
        api_data['ApiHttpResponse'] = 400
        api_data['ApiMessages'] = ['ERROR - Missing required parameters']
        api_data['ApiResult'] = []

        Logger.CreateServiceLog(endpoint, request_data, api_data)

        return api_data

    def SendEmail(request_data):

        if (not request_data.get('Purpose')):
            return Ctrl_v1.BadRequest(inspect.stack()[0][3], request_data)

        api_data = Email.Send(
            request_data.get('Purpose'),
            request_data.get('Meta', None)
        )

        return Ctrl_v1.Response(inspect.stack()[0][3], request_data, api_data)
    
    def SendTeamsMessage(request_data):

        if (not request_data.get('Purpose')):
            return Ctrl_v1.BadRequest(inspect.stack()[0][3], request_data)

        api_data = Teams.Send(
            request_data.get('Purpose'),
            request_data.get('Meta', None)
        )

        return Ctrl_v1.Response(inspect.stack()[0][3], request_data, api_data)

    def SendBatsignal(request_data):

        if (not request_data.get('UserId')):
            return Ctrl_v1.BadRequest(inspect.stack()[0][3], request_data)

        api_data = Batsignal.Send(
            request_data.get('UserId'),
            request_data.get('Purpose','Batsignal'),
            request_data.get('Meta', None)
        )

        return Ctrl_v1.Response(inspect.stack()[0][3], request_data, api_data)

    def ListBatsignal(request_data):

        api_data = Batsignal.List(
            request_data.get('Limit', None),
            request_data.get('Offset', None),
            request_data.get('Datetime',None)
        )

        return Ctrl_v1.Response(inspect.stack()[0][3], request_data, api_data)