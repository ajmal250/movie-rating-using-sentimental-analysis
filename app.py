from flask import Flask,render_template,request
from flaskext.mysql import MySQL
from textblob import TextBlob

app = Flask(__name__)


mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'movie'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


#@app.route("/")
#def main():
#    return render_template('index.html')

#@app.route("/",methods='POST')
#def score():
 #   request.args.get('text')
 #   string=request.form['text']
  #  processed_text = string.upper()
   # return processed_text
    #string='very good'
    #analysis = TextBlob(string).sentiment.polarity
    #return render_template('index.html',mydata=analysis)


@app.route('/')
def my_form():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = TextBlob(text).sentiment.polarity
    return render_template('index.html',mydata=processed_text)


@app.route("/login")
def login():
    conn = mysql.connect()
    cursor =conn.cursor()

    cursor.execute("SELECT * from users")
    result = cursor.fetchall()
    cursor.close()
    return render_template('login.html', mydata=result)


if __name__ == "__main__":
    app.run(debug=True)
