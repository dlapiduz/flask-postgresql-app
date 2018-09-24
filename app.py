import os

from flask import Flask, request, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://%s:%s@%s/%s' % (
    # ARGS.dbuser, ARGS.dbpass, ARGS.dbhost, ARGS.dbname
    os.environ['DBUSER'], os.environ['DBPASS'], os.environ['DBHOST'], os.environ['DBNAME']
)

# initialize the database connection
db = SQLAlchemy(app)

# initialize database migration management
MIGRATE = Migrate(app, db)

from models import *


@app.route('/')
def view_registered_guests():
    guests = Guest.query.all()
    return render_template('guest_list.html', guests=guests)


@app.route('/register', methods = ['GET'])
def view_registration_form():
    return render_template('guest_registration.html')


@app.route('/register', methods = ['POST'])
def register_guest():
    name = request.form.get('name')
    email = request.form.get('email')
    partysize = request.form.get('partysize')
    if not partysize or partysize=='':
        partysize = 1

    guest = Guest(name, email, partysize)
    db.session.add(guest)
    db.session.commit()

    return render_template('guest_confirmation.html',
        name=name, email=email, partysize=partysize)
