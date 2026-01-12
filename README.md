# Healthcare Portal - Azerbaijani Doctors in Germany

A comprehensive healthcare portal system for finding and managing Azerbaijani doctors practicing in Germany. The system includes a public-facing search portal and an admin dashboard for managing practitioner profiles.

## Features

### Public Portal
- Search and filter doctors by location, specialty, and languages
- Distance-based sorting
- Detailed doctor profiles with contact information
- Business hours display
- Google Maps integration
- Responsive design

### Admin Dashboard
- Add/Edit/Delete practitioner profiles
- Google Maps URL ingestion for automated data extraction
- Real-time profile preview
- SEO metadata management

## Project Structure

```
healthcare-portal/
├── backend/              # Backend API
│   ├── api/             # API endpoints
│   ├── models/          # Database models
│   └── utils/           # Utility functions
├── frontend/            # Frontend applications
│   ├── public/         # Public portal (HTML/CSS/JS)
│   └── admin/           # Admin dashboard (HTML/CSS/JS)
├── database/            # Database files and migrations
├── scripts/             # Utility scripts
└── requirements.txt     # Python dependencies
```

## Setup

### Prerequisites
- Python 3.14+
- pip or poetry
- SQLite (or PostgreSQL for production)

### Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd healthcare-portal
```

2. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize database:
```bash
python scripts/init_db.py
python scripts/seed_data.py
```

5. Run the backend server:
```bash
python backend/api/app.py
```

6. Open the frontend:
- Public portal: Open `frontend/public/index.html` in your browser
- Admin dashboard: Open `frontend/admin/index.html` in your browser

## Configuration

Create a `.env` file in the root directory:

```env
FLASK_ENV=development
FLASK_DEBUG=True
DATABASE_URL=sqlite:///database/healthcare.db
GOOGLE_MAPS_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here
```

## API Endpoints

### Public API
- `GET /api/doctors` - List all doctors (with filters)
- `GET /api/doctors/<id>` - Get doctor details
- `GET /api/specialties` - List all specialties
- `GET /api/languages` - List all languages

### Admin API
- `POST /api/admin/doctors` - Create new doctor
- `PUT /api/admin/doctors/<id>` - Update doctor
- `DELETE /api/admin/doctors/<id>` - Delete doctor
- `POST /api/admin/ingest-maps` - Ingest data from Google Maps URL

## Sample Data

The system comes with sample data for Azerbaijani doctors practicing in various German cities:
- Berlin
- Munich
- Hamburg
- Frankfurt
- Cologne
- Stuttgart

## Technologies

- **Backend**: Flask/FastAPI
- **Database**: SQLite (development), PostgreSQL (production)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla or React)
- **Maps**: Google Maps API

## License

MIT
