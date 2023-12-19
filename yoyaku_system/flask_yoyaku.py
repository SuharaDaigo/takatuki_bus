from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yoyaku_seki.db'
db = SQLAlchemy(app)

class Bus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    busid = db.Column(db.Integer, nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    seats = db.Column(db.Integer,nullable=False)

class Seat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    bus_id = db.Column(db.Integer, nullable=False) # Bus.idを入れている
    '''user_id = db.Column(db.String(100), nullable=True)'''
    reservations = db.relationship('Reservation', backref='seat', lazy=True)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    '''person_name = db.Column(db.String(50), nullable=False)'''
    seat_number = db.Column(db.Integer, db.ForeignKey('seat.number'), nullable=False)
    bus_id = db.Column(db.Integer, db.ForeignKey('bus.id'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

with app.app_context():
    db.create_all()

#時間の処理
def process_datetime_input(datetime_str):
    try:
        parts = datetime_str.split(' ')
        date_parts = parts[0].split('/')
        month = int(date_parts[0])
        day = int(date_parts[1])
        time_str = parts[1]

        current_year = datetime.now().year
        current_month = datetime.now().month

        if current_month > 9 and month <= 9:
            current_year += 1

        bus_time_object = datetime(current_year, month, day, int(time_str.split(':')[0]),int(time_str.split(':')[1]))
        return bus_time_object
    except (ValueError, IndexError):
        raise ValueError("日時の入力形式が無効です。")
    
#kanriで入力されたものをテーブルに入れている
def add_bus_and_seats(seattype, bus_time_object):
    with app.app_context():

        print(bus_time_object)
        existing_bus = Bus.query.filter_by(departure_time=bus_time_object).order_by(Bus.busid.desc()).first()
        if existing_bus:
            new_busid = existing_bus.busid + 1
        else:
            new_busid = 1
        
        #バスの正席処理　proj_takatukibusの荻野先生の過去発言参照
        a=0
        if seattype == 28:
            a = 22
        elif seattype == 24:
            a = 19

        # 新しいバスを作成
        new_bus = Bus(busid=new_busid, departure_time=bus_time_object,seats=a)
        db.session.add(new_bus)
        db.session.commit()

        nwbid = Bus.query.filter_by(id=new_bus.id).first()
        # バスに関連する22個のシートを作成
        for seat_number in range(1, a + 1):
            new_seat = Seat(number=seat_number, bus_id=nwbid.id)
            db.session.add(new_seat)
            db.session.commit()
        return nwbid.id

@app.route('/kanri')
def kanri():
    return render_template('kanri.html')

@app.route('/kanri/register', methods=['POST'])
def register():
    try:
        bus_time_str = request.form['datetime']
        seattype = int(request.form['seat_number'])
        name_booked = request.form['name_booked']

        bus_time_object = process_datetime_input(bus_time_str)
        bus_id = add_bus_and_seats(seattype, bus_time_object)

        if name_booked:
            reserevd_seats = [int(seat)for seat in name_booked.split(',')]
            for seat_number in reserevd_seats:
                seat = Seat.query.filter_by(bus_id = bus_id, number=seat_number).first()
                print(seat_number, seat.id , seat.number)
                if seat:
                    reservation = Reservation(seat_number=seat.number, user_id=str(bus_id), bus_id=bus_id)
                    db.session.add(reservation)
                    db.session.commit()
                else:
                    return f'エラー：指定された座席がありません'
        return redirect(url_for('kanri'))
    except ValueError as e:
        return f'エラー: {str(e)}'

    return redirect(url_for('choice'))

@app.route('/')
def kanricancel():
    

#ここから個人ページの処理

@app.route('/')
def personal():
    username = "test"
    current_time = datetime.now().time()
    firstbus = db.session.query(Bus).filter(Bus.departure_time > current_time).order_by(Bus.departure_time).all()
    if firstbus:
        closest_bus = firstbus[0]
        total_seats = closest_bus.seats
        reserved_seats = db.session.query(Reservation).filter_by(bus_id=closest_bus.id).count()
        available_seats = total_seats - reserved_seats

        print(f"Closest Bus - Bus ID: {closest_bus.id}, Departure Time: {closest_bus.departure_time}, Available Seats: {available_seats}")
    else:
        print("No upcoming buses.")
    return render_template('personal.html', name=username)

@app.route('/choice')
def choice():
    bus_date = db.session.query(Bus).order_by(Bus.departure_time).all()
    seat_date = db.session.query(Seat).all()
    busseat = {}
    if len(bus_date) != 0:
        for bus in bus_date:
            total_seats = bus.seats
            reserved_seats = db.session.query(Reservation).filter_by(bus_id = bus.id).count()
            available_seats = total_seats - reserved_seats
            busseat[bus] = available_seats
    else:
        return "バス情報がありません"
    return render_template('choice.html', bus_date=bus_date , busseat = busseat)

@app.route('/choice/<bnum>')
def seat(bnum):
    busid = bnum
    seat_date = db.session.query(Seat).filter_by(bus_id=busid).all()
    reservation_date = db.session.query(Reservation).filter_by(bus_id = busid).all()

    i = 0
    reservedtf = []
    for seat in seat_date:
        reserved = any(reservation.seat_number == seat.number for reservation in reservation_date)
        reservedtf.append('1' if reserved else '0')
    return render_template('bnum.html', seat_date = seat_date, reservedtf = reservedtf, bnum = busid)

@app.route('/choice/<bnum>/reserve', methods=['POST'])
def reserve(bnum):
    busid = bnum
    #USer名を保存情報として持つ
    booked = request.form['seat_number']
    seat = Seat.query.filter_by(bus_id = busid, number=booked).first()
    print(booked, seat.id , seat.number)
    if seat:
        reservation = Reservation(seat_number=seat.number, user_id='test', bus_id=bnum)
        db.session.add(reservation)
        db.session.commit()
    else:
        return f'エラー：指定された座席がありません'
    return redirect(url_for('seat', bnum=bnum))

@app.route('/cancel')
def cancel():
    #Userid = reservationのUseridが一致する ex)User_id = db.session.query(reservation).filter_by(Userid = Userid).all()
    #reservation_date = db.session.query(Reservation).filter_by(User_id = Userid).all()
    return render_template('cancel.html')

@app.route('/cancel/register')
def cancelregister():
    return redirect(url_for('personal'))