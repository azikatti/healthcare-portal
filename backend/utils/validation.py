"""Validation utilities for doctor data."""

import re
from typing import Dict, List, Optional, Tuple


def validate_doctor_data(data: Dict) -> Tuple[bool, List[str]]:
    """Validate doctor data before creation/update.
    
    Args:
        data: Dictionary containing doctor data
        
    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []
    
    # Required fields
    if not data.get('name') or not data.get('name').strip():
        errors.append('Name is required')
    
    if not data.get('address') or not data.get('address').strip():
        errors.append('Address is required')
    
    if not data.get('city') or not data.get('city').strip():
        errors.append('City is required')
    
    # Validate specialties
    specialties = data.get('specialties', [])
    if not specialties or not isinstance(specialties, list) or len(specialties) == 0:
        errors.append('At least one specialty is required')
    
    # Validate languages
    languages = data.get('languages', [])
    if not languages or not isinstance(languages, list) or len(languages) == 0:
        errors.append('At least one language is required')
    
    # Validate email format if provided
    email = data.get('email', '')
    if email and not is_valid_email(email):
        errors.append('Invalid email format')
    
    # Validate phone format if provided
    phone = data.get('phone', '')
    if phone and not is_valid_phone(phone):
        errors.append('Invalid phone format')
    
    # Validate URL format if provided
    website = data.get('website', '')
    if website and not is_valid_url(website):
        errors.append('Invalid website URL format')
    
    google_maps_url = data.get('google_maps_url', '')
    if google_maps_url and not is_valid_url(google_maps_url):
        errors.append('Invalid Google Maps URL format')
    
    # Validate rating range
    rating = data.get('rating', 0.0)
    if rating is not None and (rating < 0 or rating > 5):
        errors.append('Rating must be between 0 and 5')
    
    return len(errors) == 0, errors


def is_valid_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def is_valid_phone(phone: str) -> bool:
    """Validate phone number format (international format)."""
    # Remove spaces, dashes, and parentheses
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    # Should start with + and have 7-15 digits
    pattern = r'^\+?[1-9]\d{6,14}$'
    return bool(re.match(pattern, cleaned))


def is_valid_url(url: str) -> bool:
    """Validate URL format."""
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return bool(re.match(pattern, url))


def parse_address(address: str) -> Dict[str, Optional[str]]:
    """Parse address string to extract city and postal code.
    
    Args:
        address: Full address string
        
    Returns:
        Dictionary with 'city' and 'postal_code' keys
    """
    result = {'city': None, 'postal_code': None}
    
    if not address:
        return result
    
    # Try to extract postal code (German format: 5 digits)
    postal_code_match = re.search(r'\b\d{5}\b', address)
    if postal_code_match:
        result['postal_code'] = postal_code_match.group()
    
    # Common German cities to look for
    german_cities = [
        'Berlin', 'Munich', 'Hamburg', 'Frankfurt', 'Cologne', 'Stuttgart',
        'Düsseldorf', 'Dortmund', 'Essen', 'Leipzig', 'Bremen', 'Dresden',
        'Hannover', 'Nuremberg', 'Duisburg', 'Bochum', 'Wuppertal', 'Bielefeld',
        'Bonn', 'Münster', 'Karlsruhe', 'Mannheim', 'Augsburg', 'Wiesbaden'
    ]
    
    address_lower = address.lower()
    for city in german_cities:
        if city.lower() in address_lower:
            result['city'] = city
            break
    
    return result
