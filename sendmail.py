import os
from flask_mail import Mail, Message
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import FileField, StringField, validators
app = Flask(__name__)
# from Project import current_user
import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'saitej9705@gmail.com',
	MAIL_PASSWORD = '123134325'
	)
mail = Mail(app)

class FileForm(FlaskForm):
    file_ = FileField('Some file')
    addr = StringField('Address', [validators.InputRequired()])

# @app.route('/',methods=["POST","GET"])
def send_mail(service,date,app,current_user):
	try:
		print('current_user\n\n\n\n',current_user.name)
		import os
		SECRET_KEY = os.urandom(32)
		app.config['SECRET_KEY'] = SECRET_KEY
		app.config.update(
			DEBUG=True,
			#EMAIL SETTINGS
			MAIL_SERVER='smtp.gmail.com',
			MAIL_PORT=465,
			MAIL_USE_SSL=True,
			MAIL_USERNAME = 'saitej9705@gmail.com',
			MAIL_PASSWORD = '123134325'
			)
		mail = Mail(app)

		to = service.email
		subject = "booking info"
		message = """<h3>hai ,services</h3>
					<h4>Cus_Name:"""+current_user.name+"""</h4>
					<h4>Cus_Contact:_____</h4>
					<h4>Cus_Mailid:"""+current_user.email+"""</h4>



					
							we got one mail request"""%(str(date))
		print("\n\n\n\n",to,subject,message)
		# image = request.files['file']
		# print("file\n\n\n\n",image)
		msg = Message(subject,
		  sender="noreply@testing@gmail.com",
		  recipients=[to])
		msg.html = message
		print("\n\nbefore sent")
		# with app.open_resource("download.jpg") as fp:
		mail.send(msg)
		print("\n\n\n\nexecuted scuccessfully")
		return ' Successfully Mail sent!'
	except Exception as e:
		print("Errorrrrrr\n\n:"+str(e)) 

def send_mail_user(service,date,app,current_user):
	try:
		print('current_user\n\n\n\n',current_user.name)
		import os
		SECRET_KEY = os.urandom(32)
		app.config['SECRET_KEY'] = SECRET_KEY
		app.config.update(
			DEBUG=True,
			#EMAIL SETTINGS
			MAIL_SERVER='smtp.gmail.com',
			MAIL_PORT=465,
			MAIL_USE_SSL=True,
			MAIL_USERNAME = 'saitej9705@gmail.com',
			MAIL_PASSWORD = '123134325'
			)
		mail = Mail(app)

		to = current_user.email
		subject = "booking info"
		message = """<h1>Thanks for chating with us</h1>
					<p>we have forwarded your details to your choosen service on date:"""+str(date)+""",<br>For more information about the services.Please contact the service provider</p>

					DETAILS:-
					         <h3>Service provider_Name:"""+service.name+"""</h3>
					         <h3>Service provider_Contact:"""+service.contact+"""</h3>
					         <h3>Service provider_Mailid:"""+service.email+"""</h3><br>
					         


					         <h3>BOOKING HAS CONFIRMED!</h3>

					         <div style="border:3px solid grey;width: 300px"> 

					         	<p> # for any issues,Please feel free to<br>
					         		inform us at saitej.m.ca@gmail.com<br>or<br>
					         		call us at 9705705686
					         	
					         </div>
					         """
		print("\n\n\n\n",to,subject,message)
		# image = request.files['file']
		# print("file\n\n\n\n",image)
		msg = Message(subject,
		  sender="noreply@testing@gmail.com",
		  recipients=[to])
		msg.html = message
		print("\n\nbefore sent")
		# with app.open_resource("download.jpg") as fp:
		mail.send(msg)
		print("\n\n\n\nexecuted scuccessfully")
		return ' Successfully Mail sent!'
	except Exception as e:
		print("Errorrrrrr\n\n:"+str(e))
