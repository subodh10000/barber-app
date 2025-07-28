# app.py

from flask import Flask, request, jsonify, render_template
import json

# Initialize the Flask app
app = Flask(__name__)

# A simple list to store our appointments in memory
# In a real app, you would save this to a database!
appointments = []

# This is the main route that sends the index.html file to the browser
@app.route('/')
def index():
    # Renders the HTML file from the 'templates' folder
    return render_template('index.html')

# This route provides a list of services to the frontend
@app.route('/api/services')
def get_services():
    services = [
        {"id": 1, "name": "Men's Haircut", "price": 30},
        {"id": 2, "name": "Beard Trim", "price": 15},
        {"id": 3, "name": "Haircut & Beard Trim", "price": 40},
        {"id": 4, "name": "Kid's Haircut", "price": 25}
    ]
    return jsonify(services)

# This route handles the booking form submission
@app.route('/api/book', methods=['POST'])
def book_appointment():
    # Get the booking data from the request
    booking_data = request.json
    
    # Print the data to the terminal to confirm it was received
    print(f"Received booking: {booking_data}")
    
    # Add the new booking to our list
    appointments.append(booking_data)
    
    # Send a success message back to the frontend
    return jsonify({"message": "Appointment booked successfully!"}), 201

# This runs the app when you execute the script
if __name__ == '__main__':
    app.run(debug=True)