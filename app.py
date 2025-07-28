# app.py

import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

# --- Database Setup ---
# Get the absolute path of the directory containing this script
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# Configure the SQLite database, naming it 'appointments.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'appointments.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database object
db = SQLAlchemy(app)

# --- Database Model ---
# This class defines the structure of the 'appointment' table in our database
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

# Main route to serve the single-page application
@app.route('/')
def index():
    return render_template('index.html')

# Booking route that receives form data from the new frontend
@app.route('/book-appointment', methods=['POST'])
def book_appointment():
    # Get the JSON data sent from the JavaScript fetch call
    data = request.get_json()

    # Basic validation to ensure all required data is present
    if not all(key in data for key in ['name', 'email', 'service', 'date', 'time']):
        return jsonify({'message': 'Missing data in request'}), 400

    # Create a new Appointment object using the data
    new_appointment = Appointment(
        name=data['name'],
        email=data['email'],
        service=data['service'],
        date=data['date'],
        time=data['time']
    )

    # Add the new appointment to the database session and commit to save it
    try:
        db.session.add(new_appointment)
        db.session.commit()
        # Return a success message
        return jsonify({'message': 'Your appointment has been successfully requested!'}), 201
    except Exception as e:
        # If there's an error, roll back the session and return an error message
        db.session.rollback()
        print(f"Database Error: {e}")
        return jsonify({'message': 'An error occurred while booking.'}), 500

# This runs the app when you execute 'python3 app.py'
if __name__ == '__main__':
    # This block ensures the database and tables are created before the app starts
    with app.app_context():
        db.create_all()
    app.run(debug=True)