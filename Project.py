import flask
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from flask_mail import Mail, Message
from sqlalchemy import func
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import FileField, StringField, validators
from flask_socketio import SocketIO, emit
from flask_phantom_emoji import PhantomEmoji
import string
import os
import random
SECRET_KEY = os.urandom(32)
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
socketio = SocketIO(app)
app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'saitej9705@gmail.com',
	MAIL_PASSWORD = '123134325',
	
	)
mail = Mail(app)

app.config['SECRET_KEY']='chatapplication'
photos=UploadSet('photos', IMAGES)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import *

engine = create_engine("sqlite:///chatapp.db", 
	                    connect_args={'check_same_thread': False},
	                    echo=True)

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')


@app.route('/home')
def home():
	return render_template('home.html')


@app.route('/about')
def about():
       return render_template('about.html')


@app.route('/chat')
def chat():
       return render_template('chat.html')


@app.route('/login', methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('chat'))
	try:
		if request.method == "POST":
			owner=session.query(Owner).filter_by(email=request.form['email'],
				password=request.form['password']).first()
			print("\n\n\n\n", owner)
			if owner:
				login_user(owner)
				next_page=request.args.get('next')
				return redirect(next_page) if next_page else redirect(url_for('home'))
			else:
				flash("Login Failed, Please Check & Try Again ...!", "danger")
				return "else"
		else:
			return render_template("userlogin.html", title="Login")
	except Exception as e:
		print("\n\n\n\n\nerrorrrrrrrrrrrr", e)
		flash("Login Failed, Please Check & Try Again ...!", "danger")
		return render_template("userlogin.html", title="Login")


@app.route('/logout')
def logout():
	logout_user()
	return render_template("userlogin.html")


@app.route('/register', methods=["GET", "POST"])
def register():
	if request.method=="POST":
	   #user=session.query(User).filter_by(name=request.form['name'],email=request.form['email'],password=request.form['password']).first()
	   owner=session.query(Owner).filter_by(email=request.form['email']).first()
	   if not owner:
	   	owner=Owner(name=request.form['name'], email=request.form['email'], password=request.form['password'])
	   	session.add(owner)
	   	session.commit()
	   	return redirect('/login')
	   else:
	   	flash("User Already Exist")
	   	return render_template('registration.html')
	else:
	   	return render_template('registration.html')


@app.route('/resetPsw' , methods=['GET', 'POST'])
def resetPsw():
	if request.method == "GET":
		return render_template('reset_email.html')
	else:
		email = request.form['email']
		owner = session.query(Owner).filter_by(email=email).one_or_none()
		if not owner:
			flash('email not found')
			return redirect(url_for('home'))
		reply , token = sendEmail(email)
		if reply == True:
			reset_token = session.query(Reset_Token).filter_by(user_id=owner.id).one_or_none()
			if not reset_token:
				reset_token = Reset_Token(user_id=owner.id, token=token)
			else:
				reset_token.token = token
				session.add(reset_token)
				session.commit()
				flash('mail sent Successfully')
			return render_template('validateOTP.html', email=email)
		else:
			flash('email sent failed ')
		return redirect(url_for('home'))


@app.route('/verifytoken/', methods=['POST'])
def verifyToken():
	if request.method == 'POST':
		print('\n'*5, 'SAI', 'POST in verifyToken')
		email = request.form['email']
		received_token = request.form['utoken']
		owner = session.query(Owner).filter_by(email=email).one()
		owner.password = request.form['newpsw']
		session.commit()
		flash('password reset Successfully', "info")
		return redirect(url_for('home'))
	flash('something is wrong')
	return redirect(url_for('home'))


def sendEmail(email):
	try:
		to = email
		subject = "reset your password with in 30 min"
		token = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
		# flash('token '+token)
		message = "reset ur password by enter OTP  " + token
		print("\n\n\n\n", to,subject, message)

		# image = request.files['file']
		# print("file\n\n\n\n",image)
		msg = Message(subject,
			sender = ('hifromsender', 'saitej9705@gmail.com'),
		  recipients=[to])
		msg.body = message
		print('ok2') 
		# with app.open_resource("download.jpg") as fp:
		#msg.attach(form.file_.data.filename,
        #'application/octect-stream',
        #form.file_.data.read())
		#print("\n\n\n",msg)
		print('ok3')    
		mail.send(msg)
		return True, token
	except Exception as e:
		return False, (str(e)) 

def messageRecived():
  print('message was received!!!')


@socketio.on('my event')
def handle_my_custom_event(json):
  print('recived my event: ' + str(json))
  socketio.emit('my response', json, callback=messageRecived)


if __name__ == "__main__" :
	app.config['SECRET_KEY']='chatapplication'
	login_manager=LoginManager(app)
	login_manager.login_view='login'
	login_manager.login_message_category='info'

	@login_manager.user_loader
	def load_user(user_id):
		return session.query(Owner). get(int(user_id))
	app.debug = True
	socketio.run(app, debug=True)
	app.run(host='0.0.0.0', port=5000)

