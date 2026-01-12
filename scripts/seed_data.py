"""Seed database with sample data for Azerbaijani doctors in Germany."""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models.doctor import Doctor
from dotenv import load_dotenv

load_dotenv()

# Sample data for Azerbaijani doctors in Germany
SAMPLE_DOCTORS = [
    {
        'name': 'Dr. Leyla Mammadova',
        'specialties': ['Cardiology', 'Internal Medicine'],
        'languages': ['Azerbaijani', 'German', 'English', 'Turkish'],
        'address': 'Friedrichstraße 123',
        'city': 'Berlin',
        'postal_code': '10117',
        'latitude': 52.5200,
        'longitude': 13.4050,
        'phone': '+49 30 12345678',
        'email': 'leyla.mammadova@example.com',
        'business_hours': {
            'Monday': '09:00 - 18:00',
            'Tuesday': '09:00 - 18:00',
            'Wednesday': '09:00 - 18:00',
            'Thursday': '09:00 - 18:00',
            'Friday': '09:00 - 18:00',
            'Saturday': '10:00 - 14:00',
            'Sunday': 'Closed'
        },
        'rating': 4.9,
        'review_count': 128,
        'google_maps_url': 'https://maps.app.goo.gl/example1',
        'bio': 'Experienced cardiologist with over 15 years of practice. Specializes in preventive cardiology and heart disease management.'
    },
    {
        'name': 'Dr. Elvin Aliyev',
        'specialties': ['Pediatrics'],
        'languages': ['Azerbaijani', 'German', 'English', 'Russian'],
        'address': 'Marienplatz 45',
        'city': 'Munich',
        'postal_code': '80331',
        'latitude': 48.1351,
        'longitude': 11.5820,
        'phone': '+49 89 98765432',
        'email': 'elvin.aliyev@example.com',
        'business_hours': {
            'Monday': '08:00 - 17:00',
            'Tuesday': '08:00 - 17:00',
            'Wednesday': '08:00 - 17:00',
            'Thursday': '08:00 - 17:00',
            'Friday': '08:00 - 17:00',
            'Saturday': 'Closed',
            'Sunday': 'Closed'
        },
        'rating': 5.0,
        'review_count': 84,
        'google_maps_url': 'https://maps.app.goo.gl/example2',
        'bio': 'Pediatrician dedicated to providing comprehensive care for children. Fluent in Azerbaijani, German, and English.'
    },
    {
        'name': 'Dr. Aysel Hasanova',
        'specialties': ['Dermatology'],
        'languages': ['Azerbaijani', 'German', 'English', 'Turkish'],
        'address': 'Speicherstadt 12',
        'city': 'Hamburg',
        'postal_code': '20457',
        'latitude': 53.5511,
        'longitude': 9.9937,
        'phone': '+49 40 55512345',
        'email': 'aysel.hasanova@example.com',
        'business_hours': {
            'Monday': '10:00 - 19:00',
            'Tuesday': '10:00 - 19:00',
            'Wednesday': '10:00 - 19:00',
            'Thursday': '10:00 - 19:00',
            'Friday': '10:00 - 19:00',
            'Saturday': '10:00 - 16:00',
            'Sunday': '11:00 - 15:00'
        },
        'rating': 4.7,
        'review_count': 210,
        'google_maps_url': 'https://maps.app.goo.gl/example3',
        'bio': 'Board-certified dermatologist specializing in skin conditions and cosmetic dermatology.'
    },
    {
        'name': 'Dr. Ramin Ismayilov',
        'specialties': ['General Practice', 'Family Medicine'],
        'languages': ['Azerbaijani', 'German', 'English'],
        'address': 'Zeil 89',
        'city': 'Frankfurt',
        'postal_code': '60313',
        'latitude': 50.1109,
        'longitude': 8.6821,
        'phone': '+49 69 44455566',
        'email': 'ramin.ismayilov@example.com',
        'business_hours': {
            'Monday': '08:00 - 18:00',
            'Tuesday': '08:00 - 18:00',
            'Wednesday': '08:00 - 18:00',
            'Thursday': '08:00 - 18:00',
            'Friday': '08:00 - 18:00',
            'Saturday': '09:00 - 13:00',
            'Sunday': 'Closed'
        },
        'rating': 4.8,
        'review_count': 156,
        'google_maps_url': 'https://maps.app.goo.gl/example4',
        'bio': 'Family physician providing comprehensive primary care for all ages. Experienced in treating Azerbaijani-speaking patients.'
    },
    {
        'name': 'Dr. Nigar Mammadli',
        'specialties': ['Neurology'],
        'languages': ['Azerbaijani', 'German', 'English', 'Russian'],
        'address': 'Hohe Straße 34',
        'city': 'Cologne',
        'postal_code': '50667',
        'latitude': 50.9375,
        'longitude': 6.9603,
        'phone': '+49 221 77788899',
        'email': 'nigar.mammadli@example.com',
        'business_hours': {
            'Monday': '09:00 - 17:00',
            'Tuesday': '09:00 - 17:00',
            'Wednesday': '09:00 - 17:00',
            'Thursday': '09:00 - 17:00',
            'Friday': '09:00 - 17:00',
            'Saturday': 'Closed',
            'Sunday': 'Closed'
        },
        'rating': 4.6,
        'review_count': 92,
        'google_maps_url': 'https://maps.app.goo.gl/example5',
        'bio': 'Neurologist specializing in headache disorders, epilepsy, and neurodegenerative diseases.'
    },
    {
        'name': 'Dr. Tural Huseynov',
        'specialties': ['Orthopedics', 'Sports Medicine'],
        'languages': ['Azerbaijani', 'German', 'English', 'Turkish'],
        'address': 'Königstraße 67',
        'city': 'Stuttgart',
        'postal_code': '70173',
        'latitude': 48.7758,
        'longitude': 9.1829,
        'phone': '+49 711 33344455',
        'email': 'tural.huseynov@example.com',
        'business_hours': {
            'Monday': '08:00 - 18:00',
            'Tuesday': '08:00 - 18:00',
            'Wednesday': '08:00 - 18:00',
            'Thursday': '08:00 - 18:00',
            'Friday': '08:00 - 18:00',
            'Saturday': '10:00 - 14:00',
            'Sunday': 'Closed'
        },
        'rating': 4.9,
        'review_count': 187,
        'google_maps_url': 'https://maps.app.goo.gl/example6',
        'bio': 'Orthopedic surgeon and sports medicine specialist. Expert in joint replacement and sports injuries.'
    },
    {
        'name': 'Dr. Sevinj Aliyeva',
        'specialties': ['Gynecology', 'Obstetrics'],
        'languages': ['Azerbaijani', 'German', 'English', 'Russian'],
        'address': 'Unter den Linden 78',
        'city': 'Berlin',
        'postal_code': '10117',
        'latitude': 52.5163,
        'longitude': 13.3777,
        'phone': '+49 30 22233344',
        'email': 'sevinj.aliyeva@example.com',
        'business_hours': {
            'Monday': '09:00 - 17:00',
            'Tuesday': '09:00 - 17:00',
            'Wednesday': '09:00 - 17:00',
            'Thursday': '09:00 - 17:00',
            'Friday': '09:00 - 17:00',
            'Saturday': 'Closed',
            'Sunday': 'Closed'
        },
        'rating': 4.8,
        'review_count': 143,
        'google_maps_url': 'https://maps.app.goo.gl/example7',
        'bio': 'Gynecologist and obstetrician providing comprehensive women\'s health care. Fluent in Azerbaijani and German.'
    },
    {
        'name': 'Dr. Orkhan Mammadov',
        'specialties': ['Psychiatry', 'Psychotherapy'],
        'languages': ['Azerbaijani', 'German', 'English', 'Turkish'],
        'address': 'Maximilianstraße 23',
        'city': 'Munich',
        'postal_code': '80539',
        'latitude': 48.1351,
        'longitude': 11.5820,
        'phone': '+49 89 66677788',
        'email': 'orkhan.mammadov@example.com',
        'business_hours': {
            'Monday': '10:00 - 19:00',
            'Tuesday': '10:00 - 19:00',
            'Wednesday': '10:00 - 19:00',
            'Thursday': '10:00 - 19:00',
            'Friday': '10:00 - 19:00',
            'Saturday': 'Closed',
            'Sunday': 'Closed'
        },
        'rating': 4.7,
        'review_count': 98,
        'google_maps_url': 'https://maps.app.goo.gl/example8',
        'bio': 'Psychiatrist and psychotherapist specializing in mood disorders, anxiety, and cross-cultural mental health.'
    }
]


def seed_database():
    """Seed the database with sample data."""
    database_url = os.getenv('DATABASE_URL', 'sqlite:///database/healthcare.db')
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Check if data already exists
        existing_count = session.query(Doctor).count()
        if existing_count > 0:
            print(f"Database already contains {existing_count} doctors. Skipping seed.")
            return
        
        # Add sample doctors
        for doctor_data in SAMPLE_DOCTORS:
            doctor = Doctor(**doctor_data)
            session.add(doctor)
        
        session.commit()
        print(f"Successfully seeded {len(SAMPLE_DOCTORS)} doctors.")
    except Exception as e:
        session.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        session.close()


if __name__ == '__main__':
    seed_database()
