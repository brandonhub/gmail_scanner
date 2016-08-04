import httplib2, atexit
from apiclient import errors, discovery
from oauth2client import client
from apiclient.http import BatchHttpRequest
from myApp import dataService
from apscheduler.schedulers.background import BackgroundScheduler
from Models import User
import functools

class EmailScanner(object):
    def __init__(self, dataService):
        self.dataService = dataService

    def scanAll(self):
        users = self.dataService.getAllUsers()
        serviceTrackers = self.getServiceTrackers(users)

        batchList = {}
        batchCount = 0
        requestCount = 0
        batchList[batchCount] = discovery.build('gmail', 'v1').new_batch_http_request()

        for tracker in serviceTrackers:
            if requestCount > 998:
                batchCount += 1
                batchList[batchCount] = discovery.build('gmail', 'v1').new_batch_http_request()
                requestCount = 0
            batch = batchList[batchCount]
            batch.add(tracker['service'].users().messages().list(userId="me", q="after:2016/07/19", maxResults=500), callback=functools.partial(self.storeIds, tracker))
            requestCount += 1

        # one by one executre batches composed of 1000 requests max
        for key, batch in batchList.items():
            batch.execute()

        batchList = {}
        batchCount = 0
        requestCount = 0
        batchList[batchCount] = discovery.build('gmail', 'v1').new_batch_http_request()

        for tracker in serviceTrackers:
            for messageId in tracker['messageIds']:
                if requestCount > 998:
                    batchCount += 1
                    batchList[batchCount] = discovery.build('gmail', 'v1').new_batch_http_request()
                    requestCount = 0
                batch = batchList[batchCount]
                batch.add(tracker['service'].users().messages().get(userId="me", id=messageId, format="metadata", metadataHeaders=["Subject", "From"]), callback=functools.partial(self.storeMessage, tracker))
                requestCount += 1

        for key, batch in batchList.items():
            batch.execute()


    def storeIds(self, tracker, request_id, response, exception):
        messageIds = []
        for idDict in response['messages']:
            messageIds.append(idDict['id'])
        tracker['messageIds'] = messageIds

    def storeMessage(self, tracker, request_id, response, exception):
        user_id = tracker['user_id']
        snippet = response['snippet']
        sender = ""
        subject = ""

        for header in response['payload']['headers']:
            if header['name'] == "From":
                sender = header['value']
            elif header['name'] == "Subject":
                subject = header['value']


        self.dataService.validateAndStoreMessage(subject, sender, snippet, user_id)

    def getServiceTrackers(self, users):
        serviceTrackers = []
        for user in users:
            credentials = client.OAuth2Credentials.from_json(user.credentials)
            http_auth = credentials.authorize(httplib2.Http())
            service = {'user_id': user.id, 'emailAddress': user.emailAddress, 'service': discovery.build('gmail', 'v1', http=http_auth), "messageIds": [], "topi"}
            serviceTrackers.append(service)
        return serviceTrackers

    def startJob(self):
        bs = BackgroundScheduler()

        @bs.scheduled_job('interval', seconds=60)
        def job_function():
            self.scanAll()
            pass

        bs.start()
        atexit.register(lambda: bs.shutdown(wait=False))