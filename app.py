import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

# --- App Initialization and Configuration ---

# Get the absolute path of the directory containing this script
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# --- Database Configuration ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'appointments.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Mail Configuration ---
# IMPORTANT: Set your email and password as environment variables in your terminal
# export MAIL_USERNAME='your-email@gmail.com'
# export MAIL_PASSWORD='your-gmail-app-password'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
mail = Mail(app)


# --- Database Model ---
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    service = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Appointment for {self.name}>'


# --- Routes ---

@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')


@app.route('/book-appointment', methods=['POST'])
def book_appointment():
    """Receives booking data, saves it to the database, and sends an email notification."""
    data = request.get_json()

    if not all(key in data for key in ['name', 'email', 'service', 'date', 'time']):
        return jsonify({'message': 'Missing data in request'}), 400

    new_appointment = Appointment(
        name=data['name'],
        email=data['email'],
        service=data['service'],
        date=data['date'],
        time=data['time']
    )

    try:
        # Save to database
        db.session.add(new_appointment)
        db.session.commit()

        # Send email notification to yourself
        msg_title = f"New Booking Request from {data['name']}"
        sender = app.config['MAIL_USERNAME']
        msg = Message(msg_title, sender=sender, recipients=[sender])
        msg.body = f"""
        You have a new appointment request:

        Name:    {data['name']}
        Email:   {data['email']}
        Service: {data['service']}
        Date:    {data['date']}
        Time:    {data['time']}
        """
        mail.send(msg)
        
        return jsonify({'message': 'Your appointment has been successfully requested!'}), 201

    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}") # Log the error for debugging
        return jsonify({'message': 'An error occurred while booking.'}), 500


# --- Run Application ---

if __name__ == '__main__':
    # Creates the database and tables if they don't exist before running the app
    with app.app_context():
        db.create_all()
    app.run(debug=True)