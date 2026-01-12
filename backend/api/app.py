"""Flask API application for Healthcare Portal."""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from backend.models.doctor import Doctor, Base
from backend.utils.validation import validate_doctor_data, parse_address
from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
from geopy.distance import geodesic

load_dotenv()

app = Flask(__name__)
CORS(app)

# Database configuration
database_url = os.getenv('DATABASE_URL', 'sqlite:///database/healthcare.db')

# Create database directory if it doesn't exist
db_path = database_url.replace('sqlite:///', '')
if db_path.startswith('/'):
    db_dir = os.path.dirname(db_path)
else:
    db_dir = os.path.dirname(os.path.join(os.getcwd(), db_path))
if db_dir and not os.path.exists(db_dir):
    os.makedirs(db_dir)

# Initialize database
engine = create_engine(database_url)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def get_db_session():
    """Get database session."""
    return Session()


# ============================================================================
# PUBLIC API ENDPOINTS
# ============================================================================

@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    """Get list of doctors with optional filters."""
    session = get_db_session()
    try:
        # Get query parameters
        city = request.args.get('city', '').strip()
        specialty = request.args.get('specialty', '').strip()
        language = request.args.get('language', '').strip()
        search = request.args.get('search', '').strip()
        sort_by = request.args.get('sort_by', 'distance')  # distance, rating, name
        user_lat = request.args.get('lat', type=float)
        user_lng = request.args.get('lng', type=float)
        radius_km = request.args.get('radius', type=float, default=15.0)
        
        # Base query
        query = session.query(Doctor)
        
        # Apply filters
        if city:
            query = query.filter(Doctor.city.ilike(f'%{city}%'))
        
        if specialty:
            query = query.filter(Doctor.specialties.contains([specialty]))
        
        if language:
            query = query.filter(Doctor.languages.contains([language]))
        
        if search:
            query = query.filter(
                or_(
                    Doctor.name.ilike(f'%{search}%'),
                    Doctor.address.ilike(f'%{search}%')
                )
            )
        
        doctors = query.all()
        
        # Calculate distances if user location provided
        if user_lat and user_lng:
            for doctor in doctors:
                if doctor.latitude and doctor.longitude:
                    distance = geodesic(
                        (user_lat, user_lng),
                        (doctor.latitude, doctor.longitude)
                    ).kilometers
                    doctor._distance = distance
                else:
                    doctor._distance = None
            
            # Filter by radius
            doctors = [d for d in doctors if d._distance is None or d._distance <= radius_km]
        
        # Sort
        if sort_by == 'distance' and user_lat and user_lng:
            doctors = sorted(doctors, key=lambda d: d._distance if d._distance else float('inf'))
        elif sort_by == 'rating':
            doctors = sorted(doctors, key=lambda d: d.rating, reverse=True)
        elif sort_by == 'name':
            doctors = sorted(doctors, key=lambda d: d.name)
        
        # Convert to dict
        result = [doctor.to_dict() for doctor in doctors]
        
        # Add distance to result if calculated
        if user_lat and user_lng:
            for i, doctor in enumerate(doctors):
                if hasattr(doctor, '_distance') and doctor._distance is not None:
                    result[i]['distance'] = round(doctor._distance, 2)
        
        return jsonify({
            'count': len(result),
            'doctors': result
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


@app.route('/api/doctors/<int:doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    """Get doctor details by ID."""
    session = get_db_session()
    try:
        doctor = session.query(Doctor).filter_by(id=doctor_id).first()
        if not doctor:
            return jsonify({'error': 'Doctor not found'}), 404
        return jsonify(doctor.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


@app.route('/api/specialties', methods=['GET'])
def get_specialties():
    """Get list of all specialties."""
    session = get_db_session()
    try:
        doctors = session.query(Doctor).all()
        specialties = set()
        for doctor in doctors:
            if doctor.specialties:
                specialties.update(doctor.specialties)
        return jsonify(sorted(list(specialties)))
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


@app.route('/api/languages', methods=['GET'])
def get_languages():
    """Get list of all languages."""
    session = get_db_session()
    try:
        doctors = session.query(Doctor).all()
        languages = set()
        for doctor in doctors:
            if doctor.languages:
                languages.update(doctor.languages)
        return jsonify(sorted(list(languages)))
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


# ============================================================================
# ADMIN API ENDPOINTS
# ============================================================================

@app.route('/api/admin/doctors', methods=['POST'])
def create_doctor():
    """Create a new doctor."""
    session = get_db_session()
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate data
        is_valid, errors = validate_doctor_data(data)
        if not is_valid:
            return jsonify({'error': 'Validation failed', 'errors': errors}), 400
        
        # Parse address if city/postal_code not provided
        if not data.get('city') or not data.get('postal_code'):
            address_info = parse_address(data.get('address', ''))
            if not data.get('city') and address_info.get('city'):
                data['city'] = address_info['city']
            if not data.get('postal_code') and address_info.get('postal_code'):
                data['postal_code'] = address_info['postal_code']
        
        doctor = Doctor(
            name=data.get('name').strip(),
            specialties=data.get('specialties', []),
            languages=data.get('languages', []),
            address=data.get('address').strip(),
            city=data.get('city', '').strip(),
            postal_code=data.get('postal_code', '').strip(),
            country=data.get('country', 'Germany').strip(),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            phone=data.get('phone', '').strip() if data.get('phone') else None,
            email=data.get('email', '').strip() if data.get('email') else None,
            website=data.get('website', '').strip() if data.get('website') else None,
            business_hours=data.get('business_hours'),
            rating=data.get('rating', 0.0),
            review_count=data.get('review_count', 0),
            google_maps_url=data.get('google_maps_url', '').strip() if data.get('google_maps_url') else None,
            profile_image_url=data.get('profile_image_url', '').strip() if data.get('profile_image_url') else None,
            bio=data.get('bio', '').strip() if data.get('bio') else None,
        )
        
        session.add(doctor)
        session.commit()
        return jsonify(doctor.to_dict()), 201
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


@app.route('/api/admin/doctors/<int:doctor_id>', methods=['PUT'])
def update_doctor(doctor_id):
    """Update a doctor."""
    session = get_db_session()
    try:
        doctor = session.query(Doctor).filter_by(id=doctor_id).first()
        if not doctor:
            return jsonify({'error': 'Doctor not found'}), 404
        
        data = request.get_json()
        for key, value in data.items():
            if hasattr(doctor, key):
                setattr(doctor, key, value)
        
        session.commit()
        return jsonify(doctor.to_dict())
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


@app.route('/api/admin/doctors/<int:doctor_id>', methods=['DELETE'])
def delete_doctor(doctor_id):
    """Delete a doctor."""
    session = get_db_session()
    try:
        doctor = session.query(Doctor).filter_by(id=doctor_id).first()
        if not doctor:
            return jsonify({'error': 'Doctor not found'}), 404
        
        session.delete(doctor)
        session.commit()
        return jsonify({'message': 'Doctor deleted successfully'}), 200
    except Exception as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
