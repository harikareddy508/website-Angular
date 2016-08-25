#!/usr/bin/env python

#standard libraries
from datetime import datetime
from flask import Flask, request, send_from_directory, jsonify
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy

#utility functions
from constants import Methods
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appointment.db'

db = SQLAlchemy(app)


"""
    SQlAlchemy magic happening here. I am using this library to map objects to sql and vice versa
"""


class Appointment(db.Model):
    id = db.Column('appointment_id', db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(100))
    date = db.Column(db.Date)
    time = db.Column(db.Time)

    def __init__(self, appointmentData):
        self.description = appointmentData['description']
        self.date = datetime.strptime(appointmentData['date'], '%m-%d-%Y').date()
        self.time = datetime.strptime(appointmentData['time'], '%H:%M:%S').time()

    def serialize(self):
        return {'id': self.id,
                'description': self.description,
                'date': self.date.strftime('%m-%d-%Y'),
                'time': self.time.strftime('%H:%M:%S')
                }


"""
    Method called for /. We check whether we are getting any query params as part of request, if we get any we will send
    json if not we render index.html
"""


@app.route('/')
def index():
    # checking whether we are getting query params as part of request
    if len(request.args) > 0:
        appointments = Appointment.query.filter(Appointment.description.like('%'+str(request.args['search'])+'%')).all()
        if not appointments:
            appointments = []
        return jsonify(appointments=[appointment.serialize() for appointment in appointments])

    else:
        return render_template('index.html')


"""
    Method which will be triggered for form submission
"""


@app.route('/', methods=[Methods.POST])
def add_appointment():
    # checking whether we are submitting empty form
    if len(request.json) > 0:
        appointment = Appointment(request.json)
        db.session.add(appointment)
        db.session.commit()
        return jsonify({'status': True, 'appointment': appointment.serialize()})
    else:
        return render_template('index.html')


"""
    Method which will serve JS files located in css directory using send_from_directory
"""


@app.route('/js/<path>')
def send_js(path):
    return send_from_directory('js', path)


"""
    Method which will serve CSS files located in css directory using send_from_directory
"""


@app.route('/css/<path>')
def send_css(path):
    return send_from_directory('css', path)


if __name__ == '__main__':
    app.run()
