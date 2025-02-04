from flask import Flask, request, jsonify, render_template
from geopy.geocoders import Nominatim 
import googlemaps
from twilio.rest import Client
from dotenv import load_dotenv
import re
import os

load_dotenv()
app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize APIs
gmaps = googlemaps.Client(key=app.config['GOOGLE_MAPS_API_KEY'])
twilio_client = Client(app.config['TWILIO_ACCOUNT_SID'], app.config['TWILIO_AUTH_TOKEN'])

# Database simulation
users = {
    'user1': {
        'trusted_contacts': ['+911234567890'],
        'last_location': None
    }
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def handle_chat():
    data = request.json
    user_message = data['message'].lower()
    user_id = data.get('user_id', 'user1')  # Add authentication in real system
    
    response = {
        'message': '',
        'emergency': False,
        'location': None
    }

    # Emergency Detection
    if detect_emergency(user_message):
        location = get_precise_location()
        send_emergency_sms(user_id, location)
        response.update({
            'message': '🚨 Emergency alert sent to contacts and authorities!',
            'emergency': True,
            'location': location
        })
        return jsonify(response)

    # Handle Normal Requests
    if 'location' in user_message:
        response['location'] = get_precise_location()
        response['message'] = f"Your current location: {response['location']}"
    
    elif 'tip' in user_message:
        response['message'] = get_safety_tips()
    
    elif 'contact' in user_message:
        response['message'] = "Emergency contacts: " + ", ".join(app.config['EMERGENCY_CONTACTS'])
    
    else:
        response['message'] = "I can help with: Location sharing, Safety tips, Emergency contacts"

    return jsonify(response)

def detect_emergency(text):
    emergency_keywords = ['help', 'danger', 'attack', 'emergency', 'save me']
    return any(keyword in text for keyword in emergency_keywords)

def get_precise_location():
    # Use HTML5 Geolocation in production (simulated here)
    try:
        location = gmaps.geolocate()
        return gmaps.reverse_geocode((location['location']['lat'], location['location']['lng']))[0]['formatted_address']
    except:
        return "Unable to fetch location"

def send_emergency_sms(user_id, location):
    for number in app.config['EMERGENCY_CONTACTS'] + users[user_id]['trusted_contacts']:
        twilio_client.messages.create(
            body=f"EMERGENCY ALERT! User at {location}",
            from_='+TWILIO_NUMBER',  # Your Twilio number
            to=number
        )

if __name__ == '__main__':
    app.run(ssl_context='adhoc', debug=True)  # HTTPS for location access