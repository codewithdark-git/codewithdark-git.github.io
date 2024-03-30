from flask import Flask, request, render_template, jsonify
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure email settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send-email', methods=['POST'])
def send_email():
    # Extract form data from request
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']

    # Create Message object
    msg = Message(subject,
                  sender=email,
                  recipients=[os.getenv('MAIL_USERNAME')])  # Replace with recipient's email address
    msg.body = f'From: {name}\nEmail: {email}\nMessage: {message}'

    # Send email
    try:
        mail.send(msg)
        return jsonify(message='Email sent successfully'), 200
    except Exception as e:
        error_message = str(e)
        return jsonify(message=error_message), 500


if __name__ == '__main__':
    app.run(debug=True)
