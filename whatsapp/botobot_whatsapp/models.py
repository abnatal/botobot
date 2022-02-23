from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy import and_
from botobot_whatsapp.ext.database import db

class GupshupMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    payload = db.Column(MutableDict.as_mutable(db.JSON), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    message_id = db.Column(db.String(40), nullable=True)
    message_event_type = db.Column(db.String(40), nullable=True)
    whatsapp_id = db.Column(db.String(40), nullable=True)
    sender_phone = db.Column(db.String(40), nullable=True)
    sender_name = db.Column(db.String(40), nullable=True)
    destination = db.Column(db.String(40), nullable=True)
    outbound = db.Column(db.Boolean, nullable=False)
    response_code = db.Column(db.Integer, nullable=True)
    dt = db.Column(db.DateTime, nullable=False)
    def __repr__(self):
        return f'id={self.id}'

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @staticmethod
    def get_message_enqueued(message_id):
        return GupshupMessage.query.filter(and_(GupshupMessage.message_id == message_id, GupshupMessage.type == 'message-event', GupshupMessage.message_event_type.isnot(None))).first()
