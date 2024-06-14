from flask import *
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import datetime
import userclass
import connentclass

app = Flask(__name__)

app.config['DATABASE']='db1.db'
def connect_db():
    db=getattr(g,'_database',None)
    if db is None:
        db=g._database=sqlite3.connect(app.config['DATABASE'])
    return db

'''with app.app_context():
    db=connect_db()'''

#app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db1.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)

@app.route('/',methods=["GET","POST"])
def index():
    if request.method=="POST":
        username = request.form.get("username")
        password = request.form.get("password")
        '''try:
            query = text("select * from users where username='" + username + "' and password='" + password + "'")
            result = db.session.execute(query)
            data = result.fetchall()
        except Exception as e:
            app.logger.error(f"Database connection error: {e}")
            return jsonify({'error': 'Database connection error'}), 500'''
        db=connect_db()
        mycursor=db.cursor()
        result=mycursor.execute("select * from users where username='" + username + "' and password='" + password + "'")
        data=result.fetchall()
        if len(data)==0:
            return "Invalid username or password"
        elif data[0][5]==2:
            cutime = datetime.datetime.now()
            '''query1=text("insert into logintime(id_user, name, familyname, datetime) values('"+str(data[0][0])+"','"+data[0][1]+"','"+data[0][2]+"','"+str(cutime)+"')")
            db.session.execute(query1)
            db.session.commit()'''
            mycursor.execute("insert into logintime(id_user, name, familyname, datetime) values('"+str(data[0][0])+"','"+data[0][1]+"','"+data[0][2]+"','"+str(cutime)+"')")
            db.commit()
            return render_template("home.html", name=data[0][2], familyname=data[0][1], age=data[0][2])
        else:
            cutime=datetime.datetime.now()
            '''query2=text("insert into logintime(id_user, name, familyname, datetime) values('" + str(data[0][0]) + "','" +
                       data[0][1] + "','" + data[0][2] + "','" + str(cutime) + "')")
            db.session.execute(query2)
            db.session.commit()'''
            mycursor.execute("insert into logintime(id_user, name, familyname, datetime) values('" + str(data[0][0]) + "','" +
                       data[0][1] + "','" + data[0][2] + "','" + str(cutime) + "')")
            db.commit()
            UserClass=userclass.User()
            data1=UserClass.select_user(db)
            return render_template("admin.html",data1=data1,data=data,name=data[0][1],familyname=data[0][2])
        return render_template("index.html")
    else:
        return render_template("index.html")

@app.route('/admin',methods=["GET","POST"])
def admin():
    if request.method=="POST":
        id=request.form.get("id")
        field=request.form.get("field")
        value=request.form.get("value")
        '''query=text("update users set '"+field+"'='"+value+"' where id='"+id+"'")
        db.session.execute(query)
        db.session.commit()'''
        db=connect_db()
        mycursor=db.cursor()
        mycursor.execute("update users set '"+field+"'='"+value+"' where id='"+id+"'")
        db.commit()
        UserClass=userclass.User()
        data1=UserClass.select_user(db)
        return render_template("admin.html",data1=data1)
    else:
        return render_template("admin.html")

if __name__ == '__main__':
    app.run()
