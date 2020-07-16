from datetime import datetime

from line_app import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.Integer, nullable=False)  # 0: inactive, 1: active
    line_user_id = db.Column(db.String(255), index=True, nullable=False, unique=True)
    current_node = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    def __init__(self, status, line_user_id, current_node):
        self.status = status
        self.line_user_id = line_user_id
        self.current_node = current_node

    def to_dict(self):
        return {
            'id': self.id,
            'status': self.status,
            'line_user_id': self.line_user_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def commit_db(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def find_by_line_user_id(cls, user_id):
        users = db.session.query(User.id).filter(User.line_user_id==user_id).limit(1).all()

        return users