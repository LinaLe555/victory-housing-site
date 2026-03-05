from flask import Flask, render_template, redirect, make_response, request
from config import * 
from data import *


app = Flask (__name__)

@app.route ('/')
def main():
    objects = getobjects()
    return render_template("main.html", objects=objects)

@app.route ('/addstaff/', methods=['GET','POST'])
def addstaff():
    if request.method=='GET':
        professions = getprofessions()
        return render_template("addstaff.html", professions=professions)
    name = request.form.get('name')
    phone = request.form.get('phone')
    profession = request.form.get('profession')
    experience = request.form.get('experience')
    createstaff(name,phone,profession,experience)
    return redirect('/addstaff/')

@app.route ('/addprofession/', methods=['POST'])
def addprofession():
    profession = request.form.get('profession')
    createprofession(profession)
    return redirect ('/addstaff/')

@app.route ('/addobject/', methods=['GET','POST'])
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
    createobject(name,description,employe,type, price)
    return redirect('/addobject/')


@app.route ('/addtype/', methods=['POST'])
def addtype():
    name = request.form.get('name')
    createtype(name)
    return redirect ('/addobject/')

@app.route ('/hometype/')
def hometype():
    objects = gethome()
    return render_template('hometype.html', objects = objects)


@app.route ('/apartamenttype/')
def apartamenttype():
    objects = getapartament()
    return render_template('apartamenttype.html', objects = objects)


@app.route ('/plottype/')
def plottype():
    objects = getplot()
    return render_template('plottype.html', objects = objects)


@app.route ('/garagestype/')
def garagestype():
    objects = getgarages()
    return render_template('garagestype.html', objects = objects)

@app.route ('/othertype/')
def othertype():
    objects = getother()
    return render_template('other.html', objects = objects)

@app.route ('/filtr/')
def filtr():
    emploes=getemployees()
    type_object=gettype_object()
    return render_template('filtr.html', employees=emploes, type_object=type_object)

@app.route ('/getbyfiltr/', methods=['POST'])
def getfiltr():
    name=request.form.get('name')
    desription=request.form.get('desription')
    employee=request.form.get('employe')
    type_object=request.form.get('type')
    price=request.form.get('price')
    objects=getbyfiltr(name,desription,employee,type_object,price)
    return render_template('objectsbyfiltr.html', objects=objects)


if __name__ ==  "__main__":
    app.run(debug=True)

