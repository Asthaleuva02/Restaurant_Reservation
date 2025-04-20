import os
import json
import uuid
import logging
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, jsonify, session
from app import app
from models import Reservation, ContactMessage

# Add this function to be used in templates
@app.template_filter('now')
def _jinja2_filter_now():
    return datetime.utcnow()

# Helper function to read JSON data
def read_json_file(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error reading {file_path}: {e}")
        return {}

# Helper function to write JSON data
def write_json_file(file_path, data):
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        logging.error(f"Error writing to {file_path}: {e}")
        return False

# Route for home page
@app.route('/')
def home():
    restaurant_info = read_json_file('data/restaurant_info.json')
    return render_template('home.html', info=restaurant_info)

# Route for menu page
@app.route('/menu')
def menu():
    menu_data = read_json_file('data/menu.json')
    restaurant_info = read_json_file('data/restaurant_info.json')
    return render_template('menu.html', menu=menu_data, info=restaurant_info)

# Route for booking page
@app.route('/booking')
def booking():
    restaurant_info = read_json_file('data/restaurant_info.json')
    return render_template('booking.html', info=restaurant_info)

# API to check table availability
@app.route('/api/check-availability', methods=['POST'])
def check_availability():
    data = request.json
    date = data.get('date')
    time = data.get('time')
    guests = int(data.get('guests', 2))
    
    # Read tables and reservations
    tables = read_json_file('data/tables.json')
    reservations = read_json_file('data/reservations.json')
    
    # Filter reservations for the requested date and time
    existing_reservations = [r for r in reservations if r['date'] == date and r['time'] == time]
    reserved_table_ids = [r['table_id'] for r in existing_reservations]
    
    # Find available tables that can accommodate the party size
    available_tables = [t for t in tables if t['id'] not in reserved_table_ids and t['capacity'] >= guests]
    
    # Sort tables by capacity to assign the most appropriate sized table
    available_tables.sort(key=lambda x: x['capacity'])
    
    return jsonify({
        'available': len(available_tables) > 0,
        'tables': available_tables
    })

# Route to create a reservation
@app.route('/api/book', methods=['POST'])
def book_table():
    data = request.json
    
    # Validate required fields
    required_fields = ['name', 'email', 'phone', 'date', 'time', 'guests', 'table_id']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'success': False, 'message': f"Missing required field: {field}"})
    
    # Read current reservations
    reservations = read_json_file('data/reservations.json')
    
    # Check if table is already booked
    for reservation in reservations:
        if (reservation['date'] == data['date'] and 
            reservation['time'] == data['time'] and 
            reservation['table_id'] == data['table_id']):
            return jsonify({'success': False, 'message': "This table is already booked for the selected time."})
    
    # Create new reservation
    reservation_id = str(uuid.uuid4())
    new_reservation = {
        'id': reservation_id,
        'name': data['name'],
        'email': data['email'],
        'phone': data['phone'],
        'date': data['date'],
        'time': data['time'],
        'guests': int(data['guests']),
        'table_id': data['table_id'],
        'special_requests': data.get('special_requests', ''),
        'status': 'confirmed',
        'created_at': datetime.now().isoformat()
    }
    
    # Add to reservations and save
    reservations.append(new_reservation)
    if write_json_file('data/reservations.json', reservations):
        return jsonify({
            'success': True, 
            'message': "Reservation confirmed!",
            'reservation_id': reservation_id
        })
    else:
        return jsonify({'success': False, 'message': "An error occurred while saving your reservation."})

# Route for booking confirmation
@app.route('/confirmation/<reservation_id>')
def confirmation(reservation_id):
    reservations = read_json_file('data/reservations.json')
    restaurant_info = read_json_file('data/restaurant_info.json')
    tables = read_json_file('data/tables.json')
    
    # Find the reservation
    reservation = next((r for r in reservations if r['id'] == reservation_id), None)
    
    if not reservation:
        flash("Reservation not found.", "danger")
        return redirect(url_for('booking'))
    
    # Get table information
    table = next((t for t in tables if t['id'] == reservation['table_id']), None)
    
    return render_template('confirmation.html', 
                          reservation=reservation, 
                          table=table, 
                          info=restaurant_info)

# Route for contact page
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    restaurant_info = read_json_file('data/restaurant_info.json')
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # Validate form data
        if not all([name, email, subject, message]):
            flash("Please fill out all fields", "danger")
            return render_template('contact.html', info=restaurant_info)
        
        # Create contact message object
        contact_message = ContactMessage(
            id=str(uuid.uuid4()),
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        # Save message to file (in a real app, you'd email this or save to database)
        # For simplicity, we'll just flash a success message
        flash("Your message has been sent! We'll get back to you soon.", "success")
        return redirect(url_for('contact'))
    
    return render_template('contact.html', info=restaurant_info)

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    restaurant_info = read_json_file('data/restaurant_info.json')
    return render_template('base.html', info=restaurant_info, error="Page not found"), 404

@app.errorhandler(500)
def server_error(e):
    restaurant_info = read_json_file('data/restaurant_info.json')
    return render_template('base.html', info=restaurant_info, error="Server error"), 500
