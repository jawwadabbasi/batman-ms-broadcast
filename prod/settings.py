# Include all global variables in this file.
# These are used across different modules/packages
# where required.

# Service Name
SVC_NAME = 'batman-ms-broadcast'

# DB Settings
DB_HOST_WRITER = '127.0.0.1'
DB_HOST_READER = '127.0.0.1'
DB_PORT = 3306
DB_NAME = 'batman_broadcast'
DB_USER = 'root'
DB_PASS = ''

# Batman Settings
BATMAN_URL = ''

# Mailbox Settings
BATMAIL = 'jawwad@kodelle.com'
BATPASSWORD = 'alfredismybestfriend'

# Teams Settings
BATMAN_TEAMS_NOTIFICATION_WEBHOOK = ''
BATMAN_TEAMS_INCIDENT_WEBHOOK = ''
BATMAN_TEAMS_MESSAGE_WEBHOOK = ''

# Sentry Settings
SENTRY_DSN = ''
SENTRY_TRACES_SAMPLE_RATE = 1.0
SENTRY_PROFILES_SAMPLE_RATE = 1.0
SENTRY_ENV = 'production'

# Flask Settings
FLASK_PORT = 80
FLASK_DEBUG = False