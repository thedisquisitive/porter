import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db
from app.models import User, Order

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Order': Order, 'sa': sa, 'so': so}

# Path: porter.py