from flask import Flask,request,url_for,render_template,redirect,session
from flask_pymongo import PyMongo
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017')
db = client['Login_Database']

#app.config['MONGO_URI'] = 'mongodb://localhost:27017'
#mongo = PyMongo(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/homepage')
def main():
    return render_template('homepage.html')


@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        if request.form['fullname'] and request.form['Email'] and request.form['password']:
            users=db.users
            existing_user = users.find_one({'Email':request.form['Email']})
            if existing_user is None:
                users.insert({'fullname' : request.form['fullname'], 'Email':request.form['Email'], 'password': request.form['password']})
                return redirect(url_for('signin'))
            else:
                return 'that email already exist!'
        else:
            return 'enter valid details'
    else:
        return render_template('signup.html')



@app.route('/signin',methods=['POST','GET'])
def signin():
    if request.method == 'POST':
        users = db.users
        existing_user = users.find_one({'Email':request.form['Email']})
        if existing_user is None:
            return redirect(url_for('signup'))
        else:
            if request.form['password'] == existing_user['password']:
                session['fullname'] = existing_user['fullname']
                return redirect(url_for('main'))
            else:
                return 'invalid details...'
    else:
        return render_template('signin.html')

@app.route('/handlesession')
def handlesession():
    session.clear()
    return redirect(url_for('signin'))

if __name__ == "__main__":
    app.secret_key='arun'
    app.run(debug=True)