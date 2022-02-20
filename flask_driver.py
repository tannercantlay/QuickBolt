from app import app, db, mail
from app.models import *

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'OrderInfo': OrderInfo, 'PaymentInfo': PaymentInfo}