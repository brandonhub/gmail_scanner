import httplib2
from apiclient import errors, discovery
from oauth2client import client
from apiclient.http import BatchHttpRequest


class GmailService(object):
    def __init__(self, credentialsJson):
        credentials = client.OAuth2Credentials.from_json(credentialsJson)
        http_auth = credentials.authorize(httplib2.Http())
        self.gmailService = discovery.build('gmail', 'v1', http=http_auth)

    def getCurrentUser(self):
        return self.gmailService.users().getProfile(userId='me').execute()

