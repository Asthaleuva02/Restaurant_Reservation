import os
import json
import logging
from flask import Flask
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Ensure data directory exists
if not os.path.exists('data'):
    os.makedirs('data')

# Initialize data files if they don't exist
data_files = {
    'data/menu.json': {
        'appetizers': [
            {
                'id': 1,
                'name': 'Bruschetta',
                'description': 'Toasted bread topped with fresh tomatoes, basil, and garlic',
                'price': 8.99
            },
            {
                'id': 2,
                'name': 'Calamari',
                'description': 'Crispy fried squid served with marinara sauce',
                'price': 12.99
            },
            {
                'id': 3,
                'name': 'Caprese Salad',
                'description': 'Fresh mozzarella, tomatoes, and basil drizzled with balsamic glaze',
                'price': 10.99
            }
        ],
        'main_courses': [
            {
                'id': 4,
                'name': 'Spaghetti Carbonara',
                'description': 'Classic pasta with eggs, cheese, pancetta, and black pepper',
                'price': 16.99
            },
            {
                'id': 5,
                'name': 'Grilled Salmon',
                'description': 'Fresh salmon fillet with lemon herb butter and seasonal vegetables',
                'price': 22.99
            },
            {
                'id': 6,
                'name': 'Chicken Parmesan',
                'description': 'Breaded chicken breast topped with marinara and mozzarella, served with pasta',
                'price': 18.99
            },
            {
                'id': 7,
                'name': 'Ribeye Steak',
                'description': '12oz ribeye cooked to perfection with roasted potatoes',
                'price': 28.99
            }
        ],
        'desserts': [
            {
                'id': 8,
                'name': 'Tiramisu',
                'description': 'Classic Italian coffee-flavored dessert',
                'price': 8.99
            },
            {
                'id': 9,
                'name': 'Chocolate Lava Cake',
                'description': 'Warm chocolate cake with a molten center, served with vanilla ice cream',
                'price': 9.99
            },
            {
                'id': 10,
                'name': 'Cheesecake',
                'description': 'New York style cheesecake with berry compote',
                'price': 8.99
            }
        ],
        'drinks': [
            {
                'id': 11,
                'name': 'House Wine (Glass)',
                'description': 'Red or white house selection',
                'price': 7.99
            },
            {
                'id': 12,
                'name': 'Craft Beer',
                'description': 'Selection of local craft beers',
                'price': 6.99
            },
            {
                'id': 13,
                'name': 'Italian Soda',
                'description': 'Flavored sparkling beverage',
                'price': 4.99
            }
        ]
    },
    'data/tables.json': [
        {'id': 1, 'name': 'Table 1', 'capacity': 2},
        {'id': 2, 'name': 'Table 2', 'capacity': 2},
        {'id': 3, 'name': 'Table 3', 'capacity': 4},
        {'id': 4, 'name': 'Table 4', 'capacity': 4},
        {'id': 5, 'name': 'Table 5', 'capacity': 6},
        {'id': 6, 'name': 'Table 6', 'capacity': 6},
        {'id': 7, 'name': 'Table 7', 'capacity': 8},
        {'id': 8, 'name': 'Table 8', 'capacity': 8}
    ],
    'data/reservations.json': [],
    'data/restaurant_info.json': {
        'name': 'Bella Cucina',
        'tagline': 'Authentic Italian Cuisine',
        'address': '123 Main Street, Anytown, AN 12345',
        'phone': '(555) 123-4567',
        'email': 'info@bellacucina.com',
        'hours': {
            'Monday': '11:00 AM - 9:00 PM',
            'Tuesday': '11:00 AM - 9:00 PM',
            'Wednesday': '11:00 AM - 9:00 PM',
            'Thursday': '11:00 AM - 9:00 PM',
            'Friday': '11:00 AM - 10:00 PM',
            'Saturday': '10:00 AM - 10:00 PM',
            'Sunday': '10:00 AM - 9:00 PM'
        },
        'social_media': {
            'facebook': 'https://facebook.com/bellacucina',
            'instagram': 'https://instagram.com/bellacucina',
            'twitter': 'https://twitter.com/bellacucina'
        },
        'about': 'Bella Cucina brings the heart of Italy to your table with authentic recipes passed down through generations. Our chefs use only the finest ingredients to create memorable dining experiences in a warm, inviting atmosphere.',
        'services': [
            'Dine-in',
            'Takeout',
            'Online Reservations',
            'Private Events',
            'Catering'
        ]
    }
}

for file_path, default_data in data_files.items():
    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            json.dump(default_data, f, indent=4)

# Import routes after app initialization
from routes import *

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
