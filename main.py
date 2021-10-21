import pdb
from flask import Flask, render_template, url_for, jsonify, request, redirect
from flask.wrappers import Request
from flask_socketio import SocketIO, emit
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from RGBDiode import RPiRGBDiode
from TempHum import DHT11

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
socketio = SocketIO(app)
socketio.init_app(app,cors_allowed_origins="*")

class RPiSensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=True, unique=True)
    description = db.Column(db.String(100),nullable=True)
    pin = db.Column(db.Integer,nullable=True, unique=True)
    pin1 = db.Column(db.Integer,nullable=True)
    pin2 = db.Column(db.Integer,nullable=True)
    pin3 = db.Column(db.Integer,nullable=True)
    device_type = db.Column(db.String(20), nullable=False)
    values = db.Column(db.String(200), nullable=True)
    output = db.Column(db.Boolean,nullable=False)
    active = db.Column(db.Boolean,nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

cors = CORS(app)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/scan/<int:id>')
def check(id):
    obj = {}
    obj['device_type'] = RPiSensor.query.get_or_404(id).device_type

    if obj['device_type'] == 'rgbdiode':
        return render_template("checkrgb.html", id=id)
    elif obj['device_type'] == 'dht11':
        return render_template("checkdht11.html", id=id)
    else:
        return render_template("check.html", id=id)

@app.route('/add', methods=['POST','GET'])
def add():
    
    if request.method == 'POST':
        sensor_output = False
        sensor_active = False
        sensor_pin = 0
        pin1 = 0
        pin2 = 0
        pin3 = 0
        sensor_name = request.form['name']
        sensor_description = request.form['description']
        device_type = request.form['device_type']
        try:
            if request.form['active'] == 'on':
                sensor_active=True
            if request.form['output'] == 'on':
                sensor_output=True
        except:
            print("Disregarding active/output from /add form.")
        new_sensor = {}
        if device_type == 'rgbdiode':
            
            
            pin1 = request.form['pin1']
            pin2 = request.form['pin2']
            pin3 = request.form['pin3']
            new_sensor = RPiSensor(name=sensor_name,
                                    description=sensor_description,
                                    active=sensor_active,
                                    output=sensor_output,
                                    pin1=pin1,
                                    pin2=pin2,
                                    pin3=pin3,
                                    device_type=device_type)
        else:
            
            sensor_pin = request.form['pin']
            new_sensor = RPiSensor(name=sensor_name,
                                    description=sensor_description,
                                    active=sensor_active,
                                    output=sensor_output,
                                    pin=sensor_pin,
                                    device_type=device_type)
        try:
            db.session.add(new_sensor)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error - db adding'
    else:
        return render_template("add.html")

@socketio.on('dht_data',namespace='/dht')
def handleDHTDataSocker(id):
    obj = {}

    device = RPiSensor.query.get_or_404(id)
    try:
        dht11 = DHT11(device.pin)
    except:
        print("Could not create new object (DHT11 from /device/)")

    temp_val = dht11.temperature()
    humi_val = dht11.humidity()
    device.values = str(temp_val)+','+str(humi_val)
    try:
        db.session.commit()
    except:
        return 'Error ID: '+id+' - failure.'
    obj['name'] = device.name
    obj['values'] = str(device.values)
    obj['active'] = device.active
    emit('dht_data', obj)

@app.route('/device/<int:id>')
def device(id):
    obj = {}
    device = RPiSensor.query.get_or_404(id)
    if device.device_type == 'dht11':
        try:
            dht11 = DHT11(device.pin)
        except:
            print("Could not create new object (DHT11 from /device/)")
        temp_val = dht11.temperature()
        humi_val = dht11.humidity()
        device.values = str(temp_val)+','+str(humi_val)
        try:
            db.session.commit()
        except:
            return 'Error ID: '+id+' - failure.'
        
        del dht11
        
    obj['name'] = device.name
    obj['values'] = str(device.values)
    obj['active'] = device.active
    return jsonify(obj)

@app.route('/set/<int:id>', methods=["POST",'GET'])
def set(id):
    if request.method == 'POST':
        data = request.get_json()
        device = RPiSensor.query.get_or_404(id)
        red_value = data['red']
        green_value = data['green']
        blue_value = data['blue']
        device.values = red_value+','+green_value+','+blue_value
        try:
            diode = RPiRGBDiode(device.pin1,device.pin2,device.pin3)
        except:
            print("Could not create new object (RPiRGBDiode from /set/)")
        diode.setColor(device.values)
        try:
            db.session.commit()
            return "Correct!"
        except:
            return 'Error ID: '+id+' - failure.'
    else:
        return 'None'

@app.route('/devices', methods=["GET"])
def devices():
    devices = RPiSensor.query.order_by(RPiSensor.date_created).all()
    return render_template('devices.html', devices=devices)


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0',port=5000, debug=True)

