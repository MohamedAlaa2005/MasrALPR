// DOM Elements
const camInput = document.getElementById('camIn');
const scanBtn = document.getElementById('scanBtn');
const resultBox = document.getElementById('resBox');
const resultPlate = document.getElementById('resultPlate');
const resultStatus = document.getElementById('resultStatus');

const textInput = document.getElementById('textIn');
const blockTextBtn = document.getElementById('blockTextBtn');
const photoInput = document.getElementById('photoIn');
const blockPhotoBtn = document.getElementById('blockPhotoBtn');

const blacklistContainer = document.getElementById('blList');
const historyContainer = document.getElementById('histList');
const blockCount = document.getElementById('blockCount');

// Event Listeners
scanBtn.addEventListener('click', () => camInput.click());
blockTextBtn.addEventListener('click', addText);
blockPhotoBtn.addEventListener('click', () => photoInput.click());
camInput.addEventListener('change', scan);
photoInput.addEventListener('change', addPhoto);

// Allow Enter key to submit text
textInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        addText();
    }
});

// Scan plate function
async function scan() {
    if (!camInput.files[0]) return;

    try {
        const formData = new FormData();
        formData.append("file", camInput.files[0]);

        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        // Display result
        resultPlate.textContent = data.plate;
        resultStatus.textContent = data.allowed ? '✓ ACCESS GRANTED' : '✗ ACCESS DENIED';

        // Update result box styling
        resultBox.classList.add('show');
        if (data.allowed) {
            resultBox.classList.remove('error');
            resultBox.classList.add('success');
        } else {
            resultBox.classList.remove('success');
            resultBox.classList.add('error');
        }

        // Update history
        loadHistory();
    } catch (error) {
        console.error('Error scanning plate:', error);
        alert('ERROR: Failed to scan plate. Please try again.');
    }
}

// Add plate by text
async function addText() {
    const plateText = textInput.value.trim();
    
    if (!plateText) {
        alert('ERROR: Please enter a plate number');
        return;
    }

    try {
        await fetch(`/blacklist/add?plate=${encodeURIComponent(plateText)}`, {
            method: 'POST'
        });

        textInput.value = '';
        loadBlacklist();
    } catch (error) {
        console.error('Error adding to blacklist:', error);
        alert('ERROR: Failed to add to blacklist. Please try again.');
    }
}

// Add plate by photo
async function addPhoto() {
    if (!photoInput.files[0]) return;

    try {
        const formData = new FormData();
        formData.append("file", photoInput.files[0]);

        const response = await fetch('/blacklist/add-by-photo', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        loadBlacklist();
    } catch (error) {
        console.error('Error adding photo to blacklist:', error);
        alert('ERROR: Failed to process photo. Please try again.');
    }
}

// Load blacklist
async function loadBlacklist() {
    try {
        const response = await fetch('/blacklist');
        const data = await response.json();

        // Update count badge
        if (blockCount) {
            blockCount.textContent = data.length;
        }

        if (data.length === 0) {
            blacklistContainer.innerHTML = `
                <div class="empty-state">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"/>
                        <line x1="12" y1="8" x2="12" y2="12"/>
                        <line x1="12" y1="16" x2="12.01" y2="16"/>
                    </svg>
                    <p>NO BLOCKED PLATES</p>
                </div>
            `;
            return;
        }

        blacklistContainer.innerHTML = data.map(item => `
            <div class="entry-item">
                <span class="entry-plate">${item.plate_text}</span>
                <button class="delete-btn" onclick="deleteRule(${item.id})">×</button>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading blacklist:', error);
        blacklistContainer.innerHTML = `
            <div class="empty-state">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <line x1="15" y1="9" x2="9" y2="15"/>
                    <line x1="9" y1="9" x2="15" y2="15"/>
                </svg>
                <p>ERROR LOADING DATA</p>
            </div>
        `;
    }
}

// Delete rule from blacklist
async function deleteRule(id) {
    try {
        await fetch(`/blacklist/remove/${id}`, {
            method: 'DELETE'
        });
        loadBlacklist();
    } catch (error) {
        console.error('Error deleting rule:', error);
        alert('ERROR: Failed to remove from blacklist. Please try again.');
    }
}

// Load history
async function loadHistory() {
    try {
        const response = await fetch('/history');
        const data = await response.json();

        if (data.length === 0) {
            historyContainer.innerHTML = `
                <div class="empty-state">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"/>
                        <polyline points="12 6 12 12 16 14"/>
                    </svg>
                    <p>NO SCAN HISTORY</p>
                </div>
            `;
            return;
        }

        historyContainer.innerHTML = data.map(item => `
            <div class="log-item">
                <span class="log-plate">${item.text}</span>
                <span class="log-status ${item.is_allowed ? 'allowed' : 'blocked'}">
                    ${item.is_allowed ? 'ALLOWED' : 'BLOCKED'}
                </span>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading history:', error);
        historyContainer.innerHTML = `
            <div class="empty-state">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <line x1="15" y1="9" x2="9" y2="15"/>
                    <line x1="9" y1="9" x2="15" y2="15"/>
                </svg>
                <p>ERROR LOADING DATA</p>
            </div>
        `;
    }
}

// Make deleteRule available globally
window.deleteRule = deleteRule;

// Initialize data on page load
document.addEventListener('DOMContentLoaded', () => {
    loadBlacklist();
    loadHistory();
});