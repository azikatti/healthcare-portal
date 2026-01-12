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
    const mapsUrl = document.getElementById('maps-url').value.trim();
    if (!mapsUrl) {
        showError('Please enter a Google Maps URL');
        return;
    }
    
    const ingestBtn = document.getElementById('ingest-btn');
    const originalText = ingestBtn.innerHTML;
    ingestBtn.disabled = true;
    ingestBtn.innerHTML = '<span>⏳</span> Processing...';
    
    try {
        const response = await fetch(`${API_BASE_URL}/admin/ingest-maps`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: mapsUrl })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            // Update extracted data fields if available
            if (data.data.address) {
                document.getElementById('extracted-address').textContent = data.data.address;
            }
            if (data.data.phone) {
                document.getElementById('extracted-phone').textContent = data.data.phone;
            }
            if (data.data.city) {
                document.getElementById('doctor-city').value = data.data.city;
            }
            if (data.data.postal_code) {
                document.getElementById('doctor-postal-code').value = data.data.postal_code;
            }
            if (data.data.business_hours) {
                currentDoctor.business_hours = data.data.business_hours;
                updatePreview();
            }
            
            showSuccess('URL processed successfully! ' + (data.data.note || ''));
            updatePreview();
        } else {
            showError(data.error || 'Failed to process URL');
        }
    } catch (error) {
        console.error('Error ingesting maps data:', error);
        showError('Error ingesting data. Please try again.');
    } finally {
        ingestBtn.disabled = false;
        ingestBtn.innerHTML = originalText;
    }
}

// Handle save
async function handleSave() {
    // Validate required fields
    const name = document.getElementById('doctor-name').value.trim();
    if (!name) {
        showError('Doctor name is required');
        return;
    }
    
    if (currentDoctor.specialties.length === 0) {
        showError('At least one specialty is required');
        return;
    }
    
    if (currentDoctor.languages.length === 0) {
        showError('At least one language is required');
        return;
    }
    
    const address = document.getElementById('extracted-address').textContent.trim();
    if (!address) {
        showError('Address is required');
        return;
    }
    
    const doctorData = {
        name: name,
        specialties: currentDoctor.specialties,
        languages: currentDoctor.languages,
        address: address,
        city: document.getElementById('doctor-city').value.trim() || 'Berlin',
        postal_code: document.getElementById('doctor-postal-code').value.trim() || '',
        country: document.getElementById('doctor-country').value.trim() || 'Germany',
        phone: document.getElementById('extracted-phone').textContent.trim() || null,
        business_hours: currentDoctor.business_hours,
        google_maps_url: document.getElementById('maps-url').value.trim() || null
    };
    
    const saveBtn = document.getElementById('save-btn');
    const originalText = saveBtn.innerHTML;
    saveBtn.disabled = true;
    saveBtn.innerHTML = '<span>⏳</span> Saving...';
    
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
            showSuccess('Doctor profile saved successfully!');
            // Optionally reset form or redirect
            setTimeout(() => {
                handleDiscard();
            }, 2000);
        } else {
            const errorMsg = data.errors ? data.errors.join(', ') : (data.error || 'Failed to save');
            showError('Error: ' + errorMsg);
        }
    } catch (error) {
        console.error('Error saving doctor:', error);
        showError('Error saving doctor. Please try again.');
    } finally {
        saveBtn.disabled = false;
        saveBtn.innerHTML = originalText;
    }
}

// Show success message
function showSuccess(message) {
    // Create or update notification
    let notification = document.getElementById('notification');
    if (!notification) {
        notification = document.createElement('div');
        notification.id = 'notification';
        notification.style.cssText = 'position: fixed; top: 20px; right: 20px; padding: 1rem 1.5rem; background: #10b981; color: white; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); z-index: 1000; max-width: 400px;';
        document.body.appendChild(notification);
    }
    notification.textContent = message;
    notification.style.background = '#10b981';
    notification.style.display = 'block';
    setTimeout(() => {
        notification.style.display = 'none';
    }, 5000);
}

// Show error message
function showError(message) {
    // Create or update notification
    let notification = document.getElementById('notification');
    if (!notification) {
        notification = document.createElement('div');
        notification.id = 'notification';
        notification.style.cssText = 'position: fixed; top: 20px; right: 20px; padding: 1rem 1.5rem; background: #ef4444; color: white; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); z-index: 1000; max-width: 400px;';
        document.body.appendChild(notification);
    }
    notification.textContent = message;
    notification.style.background = '#ef4444';
    notification.style.display = 'block';
    setTimeout(() => {
        notification.style.display = 'none';
    }, 5000);
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
