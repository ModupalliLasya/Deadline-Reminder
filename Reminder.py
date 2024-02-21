from flask import Flask, render_template, request, flash
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
app = Flask(__name__, template_folder='E:\IEEE\DeadLine Reminder\templates')

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345-67890'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'lasyasujith4@gmail.com'  # Replace with your Gmail address
app.config['MAIL_PASSWORD'] = 'qyotssewooywvphv'  # Replace with your Gmail password

mail = Mail(app)

def send_reminder(recipient, subject, body, deadline_datetime):
    with app.app_context():
        msg = Message(subject, sender='lasyasujith4@gmail.com', recipients=[recipient])
        msg.body = f'{body}\n\nDeadline: {deadline_datetime.strftime("%Y-%m-%d %H:%M")}'
        mail.send(msg)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set_reminder', methods=['POST'])
def set_reminder():
    recipient_email = request.form.get('recipient_email')
    subject = request.form.get('subject')
    deadline_date = request.form.get('deadline_date')
    deadline_time = request.form.get('deadline_time')

    # Convert deadline_date and deadline_time to datetime object
    deadline_datetime = datetime.strptime(f'{deadline_date} {deadline_time}', '%Y-%m-%d %H:%M')

    # Schedule the reminder one day before the deadline
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(send_reminder, 'date', run_date=deadline_datetime - timedelta(days=1),
                      args=[recipient_email, subject, 'Reminder for your deadline', deadline_datetime])

    flash('Reminder set successfully. You will receive a reminder one day before the deadline.', 'success')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
