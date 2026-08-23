import os
from functools import wraps

from flask import (Flask, render_template, redirect, make_response, request,
                   url_for, flash)
from flask_login import (LoginManager, login_user, logout_user, login_required,
                         current_user)

from config import * 
from data import *

from user import *
from forms import LoginForm, RegistrForm

from werkzeug.utils import secure_filename


app = Flask(__name__)

app.config['SECRET_KEY'] = '555'
app.config['UPLOAD_FOLDER'] = 'static/avataras'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

def admin_requed(func):
    @wraps(func)
    def decor(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        if not current_user.is_admin():
            return redirect(url_for('index'))
        return func(*args, **kwargs)
    return decor

@login_manager.user_loader
def load_user(username):
    return User.get(username)

@app.route('/')
@app.route('/index')
def main():
    objects = getobjects()
    return render_template("main.html", objects=objects)

@app.route('/object/<int:arg>')
def object(arg):
    item = get_object(arg)

    return render_template("object.html", item=item)

@app.route('/addstaff/', methods=['GET','POST'])
@admin_requed
def addstaff():
    if request.method=='GET':
        professions = getprofessions()
        return render_template("addstaff.html", professions=professions)
    name = request.form.get('name')
    phone = request.form.get('phone')
    profession = request.form.get('profession')
    experience = request.form.get('experience')

    createstaff(name, phone, profession, experience)
    return redirect('/addstaff/')

@app.route('/addprofession/', methods=['POST'])
@admin_requed
def addprofession():
    profession = request.form.get('profession')
    createprofession(profession)
    return redirect ('/addstaff/')

@app.route('/addobject/', methods=['GET','POST'])
@admin_requed
def addobject():
    if request.method=='GET':
        employees = getemployees()
        type_object = gettype_object()
        return render_template("addobject.html", employees=employees, type_object=type_object)
    name = request.form.get('name')
    description = request.form.get('description')
    employe = request.form.get('employe')
    type = request.form.get('type')
    price = request.form.get('price')
    createobject(name, description, employe, type, price)
    return redirect('/addobject/')


@app.route('/addtype/', methods=['POST'])
@admin_requed
def addtype():
    name = request.form.get('name')
    createtype(name)
    return redirect ('/addobject/')

@app.route('/hometype/')
def hometype():
    objects = gethome()
    return render_template('hometype.html', objects=objects)


@app.route('/apartamenttype/')
def apartamenttype():
    objects = getapartament()
    return render_template('apartamenttype.html', objects=objects)


@app.route('/plottype/')
def plottype():
    objects = getplot()
    return render_template('plottype.html', objects=objects)


@app.route('/garagestype/')
def garagestype():
    objects = getgarages()
    return render_template('garagestype.html', objects=objects)

@app.route('/othertype/')
def othertype():
    objects = getother()
    return render_template('other.html', objects=objects)

@app.route('/filtr/')
def filtr():
    emploes=getemployees()
    type_object=gettype_object()
    return render_template('filtr.html', employees=emploes, type_object=type_object)

@app.route('/getbyfiltr/', methods=['POST'])
def getfiltr():
    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()  # исправлено название поля
    employee = request.form.get('employe', '').strip()
    type_object = request.form.get('type', '').strip()
    price = request.form.get('price', '').strip()

    # Преобразуем пустые строки в None для корректной работы фильтра
    objects = getbyfiltr(
        name if name else None,
        description if description else None,
        int(employee) if employee and employee.isdigit() else None,
        int(type_object) if type_object and type_object.isdigit() else None,
        float(price) if price else None
    )

    return render_template('objectsbyfiltr.html', objects=objects)

@app.route('/login', methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)
        if user:
            login_user(user)
            return redirect(url_for('main'))
    return render_template('login.html', form=form)

@app.route('/registr', methods=['POST','GET'])
def registr():
    if current_user.is_authenticated:
        return redirect(url_for('main'))
    form = RegistrForm()
    if form.validate_on_submit():
        if  userbylogin(form.username.data)==[]:
            userbyregister(form.username.data, form.password.data, 'user')
            user = User.authenticate(form.username.data, form.password.data)
            login_user(user)
            return redirect(url_for('main'))
        else:
            flash(['Такой логин уже занят!', 'red'])
            return render_template('register.html', form=form)
    return render_template('register.html', form=form)


@app.route('/profile', methods=['POST','GET'])
def profile():
    if current_user.is_authenticated:
        img = current_user.getAvataras()
        return render_template('profile.html', avatar=img)
    
@app.route('/admin', methods=['POST','GET'])
def admin():
    if current_user.is_authenticated:
        return render_template('admin.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/changepassword', methods=['POST','GET'])
def changepassword():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if request.method=='POST':
        newpassword = str(request.form.get('newpassword'))
        oldpassword = str(request.form.get('oldpassword'))
        if newpassword != '' and oldpassword != '':
            if newpassword != oldpassword:
                if current_user.check_password(oldpassword):
                    current_user.update_password(newpassword)
    return render_template('changepassword.html')


@app.route('/changeavataras', methods=['POST'])
def changeavataras():
    file = request.files['img']
    if file and file.filename:
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        changeavatar(current_user.username,path)
        return redirect(url_for('profile'))
    
@app.route('/choesavatar', methods=['POST'])
def choesavatar():
    action = request.form.get('action')
    if action == 'photo1':
      changeavatar(current_user.username, 'static/avatarus/photo_2026-07-26_01-02-35 copy 2.jpg')
    elif action == 'photo2':
      changeavatar(current_user.username, 'static/avatarus/худойарс.jpg')
    elif action == 'photo3':
          changeavatar(current_user.username, 'static/avatarus/жиробасарс.jpg')
    return redirect(url_for('profile'))

@app.route('/helpwrite', methods=['POST','GET'])
def heilwrite():
    if request.method=='POST':
        topic = request.form.get('topic')
        message = request.form.get('message')
        name = request.form.get('name')
        helpwrite(current_user.id,topic,message,name)
    return render_template('helpwrite.html')

@app.route('/tikets',methods=['POST','GET'])
@admin_requed
def tikets():
    d = gettikets()
    return render_template('tikets.html', tikets=d)

@app.route('/suppochat/<int:chat>', methods=['POST','GET'])
def suppochat(chat):
    return render_template('suppochat.html', chat=chat)

# Получить сообщения
@app.route('/api/suppochat/<int:chat>/messages')
def get_chat_messages(chat):
    messages = get_message(chat)

    result = []

    for i in messages:
        result.append({
            'id': message[0],
            'ticket_id': message[1],
            'user_id': message[2],
            'text': message[3],
            'date': message[4]
        })

    return jsonify(result)

# Отправить сообщение
@app.route('/api/suppochat/<int:chat>/messages', methods=['POST'])
def send_chat_message(chat):
    data_json = request.get_json()

    text = data_json.get('text', '').strip()

    if not text:
        return jsonify({
            'error': 'Сообщение пустое'
        }), 400

    add_message(chat, current_user.id, text)

    return jsonify({'success': True})

if __name__ ==  "__main__":
    app.run(debug=True)
