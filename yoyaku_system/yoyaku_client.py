from flask import Flask, render_template, url_for, jsonify, redirect, request
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'
API_URL = "http://127.0.0.1:5000"  # Web API の URL

@app.route('/kanri')
def kanri():
    return render_template('kanri.html')

@app.route('/kanri/register')
def register():
    bus_time_str = request.form['datetime']
    seattype = int(request.form['seat_number'])
    name_booked = request.form['name_booked']
    requests.post(f"{API_URL}/kanri/register", json={'datetime': bus_time_str, 'seta_number': seattype, 'name_booked': name_booked})
    return redirect(url_for('kanri'))

@app.route('/')
def personal():
    name = "test"
    return render_template('personal.html', name=name)

if __name__ == '__main__':
    app.run(port=8000)
