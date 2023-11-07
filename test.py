from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import random
from twilio.rest import Client
app = Flask(__name__)

account_sid = "ACf36c5b1de7ee6eb3c597b03050f83023"
auth_token = "51882c677f55cde2116e36b30d9c1873"

# Your routes
@app.route('/')
def index():
    return render_template("signup.html")

@app.route('/send_otp', methods=['GET','POST'])
def send_otp():
    if request.method == 'POST':
        ph_number = request.form["number"]
        val = getOTP_API(ph_number)
        
        if val:
            print("otp sent successfully")
    return render_template("index.html")
        
def getOTP_API(ph_number):  
    
    
    verify_sid = "VA304ee9cdcd2787c463625a474fc196e3"
    verified_number = "+919405926301"

    client = Client(account_sid, auth_token)
    otp = generate_otp()
    body = f"Your OTP is {str(otp)}"
    message = client.messages.create(
            body=f'Your OTP is: {otp}',
            from_="+12563636288",
            to=str(ph_number)
        )
    
    if message.sid:
        return True
    else:
        return False
    



        
# Function to generate a unique 4-digit OTP
def generate_otp():
    return random.randrange(1000,9999)

if __name__ == '__main__':
    app.run(debug=True)
