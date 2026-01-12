"""Database models for doctors/practitioners."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Doctor(Base):
    """Doctor/Practitioner model."""
    
    __tablename__ = 'doctors'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    specialties = Column(JSON, nullable=False)  # List of specialties
    languages = Column(JSON, nullable=False)  # List of languages
    address = Column(Text, nullable=False)
    city = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    country = Column(String(100), default='Germany')
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    phone = Column(String(50), nullable=True)
    email = Column(String(200), nullable=True)
    website = Column(String(500), nullable=True)
    business_hours = Column(JSON, nullable=True)  # Dict with day: hours
    rating = Column(Float, default=0.0)
    review_count = Column(Integer, default=0)
    google_maps_url = Column(String(500), nullable=True)
    profile_image_url = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert doctor to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'specialties': self.specialties,
            'languages': self.languages,
            'address': self.address,
            'city': self.city,
            'postal_code': self.postal_code,
            'country': self.country,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'phone': self.phone,
            'email': self.email,
            'website': self.website,
            'business_hours': self.business_hours,
            'rating': self.rating,
            'review_count': self.review_count,
            'google_maps_url': self.google_maps_url,
            'profile_image_url': self.profile_image_url,
            'bio': self.bio,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
