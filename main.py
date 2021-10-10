from flask import Flask, render_template, url_for, jsonify, request, redirect
from flask.wrappers import Request
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class RPiSensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=True, unique=True)
    description = db.Column(db.String(200),nullable=True)
    value = db.Column(db.Float,nullable=False)
    active = db.Column(db.Boolean,nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<RPiSensor %r' % self.id

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def get_variable():
    variable="aaaa"
    return variable

@app.route('/')
def index():
    get_first = RPiSensor.query.get_or_404(1)
    get_first.value = get_first.value+1

    try:
        db.session.commit()
    except:
        pass
    return render_template("index.html")

@app.route('/scan/<int:id>')
def check(id):
    return render_template("check.html", id=id)

@app.route('/add', methods=['POST','GET'])
def add():
    if request.method == 'POST':
        sensor_active = False
        sensor_name = request.form['name']
        sensor_description = request.form['description']
        sensor_value = request.form['value']
        try:
            if request.form['active'] == 'on':
                sensor_active=True
        except:
            pass
        
        new_sensor = RPiSensor(name=sensor_name,description=sensor_description,value=sensor_value, active=sensor_active)
        
        try:
            db.session.add(new_sensor)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error - db adding'
    else:
        return render_template("add.html")

@app.route('/device/<int:id>')
def device(id):
    obj = {}
    obj['name'] = RPiSensor.query.get_or_404(id).name
    obj['value'] = RPiSensor.query.get_or_404(id).value
    obj['active'] = RPiSensor.query.get_or_404(id).active
    return jsonify(obj)

@app.route('/devices', methods=["GET"])
def devices():
    devices = RPiSensor.query.order_by(RPiSensor.date_created).all()
    return render_template('devices.html', devices=devices)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)


    