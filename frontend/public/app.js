// API Configuration
const API_BASE_URL = 'http://localhost:5001/api';

// State
let doctors = [];
let specialties = [];
let languages = [];
let filters = {
    city: 'Germany',
    specialty: '',
    language: '',
    search: '',
    sort_by: 'distance'
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    loadSpecialties();
    loadLanguages();
    loadDoctors();
    
    // Event listeners
    document.getElementById('sort-by').addEventListener('change', (e) => {
        filters.sort_by = e.target.value;
        loadDoctors();
    });
    
    document.getElementById('reset-filters').addEventListener('click', (e) => {
        e.preventDefault();
        resetFilters();
    });
    
    document.getElementById('load-more').addEventListener('click', loadMoreDoctors);
});

// Load specialties
async function loadSpecialties() {
    try {
        const response = await fetch(`${API_BASE_URL}/specialties`);
        specialties = await response.json();
        renderSpecialtiesFilter();
    } catch (error) {
        console.error('Error loading specialties:', error);
    }
}

// Load languages
async function loadLanguages() {
    try {
        const response = await fetch(`${API_BASE_URL}/languages`);
        languages = await response.json();
        renderLanguagesFilter();
    } catch (error) {
        console.error('Error loading languages:', error);
    }
}

// Render specialties filter
function renderSpecialtiesFilter() {
    const container = document.getElementById('specialties-filter');
    container.innerHTML = specialties.map(specialty => `
        <div class="checkbox-item">
            <input type="checkbox" id="spec-${specialty}" value="${specialty}" 
                   onchange="handleSpecialtyChange(this)">
            <label for="spec-${specialty}">${specialty}</label>
        </div>
    `).join('');
}

// Render languages filter
function renderLanguagesFilter() {
    const container = document.getElementById('languages-filter');
    container.innerHTML = languages.map(language => `
        <div class="checkbox-item">
            <input type="checkbox" id="lang-${language}" value="${language}" 
                   onchange="handleLanguageChange(this)">
            <label for="lang-${language}">${language}</label>
        </div>
    `).join('');
}

// Handle specialty change
function handleSpecialtyChange(checkbox) {
    if (checkbox.checked) {
        filters.specialty = checkbox.value;
    } else {
        filters.specialty = '';
    }
    loadDoctors();
}

// Handle language change
function handleLanguageChange(checkbox) {
    if (checkbox.checked) {
        filters.language = checkbox.value;
    } else {
        filters.language = '';
    }
    loadDoctors();
}

// Load doctors
async function loadDoctors() {
    const doctorsList = document.getElementById('doctors-list');
    doctorsList.innerHTML = '<div class="loading">Loading doctors...</div>';
    
    try {
        const params = new URLSearchParams();
        if (filters.city) params.append('city', filters.city);
        if (filters.specialty) params.append('specialty', filters.specialty);
        if (filters.language) params.append('language', filters.language);
        if (filters.search) params.append('search', filters.search);
        if (filters.sort_by) params.append('sort_by', filters.sort_by);
        
        const response = await fetch(`${API_BASE_URL}/doctors?${params}`);
        const data = await response.json();
        
        doctors = data.doctors || [];
        renderDoctors();
        updateResultsCount(data.count);
    } catch (error) {
        console.error('Error loading doctors:', error);
        doctorsList.innerHTML = '<div class="loading">Error loading doctors. Please try again.</div>';
    }
}

// Render doctors
function renderDoctors() {
    const container = document.getElementById('doctors-list');
    
    if (doctors.length === 0) {
        container.innerHTML = '<div class="loading">No doctors found matching your criteria.</div>';
        return;
    }
    
    container.innerHTML = doctors.map(doctor => `
        <div class="doctor-card">
            <div class="doctor-image">
                👨‍⚕️
            </div>
            <div class="doctor-info">
                <h3 class="doctor-name">${doctor.name}</h3>
                <div class="specialty-tags">
                    ${doctor.specialties.map(s => `<span class="tag">${s}</span>`).join('')}
                </div>
                <div class="rating">
                    ★ ${doctor.rating} (${doctor.review_count} reviews)
                </div>
                <div class="doctor-details">
                    <div class="detail-item">
                        <span class="detail-item-icon">📍</span>
                        <span>${doctor.address}, ${doctor.city}, ${doctor.postal_code}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-item-icon">📞</span>
                        <span>${doctor.phone || 'N/A'}</span>
                    </div>
                    <div class="detail-item">
                        <span class="detail-item-icon">🌐</span>
                        <span>${doctor.languages.join(', ')}</span>
                    </div>
                </div>
                ${renderBusinessHours(doctor.business_hours)}
                ${doctor.google_maps_url ? `
                    <a href="${doctor.google_maps_url}" target="_blank" class="open-maps-btn">
                        📍 Open in Google Maps
                    </a>
                ` : ''}
            </div>
        </div>
    `).join('');
}

// Render business hours
function renderBusinessHours(hours) {
    if (!hours) return '';
    
    const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
    return `
        <div class="business-hours">
            ${days.map(day => {
                const hoursText = hours[day] || 'Closed';
                return `<div class="hours-item">${day}: ${hoursText}</div>`;
            }).join('')}
        </div>
    `;
}

// Update results count
function updateResultsCount(count) {
    const countElement = document.getElementById('results-count');
    countElement.textContent = `${count} Doctors found near you`;
}

// Reset filters
function resetFilters() {
    filters = {
        city: 'Germany',
        specialty: '',
        language: '',
        search: '',
        sort_by: 'distance'
    };
    
    document.getElementById('location-input').value = 'Germany';
    document.getElementById('sort-by').value = 'distance';
    
    // Uncheck all checkboxes
    document.querySelectorAll('#specialties-filter input[type="checkbox"]').forEach(cb => cb.checked = false);
    document.querySelectorAll('#languages-filter input[type="checkbox"]').forEach(cb => cb.checked = false);
    
    loadDoctors();
}

// Load more doctors (placeholder)
function loadMoreDoctors() {
    // Implement pagination if needed
    console.log('Load more doctors');
}
