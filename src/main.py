# Built with ingenuity,
# by Jawwad Abbasi (jawwad@kodelle.com)

# Initiates a Flask app to handle managed endpoints
# and relays to corresponding controller and module
# for processing.

import json
import settings
import sentry_sdk

from flask import Flask,Response,request
from sentry_sdk.integrations.flask import FlaskIntegration
from v1.controller import Ctrl_v1
from v2.controller import Ctrl_v2

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    traces_sample_rate=settings.SENTRY_TRACES_SAMPLE_RATE,
    profiles_sample_rate=settings.SENTRY_PROFILES_SAMPLE_RATE,
    environment=settings.SENTRY_ENV,
    enable_tracing=True,
    integrations=[
        FlaskIntegration(transaction_style="url",),
    ]
)

app = Flask(__name__)

@app.errorhandler(404)
def RouteNotFound(e):

    return Response(None,status = 400,mimetype = 'application/json')

####################################
# Supported endpoints for API v1
####################################
@app.route('/api/v1/Email/Send', methods=['POST'])
def SendEmail():

    data = Ctrl_v1.SendEmail(request.json)
    return Response(json.dumps(data), status=data['ApiHttpResponse'], mimetype='application/json')

@app.route('/api/v1/Teams/Send', methods=['POST'])
def SendTeamsMessage():

    data = Ctrl_v1.SendTeamsMessage(request.json)
    return Response(json.dumps(data), status=data['ApiHttpResponse'], mimetype='application/json')

@app.route('/api/v1/Batsignal/Send', methods=['POST'])
def SendBatsignal():

    data = Ctrl_v1.SendBatsignal(request.json)
    return Response(json.dumps(data), status=data['ApiHttpResponse'], mimetype='application/json')

@app.route('/api/v1/Batsignal/List', methods=['GET'])
def ListBatsignal():

    data = Ctrl_v1.ListBatsignal(request.args)
    return Response(json.dumps(data), status=data['ApiHttpResponse'], mimetype='application/json')

####################################
# Initiate web server
####################################
app.run(host = '0.0.0.0',port = settings.FLASK_PORT,debug = settings.FLASK_DEBUG)