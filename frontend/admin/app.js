// API Configuration
const API_BASE_URL = 'http://localhost:5001/api';

// State
let currentDoctor = {
    name: 'Dr. Jane Smith',
    specialties: ['Cardiology', 'Pediatrics'],
    languages: ['Azerbaijani'],
    address: '123 Medical Plaza, Downtown Health District, NY 10001',
    phone: '+1 (555) 098-7654',
    business_hours: {
        'Monday': '08:00 - 18:00',
        'Tuesday': '08:00 - 18:00',
        'Wednesday': '08:00 - 18:00',
        'Thursday': '08:00 - 18:00',
        'Friday': '08:00 - 18:00',
        'Saturday': '09:00 - 14:00',
        'Sunday': 'Closed'
    }
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    updatePreview();
});

// Setup event listeners
function setupEventListeners() {
    // Name input
    document.getElementById('doctor-name').addEventListener('input', (e) => {
        currentDoctor.name = e.target.value;
        updatePreview();
    });
    
    // Specialty input
    const specialtyInput = document.getElementById('specialty-input');
    specialtyInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            addSpecialty(e.target.value);
            e.target.value = '';
        }
    });
    
    // Language input
    const languageInput = document.getElementById('language-input');
    languageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            addLanguage(e.target.value);
            e.target.value = '';
        }
    });
    
    // Remove specialty tags
    document.getElementById('specialties-input').addEventListener('click', (e) => {
        if (e.target.classList.contains('tag-remove')) {
            const tag = e.target.closest('.tag');
            const specialty = tag.textContent.trim().replace('×', '').trim();
            removeSpecialty(specialty);
        }
    });
    
    // Remove language tags
    document.getElementById('languages-input').addEventListener('click', (e) => {
        if (e.target.classList.contains('tag-remove')) {
            const tag = e.target.closest('.tag');
            const language = tag.textContent.trim().replace('×', '').trim();
            removeLanguage(language);
        }
    });
    
    // Ingest button
    document.getElementById('ingest-btn').addEventListener('click', handleIngest);
    
    // Save button
    document.getElementById('save-btn').addEventListener('click', handleSave);
    
    // Discard button
    document.getElementById('discard-btn').addEventListener('click', handleDiscard);
}

// Add specialty
function addSpecialty(specialty) {
    if (specialty.trim() && !currentDoctor.specialties.includes(specialty.trim())) {
        currentDoctor.specialties.push(specialty.trim());
        renderSpecialties();
        updatePreview();
    }
}

// Remove specialty
function removeSpecialty(specialty) {
    currentDoctor.specialties = currentDoctor.specialties.filter(s => s !== specialty);
    renderSpecialties();
    updatePreview();
}

// Render specialties
function renderSpecialties() {
    const container = document.getElementById('specialties-input');
    const input = document.getElementById('specialty-input');
    container.innerHTML = currentDoctor.specialties.map(s => `
        <span class="tag">${s} <span class="tag-remove">×</span></span>
    `).join('');
    container.appendChild(input);
}

// Add language
function addLanguage(language) {
    if (language.trim() && !currentDoctor.languages.includes(language.trim())) {
        currentDoctor.languages.push(language.trim());
        renderLanguages();
        updatePreview();
    }
}

// Remove language
function removeLanguage(language) {
    currentDoctor.languages = currentDoctor.languages.filter(l => l !== language);
    renderLanguages();
    updatePreview();
}

// Render languages
function renderLanguages() {
    const container = document.getElementById('languages-input');
    const input = document.getElementById('language-input');
    container.innerHTML = currentDoctor.languages.map(l => `
        <span class="tag">${l} <span class="tag-remove">×</span></span>
    `).join('');
    container.appendChild(input);
}

// Update preview
function updatePreview() {
    document.getElementById('preview-name').textContent = currentDoctor.name;
    
    const specialtiesContainer = document.getElementById('preview-specialties');
    specialtiesContainer.innerHTML = currentDoctor.specialties.map(s => 
        `<span class="preview-tag">${s.toUpperCase()}</span>`
    ).join('');
    
    document.getElementById('preview-languages').textContent = currentDoctor.languages.join(', ');
    document.getElementById('preview-address').textContent = currentDoctor.address;
    document.getElementById('preview-phone').textContent = currentDoctor.phone;
}

// Handle ingest
async function handleIngest() {
    const mapsUrl = document.getElementById('maps-url').value;
    if (!mapsUrl) {
        alert('Please enter a Google Maps URL');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/admin/ingest-maps`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: mapsUrl })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Update extracted data (placeholder - would be real data from API)
            alert('Data ingested successfully! (This is a placeholder - implement Google Maps API integration)');
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        console.error('Error ingesting maps data:', error);
        alert('Error ingesting data. Please try again.');
    }
}

// Handle save
async function handleSave() {
    const doctorData = {
        name: document.getElementById('doctor-name').value,
        specialties: currentDoctor.specialties,
        languages: currentDoctor.languages,
        address: document.getElementById('extracted-address').textContent,
        city: document.getElementById('doctor-city').value || 'Berlin',
        postal_code: document.getElementById('doctor-postal-code').value || '',
        country: document.getElementById('doctor-country').value || 'Germany',
        phone: document.getElementById('extracted-phone').textContent,
        business_hours: currentDoctor.business_hours,
        google_maps_url: document.getElementById('maps-url').value
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/admin/doctors`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(doctorData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert('Doctor profile saved successfully!');
            // Reset form or redirect
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        console.error('Error saving doctor:', error);
        alert('Error saving doctor. Please try again.');
    }
}

// Handle discard
function handleDiscard() {
    if (confirm('Are you sure you want to discard changes?')) {
        // Reset form
        document.getElementById('doctor-name').value = 'Dr. Jane Smith';
        document.getElementById('doctor-city').value = 'Berlin';
        document.getElementById('doctor-postal-code').value = '10117';
        document.getElementById('doctor-country').value = 'Germany';
        currentDoctor = {
            name: 'Dr. Jane Smith',
            specialties: ['Cardiology', 'Pediatrics'],
            languages: ['Azerbaijani'],
            address: '123 Medical Plaza, Downtown Health District, NY 10001',
            phone: '+1 (555) 098-7654',
            business_hours: currentDoctor.business_hours
        };
        renderSpecialties();
        renderLanguages();
        updatePreview();
    }
}
