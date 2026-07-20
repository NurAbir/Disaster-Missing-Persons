function getUserFromToken() {
    const token = localStorage.getItem('token');
    if (!token) return null;
    try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        if (payload.exp * 1000 < Date.now()) {
            localStorage.removeItem('token');
            return null;
        }
        return payload;
    } catch (e) { return null; }
}

function logout() {
    localStorage.removeItem('token');
    window.location.href = '/';
}

function showToast(message, type) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type} show`;
    setTimeout(() => toast.classList.remove('show'), 3000);
}

function createReportCard(report) {
    const photo = report.photos && report.photos.length > 0 
        ? report.photos[0] 
        : 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="300" height="200"><rect fill="%23f3f4f6" width="300" height="200"/><text fill="%239ca3af" x="50%" y="50%" text-anchor="middle" dy=".3em">No Photo</text></svg>';
    return `
        <a href="/reports/${report.id}" class="report-card ${report.is_urgent ? 'urgent' : ''}">
            <img src="${photo}" alt="${report.full_name}" class="report-img" loading="lazy">
            <div class="report-card-body">
                ${report.is_urgent ? '<div class="urgent-badge">URGENT</div>' : ''}
                <h3>${report.full_name}</h3>
                <div class="report-meta">
                    <span class="status status-${report.status}">${report.status}</span>
                    <span>Age: ${report.age || '?'}</span>
                    <span>${report.gender}</span>
                </div>
                <div class="report-meta" style="margin-top:0.5rem;">
                    <span>${report.last_seen_location.address || 'Location unknown'}</span>
                </div>
                <div class="report-meta">
                    <span>${new Date(report.last_seen_datetime).toLocaleDateString()}</span>
                    <span>${report.tips_count} tips</span>
                </div>
            </div>
        </a>
    `;
}

function toggleNav() {
    document.getElementById('navLinks').classList.toggle('show');
}

// Helper for fetch with better error reporting
async function apiFetch(url, options = {}) {
    try {
        console.log('API Request:', url, options);
        const res = await fetch(url, options);
        console.log('API Response:', res.status, res.statusText);

        if (!res.ok) {
            const text = await res.text();
            console.error('API Error body:', text);
            let detail = 'Request failed';
            try {
                const json = JSON.parse(text);
                // Handle FastAPI validation errors (422)
                if (json.detail && Array.isArray(json.detail)) {
                    detail = json.detail.map(e => `${e.loc.join('.')}: ${e.msg}`).join('; ');
                } else if (json.detail) {
                    detail = json.detail;
                } else if (json.message) {
                    detail = json.message;
                } else {
                    detail = JSON.stringify(json).substring(0, 200);
                }
            } catch (e) {
                detail = text.substring(0, 200) || `HTTP ${res.status}`;
            }
            throw new Error(detail);
        }
        return res;
    } catch (err) {
        console.error('Fetch error:', err);
        if (err.message === 'Failed to fetch') {
            throw new Error('Cannot connect to server. Is it running?');
        }
        throw err;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const user = getUserFromToken();
    const loginLink = document.getElementById('loginLink');
    const registerLink = document.getElementById('registerLink');
    const logoutBtn = document.getElementById('logoutBtn');
    const userInfo = document.getElementById('userInfo');
    const createReportLink = document.getElementById('createReportLink');
    const adminLink = document.getElementById('adminLink');

    if (user) {
        if (loginLink) loginLink.style.display = 'none';
        if (registerLink) registerLink.style.display = 'none';
        if (logoutBtn) logoutBtn.style.display = 'inline';
        if (userInfo) { userInfo.style.display = 'inline'; userInfo.textContent = user.role; }
        if (user.role === 'rescuer' || user.role === 'admin') {
            if (createReportLink) createReportLink.style.display = 'inline';
        }
        if (user.role === 'admin') {
            if (adminLink) adminLink.style.display = 'inline';
        }
    }
});
