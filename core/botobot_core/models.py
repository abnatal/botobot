from botobot_core.ext.database import db

class Api(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    label = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(400), nullable=False)
    visible = db.Column(db.Boolean, nullable=False, default = 1)
    position = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'id={self.id}, name={self.name}'

    @staticmethod
    def get_all_visible():
        return Api.query.filter_by(visible = True).order_by(Api.position).all()

    @staticmethod
    def get_all():
        return Api.query.order_by(Api.position).all()

    @staticmethod
    def get(id):
        return Api.query.get(id)

    @staticmethod
    def get_by_name(name):
        return Api.query.filter_by(name = name).first()

class StaticText(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String, nullable=False, unique=True)
    fulltext = db.Column(db.String, nullable=False)
    def __repr__(self):
        return f'id={self.id}, topic={self.topic}'

    @staticmethod
    def get(topic):
        return StaticText.query.filter_by(topic = topic).first()

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(60), nullable=False, unique=True)
    fulltext = db.Column(db.Text)

    def __repr__(self):
        return f'id={self.id}, key={self.key}'

    @staticmethod
    def get(key):
        return Message.query.filter_by(key = key).first()

class ChatContext(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.String(30), index=True, nullable=False)
    client = db.Column(db.String(30), nullable=False)
    version = db.Column(db.String(20), nullable=False)
    current_api_id = db.Column(db.Integer, db.ForeignKey('api.id'))
    current_api = db.relationship("Api", backref=db.backref("contexts"))
    def __repr__(self):
        return f'id={self.id}, chat_id={self.chat_id}'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get(chat_id, client):
        return ChatContext.query.filter_by(chat_id = chat_id, client = client).first()
