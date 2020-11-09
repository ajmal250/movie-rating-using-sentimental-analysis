import matplotlib
from flask import Flask, render_template, request, session, redirect, url_for
from flaskext.mysql import MySQL
from jedi.api.refactoring import inline
from textblob import TextBlob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from string import punctuation
from collections import Counter


app = Flask(__name__)


mysql = MySQL()
app.secret_key = 'your secret key'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'movie'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route("/")
def main():
    return render_template('index.html')


@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/signup")
def signup():
    return render_template('signup.html')


@app.route('/signup', methods=['POST'])
def signuppost():
    name = request.form['uname']
    password=request.form['password']
    cpass = request.form['cpassword']
    if name =='':
        exe='enter user name!!!'
    elif password =='':
        exe='enter password!!!'
    elif password == cpass and name !='' and password!='':
        conn=mysql.connect()
        cur=conn.cursor()
        #cur.execute('''SELECT MAX(userid) FROM user''')
        #maxid=cur.fetchone()
        cur.execute('''INSERT INTO user (username,password) VALUES (%s,%s)''',(name,password))
        cur.close()
        exe='user : '+name+' created'
    else:
        exe='incorrect password!!!'
    return render_template('signup.html',data=exe)


@app.route("/contact")
def contact():
    return render_template('contact.html')


@app.route("/movie")
def movie():
    return render_template('movie.html')


@app.route('/rating')
def rating():
    return render_template('rating.html')


@app.route('/rating', methods=['POST'])
def ratingpost():
    text = request.form['text']
    processed_text = TextBlob(text).sentiment.polarity
    return render_template('rating.html', mydata=processed_text)


@app.route('/userrating')
def userrating():
    return render_template('userrating.html')


@app.route('/usermovie')
def usermovie():
    return render_template('usermovie.html')


@app.route('/userrating',methods=['POST'])
def userratingpost():
    text = request.form['text']
    processed_text = TextBlob(text).sentiment.polarity
    return render_template('userrating.html', mydata=processed_text)



@app.route("/login")
def login():
    #conn = mysql.connect()
    #cur =conn.cursor()
    #cur.execute("SELECT * from users")
    #result = cursor.fetchall()
    #cursor.close()
    return render_template('login.html')


@app.route('/login',methods=['POST'])
def logincheck():
    name=request.form['uname']
    password=request.form['password']
    msg=''
    if name!='' and password !='':
        conn=mysql.connect()
        cur=conn.cursor()
        cur.execute('''SELECT * FROM user WHERE username=%s AND password=%s''',(name,password))
        account = cur.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            return render_template('user.html')
        else:
            msg='Incorrect username/password!'
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route('/user')
def userpage():
    return render_template('user.html')


@app.route("/about")
def about():
    id='2'
    conn = mysql.connect()
    #cur = conn.cursor()
    #cur.execute('''SELECT comment FROM comment WHERE movieid=%s''', (movieid))
    #data = cur.fetchall()
    #df=pd.DataFrame(data, columns=cur.)
    sql='''SELECT comment FROM comment WHERE movieid='''+id
    df = pd.read_sql(sql=sql, con=conn)

    return render_template('about.html',mydata=df)


@app.route("/userabout")
def usercontact():
    return render_template('contactuser.html')

@app.route("/admin")
def adminlog():
    return render_template('adminlogin.html')

@app.route('/admin',methods=['POST'])
def adminlogin():
    name=request.form['uname']
    password=request.form['password']
    msg=''
    if name!='' and password !='':
        conn=mysql.connect()
        cur=conn.cursor()
        cur.execute('''SELECT * FROM user WHERE username=%s AND password=%s AND type=1''',(name,password))
        account = cur.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            return render_template('adminpage.html')
        else:
            msg='Incorrect username/password!'
    return render_template('adminlogin.html', msg=msg)

@app.route('/addmovie')
def addmovie():
    return render_template('addmovie.html')

@app.route('/editmovie')
def editmovie():
    return render_template('editmovie.html')

@app.route('/viewuser')
def viewuser():
    return render_template('viewuser.html')

@app.route('/deletemovie')
def deletemovie():
    return render_template('deletemovie.html')

@app.route('/ratemovie')
def ratemovie():
    return render_template('ratemovie.html')


@app.route('/adminpage')
def adminpage():
    return render_template('adminpage.html')



if __name__ == "__main__":
    app.run(debug=True)
