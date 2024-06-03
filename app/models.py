from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin



class User(UserMixin, db.Model):
    id: so.Mapped[int] = db.Column(db.Integer, primary_key=True)
    username: so.Mapped[str] = db.Column(db.String(64), index=True, unique=True)
    email: so.Mapped[str] = db.Column(db.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = db.Column(db.String(128))

    def __repr__(self) -> str:
        return f'<User {self.id}:{self.username}>\n{self.email}\n{self.password_hash}'
    
    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id: int) -> User:
    return User.query.get(int(id))
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
    

    