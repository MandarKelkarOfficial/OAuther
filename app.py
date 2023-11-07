import random
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_data.db'
db = SQLAlchemy(app)

def generate_otp():
    return str(random.randint(10000, 99999))



# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    # created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# Function to encrypt the password using SHA-256
def encrypt_password(password):
    return sha256_crypt.hash(password)
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(name=name).first()
        
        if user:
            # Verify the hashed password
            if sha256_crypt.verify(password, user.password):
                send_otp_to_email(user.email)
                # Successful login
                return render_template('otp1.html')
            else:
                # Password doesn't match
                return 'Login failed. Please check your username and password.'
        else:
            # User not found
            return 'Login failed. User not found. Please check your username and password.'

    return render_template('login.html')


@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        dob = request.form['dob']
        email = request.form['email']
        password = request.form['password']
        mobile = request.form['mobile']
        # otp = request.form['otp']

        # Encrypt the password
        hashed_password = encrypt_password(password)

        # Create a new user and add it to the database
        new_user = User(name=name, dob=dob, email=email, password=hashed_password, mobile=mobile)
        db.session.add(new_user)
        db.session.commit()
        
        
       

        return render_template('login.html')
    
    return render_template('signup.html')


@app.route('/otp', methods=['POST'])
def otp():
    if request.method == 'POST':
        user_otp = request.form['otp']  # Get the OTP entered by the user

        if user_otp == otp:  # Compare the user's OTP with the generated OTP
            print("true")  # Print "true" if the OTPs match
            return render_template('welcome.html')
        else:
            print("false")  # Print "false" if the OTPs do not match

    return render_template('otp1.html')


def send_otp_to_email(receiver_email):
    # Sender's email and password
    sender_email = "sdbcontactme@gmail.com"
    sender_password = "fywacjgevdugsgtz"

    # Generate an OTP
    global otp
    otp = generate_otp()

    # Create the message with the OTP
    message_body = f"Your OTP is: {otp}"
    subject = "OTP Verification"

    # Create an email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(message_body, "plain"))

    # Set up the SMTP server and send the email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print(f"OTP sent to {receiver_email}")
    except Exception as e:
        print(f"Failed to send OTP: {e}")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
