from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class User(db.Model):
    id: so.Mapped[int] = db.Column(db.Integer, primary_key=True)
    username: so.Mapped[str] = db.Column(db.String(64), index=True, unique=True)
    email: so.Mapped[str] = db.Column(db.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = db.Column(db.String(128))

    def __repr__(self) -> str:
        return f'<User {self.username}>'
    
class Order(db.Model):
    id: so.Mapped[int] = db.Column(db.Integer, primary_key=True)
    user_id: so.Mapped[int] = db.Column(db.Integer, db.ForeignKey('user.id'))
    name: so.Mapped[str] = db.Column(db.String(120))
    description: so.Mapped[str] = db.Column(db.String(1200))
    tracking_number: so.Mapped[str] = db.Column(db.String(120))
    date: so.Mapped[str] = db.Column(db.String(120))
    price: so.Mapped[str] = db.Column(db.String(120))
    status: so.Mapped[str] = db.Column(db.String(120))


    def __repr__(self) -> str:
        return f'<Order {self.name}><br>{self.decription}<br>{self.tracking_number}<br>{self.date}<br>{self.price}<br>{self.status}'
    

    