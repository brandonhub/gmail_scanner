from Models import User, Message

class DataService(object):
    def __init__(self, db):
        self.db = db

    def storeCredentials(self, emailAddress, credentials):
        if (self.userExists(emailAddress)):
            user = User.query.filter_by(emailAddress=emailAddress).first()
            user.credentials = credentials.to_json()
            self.db.session.commit()
            print ("user already exists...updating fields for user", user)
        else:
            user = User(emailAddress, credentials.to_json())
            self.db.session.add(user)
            self.db.session.commit()
            print ("new user added: ", user)

    def validateAndStoreMessage(self, subject, sender, snippet, user_id):
        latestScan = User.query().get(user_id).latestScan
        print (latestScan)
        message = Message(subject, sender, snippet, user_id)
        self.db.session.add(message)
        self.db.session.commit()
        print ("stored message")

    def isValidEmail(self, message):
        #check if already scanned
        #check if is a sale or nah
        return True

    def userExists(self, emailAddress):
        user = user = User.query.filter_by(emailAddress=emailAddress).first()
        return not user is None

    def getUser(self, emailAddress):
        user = User.query.filter_by(emailAddress=emailAddress).first()
        return user

    def getAllUsers(self):
        users = User.query.all()
        return users


