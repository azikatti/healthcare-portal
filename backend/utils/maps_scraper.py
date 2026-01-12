"""Google Maps web scraper with human-like behavior."""

import re
import time
import json
import random
from typing import Dict, Optional
from urllib.parse import urlparse, parse_qs
import requests
from bs4 import BeautifulSoup


class GoogleMapsScraper:
    """Scraper for Google Maps URLs with human-like delays."""
    
    def __init__(self):
        self.session = requests.Session()
        # Human-like headers
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,de;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
        })
    
    def _human_delay(self, min_seconds: float = 2.0, max_seconds: float = 5.0):
        """Simulate human-like delay."""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
    
    def extract_coordinates_from_url(self, url: str) -> Optional[Dict]:
        """Extract coordinates from Google Maps URL."""
        # Pattern: @lat,lng
        coord_match = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', url)
        if coord_match:
            return {
                'lat': float(coord_match.group(1)),
                'lng': float(coord_match.group(2))
            }
        
        # Pattern: !3dlat!4dlng
        coord_match = re.search(r'!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)', url)
        if coord_match:
            return {
                'lat': float(coord_match.group(1)),
                'lng': float(coord_match.group(2))
            }
        
        return None
    
    def scrape_maps_page(self, url: str) -> Dict:
        """Scrape Google Maps page to extract place data with human-like behavior."""
        result = {
            'address': None,
            'phone': None,
            'website': None,
            'business_hours': None,
            'name': None,
            'rating': None,
            'review_count': None,
            'latitude': None,
            'longitude': None,
            'city': None,
            'postal_code': None,
            'country': 'Germany',
            'success': False,
            'error': None
        }
        
        try:
            # Human-like delay before request
            self._human_delay(2.0, 4.0)
            
            # Fetch the page
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            # Another small delay (like human reading)
            self._human_delay(1.0, 2.0)
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Try to extract JSON-LD structured data (most reliable)
            json_data = self._extract_json_ld(soup)
            if json_data:
                result.update(self._parse_json_ld(json_data))
            
            # Extract from HTML content as fallback
            self._extract_from_html(soup, result)
            
            # Extract coordinates from URL
            coords = self.extract_coordinates_from_url(url)
            if coords:
                result['latitude'] = coords.get('lat')
                result['longitude'] = coords.get('lng')
            
            # Parse address to extract city/postal code
            if result['address']:
                from backend.utils.validation import parse_address
                address_info = parse_address(result['address'])
                if not result['city'] and address_info.get('city'):
                    result['city'] = address_info['city']
                if not result['postal_code'] and address_info.get('postal_code'):
                    result['postal_code'] = address_info['postal_code']
            
            result['success'] = True
            
        except requests.RequestException as e:
            result['error'] = f'Network error: {str(e)}'
        except Exception as e:
            result['error'] = f'Parsing error: {str(e)}'
        
        return result
    
    def _extract_json_ld(self, soup: BeautifulSoup) -> Optional[Dict]:
        """Extract JSON-LD structured data from page."""
        scripts = soup.find_all('script', type='application/ld+json')
        for script in scripts:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict) and '@type' in data:
                    if data.get('@type') in ['LocalBusiness', 'MedicalBusiness', 'Physician', 'Place', 'Organization']:
                        return data
            except (json.JSONDecodeError, AttributeError):
                continue
        return None
    
    def _parse_json_ld(self, data: Dict) -> Dict:
        """Parse JSON-LD data to extract place information."""
        result = {}
        
        # Name
        if 'name' in data:
            result['name'] = data['name']
        
        # Address
        if 'address' in data:
            address = data['address']
            if isinstance(address, dict):
                address_parts = []
                if 'streetAddress' in address:
                    address_parts.append(address['streetAddress'])
                if 'addressLocality' in address:
                    address_parts.append(address['addressLocality'])
                    result['city'] = address['addressLocality']
                if 'postalCode' in address:
                    address_parts.append(address['postalCode'])
                    result['postal_code'] = address['postalCode']
                if 'addressCountry' in address:
                    if isinstance(address['addressCountry'], dict):
                        result['country'] = address['addressCountry'].get('name', 'Germany')
                    else:
                        result['country'] = address['addressCountry']
                result['address'] = ', '.join(address_parts)
            elif isinstance(address, str):
                result['address'] = address
        
        # Phone
        if 'telephone' in data:
            result['phone'] = data['telephone']
        
        # Website
        if 'url' in data or 'sameAs' in data:
            result['website'] = data.get('url') or data.get('sameAs')
        
        # Coordinates
        if 'geo' in data:
            geo = data['geo']
            if isinstance(geo, dict):
                if 'latitude' in geo:
                    result['latitude'] = float(geo['latitude'])
                if 'longitude' in geo:
                    result['longitude'] = float(geo['longitude'])
        
        # Rating
        if 'aggregateRating' in data:
            rating_data = data['aggregateRating']
            if isinstance(rating_data, dict):
                if 'ratingValue' in rating_data:
                    result['rating'] = float(rating_data['ratingValue'])
                if 'reviewCount' in rating_data:
                    result['review_count'] = int(rating_data['reviewCount'])
        
        # Opening hours
        if 'openingHoursSpecification' in data:
            hours = data['openingHoursSpecification']
            if isinstance(hours, list):
                result['business_hours'] = self._parse_opening_hours(hours)
        
        return result
    
    def _extract_from_html(self, soup: BeautifulSoup, result: Dict):
        """Extract data from HTML content when JSON-LD is not available."""
        # Try to find address in various selectors
        if not result.get('address'):
            address_selectors = [
                '[data-value="Address"]',
                '.section-address',
                '[itemprop="address"]',
                '.address',
                '[data-item-id="address"]',
            ]
            for selector in address_selectors:
                elem = soup.select_one(selector)
                if elem:
                    result['address'] = elem.get_text(strip=True)
                    break
        
        # Try to find phone
        if not result.get('phone'):
            phone_patterns = [
                r'\+?[\d\s\-\(\)]{10,}',
                r'Tel[:\s]+([+\d\s\-\(\)]+)',
                r'Phone[:\s]+([+\d\s\-\(\)]+)',
            ]
            text = soup.get_text()
            for pattern in phone_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    phone = match.group(1) if match.groups() else match.group(0)
                    cleaned = re.sub(r'[^\d+]', '', phone)
                    if len(cleaned) >= 10:
                        result['phone'] = phone.strip()
                        break
    
    def _parse_opening_hours(self, hours_spec: list) -> Dict[str, str]:
        """Parse opening hours specification from JSON-LD."""
        days_map = {
            'Monday': 'Monday',
            'Tuesday': 'Tuesday',
            'Wednesday': 'Wednesday',
            'Thursday': 'Thursday',
            'Friday': 'Friday',
            'Saturday': 'Saturday',
            'Sunday': 'Sunday',
        }
        
        result = {}
        for spec in hours_spec:
            if isinstance(spec, dict):
                day = spec.get('dayOfWeek', '')
                day = days_map.get(day, day)
                opens = spec.get('opens', '')
                closes = spec.get('closes', '')
                
                if day and opens and closes:
                    result[day] = f"{opens} - {closes}"
                elif day:
                    result[day] = 'Closed'
        
        return result


def scrape_google_maps(url: str) -> Dict:
    """Convenience function to scrape Google Maps URL."""
    scraper = GoogleMapsScraper()
    return scraper.scrape_maps_page(url)
