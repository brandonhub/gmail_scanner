from myApp import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emailAddress = db.Column(db.String(240), unique=True)
    credentials = db.Column(db.String(500), unique=False)
    latestScan = db.Column(db.DateTime)
    topic = db.relationship('Topic', backref='user',
                                lazy='dynamic')

    def __init__(self, emailAddress, credentials):
        self.emailAddress = emailAddress
        self.credentials = credentials

    def __repr__(self):
        return '<User: %r>' % self.emailAddress

class Topic(db.Modal):
    id = db.Column(db.Integer, primary_key=True)
    displayName = db.Column(db.String(400))
    query = db.Column(db.String(400);
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.relationship('Message', backref='topic',
    lazy='dynamic')

    def __init__(self, displayName, query, user_id):
        self.displayName = subject
        self.query = sender
        self.user_id = user_id

    def __repr__(self):
        return '<Topic: %r>' % self.displayName

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(400))
    sender = db.Column(db.String(400))
    snippet = db.Column(db.String(400))
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))

    def __init__(self, subject, sender, snippet, user_id):
        self.subject = subject
        self.sender = sender
        self.snippet = snippet
        self.user_id = user_id

    def __repr__(self):
        return '<Message: %r>' % self.subject

