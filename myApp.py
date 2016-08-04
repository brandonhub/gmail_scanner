import flask, httplib2, json, atexit
from apscheduler.schedulers.background import BackgroundScheduler
from flask_sqlalchemy import SQLAlchemy
from oauth2client import client
from gmail_service import GmailService

app = flask.Flask(__name__)
app.secret_key = "super secret key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

from data_service import DataService
db.reflect()
db.drop_all()
db.session.commit()
db.create_all()
db.session.commit()
dataService = DataService(db)

print("--------------------\n")
print("--------------------\n")
print("--------------------\n")
print("--------------------\n")

from email_scanner import EmailScanner
emailScanner = EmailScanner(dataService)
emailScanner.scanAll()
#emailScanner.startJob()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return flask.render_template('login.html')
    else:
        return flask.redirect(flask.url_for('oauth2callback'))

@app.route('/test')
def testService():
    emailScanner.scanAll();
    return ("done")

@app.route('/')
def index():
    return flask.render_template('result.html')

@app.route('/oauth2callback')
def oauth2callback():
    flow = client.flow_from_clientsecrets(
        'client_id.json',
        scope=['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify'],
        redirect_uri=flask.url_for('oauth2callback', _external=True)
    )
    flow.params['access_type'] = 'offline'
    if 'code' not in flask.request.args:
        auth_uri = flow.step1_get_authorize_url()
        return flask.redirect(auth_uri)
    else:
        auth_code = flask.request.args.get('code')
        credentials = flow.step2_exchange(auth_code)

        gmailService = GmailService(credentials.to_json())
        currentUser = gmailService.getCurrentUser()
        emailAddress = currentUser['emailAddress']
        dataService.storeCredentials(emailAddress, credentials)

        return flask.redirect(flask.url_for('index'))

if __name__ == '__main__':
    import uuid
    app.secret_key = str(uuid.uuid4())
    app.debug = False
    app.run()


