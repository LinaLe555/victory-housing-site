import sqlite3

connect = sqlite3.connect("win_house.db", check_same_thread=False)
cursor = connect.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS profession(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profession VARCHAR(30) NOT NULL
               )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS employees(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name VARCHAR(130) NOT NULL,
            phone VARCHAR(12),
            experience DECIMAL(10, 2),
            profession INTEGER,
            FOREIGN KEY(profession) REFERENCES profession (id)
               )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS type_object(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(50)
               )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS object(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(30),
            description TEXT,
            employ INTEGER, 
            price FLOAT,
            type INTEGER,
            FOREIGN KEY(employ) REFERENCES employees (id),
            FOREIGN KEY(type) REFERENCES type_object (id)
               )""")


connect.commit()

def getprofessions():
    cursor.execute('select * from profession')
    return cursor.fetchall()

def createprofession(profession):
    cursor.execute('insert into profession(profession) values(?)', [profession])
    connect.commit()

def createstaff(name,phone,profession,experience):
    cursor.execute('insert into employees (full_name,phone,profession,experience) values(?,?,?,?)',[name,phone,profession,experience])
    connect.commit()

def getemployees():
    cursor.execute('select * from employees')
    return cursor.fetchall() 

def gettype_object():
    cursor.execute('select * from type_object')
    return cursor.fetchall()

def  createtype(type_object):
    cursor.execute('insert into type_object(name) values(?)', [type_object])
    connect.commit()

def createobject (name,description,employe,type, price):
    cursor.execute('insert into object (name,description,employ,type, price) values(?,?,?,?,?)',[name,description,employe,type, price])
    connect.commit()

def getobjects():
    cursor.execute('select * from object')
    return cursor.fetchall()

def gethome():
    cursor.execute('select * from object, type_object where type_object.name = "Дом" and type_object.id = object.type')
    return cursor.fetchall()

def getgarages():
    cursor.execute('select * from object, type_object where type_object.name = "Гараж" and type_object.id = object.type')
    return cursor.fetchall()

def getapartament():
    cursor.execute('select * from object, type_object where type_object.name = "Квартира" and type_object.id = object.type')
    return cursor.fetchall()

def getplot():
    cursor.execute('select * from object, type_object where type_object.name = "Участок" and type_object.id = object.type')
    return cursor.fetchall()

def getother():
    cursor.execute('select * from object, type_object where type_object.name != "Участок" and type_object.name != "Квартира" and type_object.name != "Гараж" and type_object.name != "Дом" and type_object.id = object.type ')
    return cursor.fetchall()

def getbyfiltr(name,desc,employee,type,price):
    query=f'''select * from object where {f"name like '%{name}%'" if name else 1} and {f"description like '%{desc}%'" if desc else 1} and {f"employ = {employee}" if employee else 1} and {f"type = {type}" if type else 1} and {f"price >= {price}" if price else 1 } '''
    cursor.execute(query)
    return cursor.fetchall()