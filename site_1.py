from flask import Flask, render_template, url_for, request, flash, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from create_db import DataBase, Bouquets, Papers, Tapes, Users, Orders
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from user_login import UserLogin
from datetime import datetime

engine = create_engine('sqlite:///bloom.db') 
DataBase.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()
app=Flask(__name__) 
app.config['SECRET_KEY'] = 'KseniyaGracheva'

login_manager = LoginManager(app)
login_manager.login_view = 'log_in'
login_manager.login_message = "Необходима авторизация"
login_manager.login_message_category = "success"

def addUser(username, hpsw):
    existing_username = session.query(Users).filter_by(user_email=username).first()
    if existing_username:
        # Если пользователь уже существует
        flash("Пользователь существует", "error")
        return False
    else:
        # Создание нового пользователя
        new_user = Users(user_email=username, user_password=hpsw)
        session.add(new_user)
        session.commit()
        return True

@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id)

@app.route("/")
@login_required
def index():
    return render_template('главная страница.html')

@app.route("/log_out")
@login_required
def log_out():
    logout_user()
    return render_template('log_in.html')

@app.route("/log_in", methods = ["POST", "GET"])
def log_in():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == "POST":
        user = session.query(Users).filter_by(user_email=request.form['username']).first()
        if user and check_password_hash(user.user_password, request.form['password']):
            userlogin = UserLogin().create(user)
            rm = True if request.form.get('rememberMe') else False
            login_user(userlogin, remember=rm)
            return redirect(url_for('index'))
        else:
            flash ("Неверный логин/пароль", "error")
    return render_template('log_in.html')

@app.route("/sign_up", methods = ["POST", "GET"])
def sign_up():
    if request.method == "POST":
        if request.form['username'] != "" and len(request.form['password']) > 4 \
        and request.form['password'] == request.form['password2']:
            hash = generate_password_hash(request.form['password'])
            res = addUser(request.form['username'], hash)
            if res:
                flash("Регистрация прошла успещно!", "success")
                return redirect(url_for('log_in'))
            else:
                flash("Ошибка при заполнении формы: проверьте длину пароля и совпадение", "error")
        else:
            flash("Неверно заполнены поля", "error")
    return render_template('sign_up.html')

@app.route("/bouquets", methods = ["POST", "GET"])
@login_required
def bouquets():
    if request.method == "POST":
        selected_bouquet = request.form.get('bouquet_id')
        return redirect(url_for('packing', selected_bouquet = selected_bouquet))
    bouquet1 = session.query(Bouquets).first()
    bouquet2 = session.query(Bouquets).offset(1).first()
    bouquet3 = session.query(Bouquets).offset(2).first()
    return render_template('готовые букеты.html', bouquet1 = bouquet1, bouquet2 = bouquet2, bouquet3 = bouquet3)

@app.route("/packing", methods = ["POST", "GET"])
@login_required
def packing():
    if request.method == "POST":
        selected_paper = request.form.get('paper_id')
        selected_bouquet = request.args.get('selected_bouquet')
        print(request.args)
        return redirect(url_for('tapes', selected_bouquet = selected_bouquet, selected_paper = selected_paper))
    packing1 = session.query(Papers).first()
    packing2 = session.query(Papers).offset(1).first()
    packing3 = session.query(Papers).offset(2).first()
    return render_template('упаковка.html', packing1 = packing1, packing2 = packing2, packing3 = packing3)

@app.route("/tapes", methods = ["POST", "GET"])
@login_required
def tapes():
    if request.method == "POST":
        selected_tape = request.form.get('tape_id')
        selected_paper = request.args.get('selected_paper')
        selected_bouquet = request.args.get('selected_bouquet')
        return redirect(url_for('basket', selected_tape = selected_tape, selected_paper = selected_paper, selected_bouquet = selected_bouquet))
    tape1 = session.query(Tapes).first()
    tape2 = session.query(Tapes).offset(1).first()
    tape3 = session.query(Tapes).offset(2).first()
    return render_template('ленты.html', tape1 = tape1, tape2 = tape2, tape3 = tape3)

@app.route("/basket", methods = ["POST", "GET"])
@login_required
def basket():
    
    selected_tape = request.args.get('selected_tape') 
    selected_paper = request.args.get('selected_paper') 
    selected_bouquet = request.args.get('selected_bouquet') 
    if request.method == "POST":
        t=str(request.form.get('time'))+':00'
        print(t)
        print(request.form.get('date'))
        order_one = Orders(
            user_id = current_user.get_id(),
            bouquet_id = selected_bouquet,
            paper_id = selected_paper,
            tape_id = selected_tape,
            day = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date(),
            time = datetime.strptime(t, '%H:%M:%S').time())
        
        session.add(order_one)
        session.commit()
        return redirect(url_for('order_complete'))

    existing_bouquet = session.query(Bouquets).filter_by(bouquet_id=selected_bouquet).first()
    existing_tape = session.query(Tapes).filter_by(tape_id=selected_tape).first()
    existing_paper = session.query(Papers).filter_by(paper_id=selected_paper).first()

    return render_template('корзина.html', existing_bouquet = existing_bouquet, existing_paper = existing_paper, existing_tape = existing_tape)

selected_boquet = None
selected_paper = None 
selected_tape = None

@app.route('/order_complete')
def order_complete():
    return render_template('order_complete.html')

if __name__=='__main__':
    app.run(debug=True)
