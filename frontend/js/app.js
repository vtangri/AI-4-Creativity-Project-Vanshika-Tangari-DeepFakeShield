/**
 * DeepFakeShield AI - Premium Frontend Application
 * Features: 3D Tilt, Intersection Observer, Dynamic Charts
 */

const API_BASE = '/api/v1';

// --- VISUAL EFFECTS ---

class VFX {
    static init() {
        this.initTilt();
        this.initScrollReveal();
        this.initMagneticButtons();
    }

    // 3D Tilt Effect for Glass Cards
    static initTilt() {
        document.querySelectorAll('.glass-card, .feature-card, .verdict-card').forEach(card => {
            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                
                const centerX = rect.width / 2;
                const centerY = rect.height / 2;
                
                const rotateX = ((y - centerY) / centerY) * -5;
                const rotateY = ((x - centerX) / centerX) * 5;
                
                card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
                
                // Dynamic Highlight
                const sheenX = (x / rect.width) * 100;
                const sheenY = (y / rect.height) * 100;
                card.style.background = `radial-gradient(circle at ${sheenX}% ${sheenY}%, rgba(255,255,255,0.08), rgba(255,255,255,0.03) 40%)`;
            });

            card.addEventListener('mouseleave', () => {
                card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)';
                card.style.background = 'var(--bg-panel)';
            });
        });
    }

    // Scroll Reveal Animation
    static initScrollReveal() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, { threshold: 0.1 });

        document.querySelectorAll('.feature-card, .step-card').forEach((el, index) => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = `all 0.6s cubic-bezier(0.16, 1, 0.3, 1) ${index * 0.1}s`;
            observer.observe(el);
        });
    }
    
    // Auto-init on new content
    static refresh() {
        this.initTilt();
    }
}

// --- STATE MANAGEMENT ---

const state = {
    user: null,
    token: localStorage.getItem('token'),
    currentJobId: null,
    selectedFile: null
};

// --- API CLIENT ---

const api = {
    async request(endpoint, options = {}) {
        const headers = { 'Content-Type': 'application/json', ...options.headers };
        if (state.token) headers['Authorization'] = `Bearer ${state.token}`;
        
        try {
            const response = await fetch(`${API_BASE}${endpoint}`, { ...options, headers });
            const data = await response.json();
            if (!response.ok) throw new Error(data.detail || 'Request failed');
            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },
    
    async login(email, password) {
        const formData = new FormData();
        formData.append('username', email);
        formData.append('password', password);
        
        const response = await fetch(`${API_BASE}/auth/login`, { method: 'POST', body: formData });
        const data = await response.json();
        
        if (!response.ok) throw new Error(data.detail || 'Login failed');
        state.token = data.access_token;
        localStorage.setItem('token', state.token);
        return data;
    },
    
    async uploadMedia(file) {
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await fetch(`${API_BASE}/media/upload`, {
            method: 'POST',
            headers: { Authorization: `Bearer ${state.token}` },
            body: formData
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.detail || 'Upload failed');
        return data;
    },
    
    async startAnalysis(mediaId) {
        return this.request('/analysis/start', {
            method: 'POST',
            body: JSON.stringify({ media_id: mediaId })
        });
    },
    
    async getJobStatus(jobId) { return this.request(`/analysis/${jobId}/status`); },
    async getJobResult(jobId) { return this.request(`/analysis/${jobId}/result`); },
    async getUser() { return this.request('/auth/me'); }
};

// --- CORE LOGIC ---

function navigateTo(pageId) {
    // Fade out current
    const current = document.querySelector('.page.active');
    if(current) {
        current.style.opacity = '0';
        current.style.transform = 'translateY(-20px)';
        setTimeout(() => current.classList.remove('active'), 300);
    }

    // Fade in new
    setTimeout(() => {
        document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
        const newPage = document.getElementById(`${pageId}-page`);
        if(newPage) {
            newPage.classList.add('active');
            requestAnimationFrame(() => {
                newPage.style.opacity = '1';
                newPage.style.transform = 'translateY(0)';
            });
        }
    }, 300);

    // Update Nav
    document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
    document.querySelector(`[data-page="${pageId}"]`)?.classList.add('active');
    
    VFX.refresh();
}

// File Upload Handler with Drag Visuals
function initFileUpload() {
    const zone = document.getElementById('uploadZone');
    const input = document.getElementById('fileInput');

    zone.addEventListener('click', () => input.click());
    input.addEventListener('change', (e) => handleFiles(e.target.files));

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        zone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    zone.addEventListener('dragenter', () => zone.classList.add('dragover'));
    zone.addEventListener('dragleave', () => zone.classList.remove('dragover'));
    zone.addEventListener('drop', (e) => {
        zone.classList.remove('dragover');
        handleFiles(e.dataTransfer.files);
    });

    function handleFiles(files) {
        if(files.length > 0) {
            const file = files[0];
            state.selectedFile = file;
            
            // Visual Update
            document.getElementById('fileName').textContent = file.name;
            document.getElementById('fileSize').textContent = formatBytes(file.size);
            document.getElementById('uploadPreview').style.display = 'block';
            
            // Auto scroll to preview
            document.getElementById('uploadPreview').scrollIntoView({ behavior: 'smooth' });
        }
    }
}

// Analysis Workflow
async function startAnalysis() {
    if (!state.selectedFile || !state.token) {
        if(!state.token) showAuthModal();
        return;
    }

    navigateTo('processing');
    
    try {
        updateStatus('uploading', 0, 'Uploading Media...');
        const upload = await api.uploadMedia(state.selectedFile);
        
        updateStatus('queued', 10, 'Initializing AI Models...');
        const job = await api.startAnalysis(upload.media_id);
        
        pollStatus(job.job_id);
    } catch (e) {
        alert(e.message);
        navigateTo('upload');
    }
}

async function pollStatus(jobId) {
    const poll = async () => {
        try {
            const status = await api.getJobStatus(jobId);
            
            // Map stage to progress
            const progressMap = {
                'validating': 20,
                'extracting': 40,
                'transcribing': 50,
                'analyzing': 70,
                'fusion': 90,
                'done': 100
            };
            
            const pct = progressMap[status.stage] || 50;
            updateStatus(status.stage, pct, `Processing: ${status.stage}...`);
            
            if (status.status === 'done') {
                const result = await api.getJobResult(jobId);
                showResults(result);
            } else if (status.status === 'failed') {
                alert('Analysis failed');
                navigateTo('upload');
            } else {
                setTimeout(poll, 2000);
            }
        } catch (e) {
            console.error(e);
            setTimeout(poll, 3000);
        }
    };
    poll();
}

function updateStatus(stage, percent, text) {
    const bar = document.getElementById('progressFill');
    const txt = document.getElementById('progressText');
    const label = document.getElementById('processingStage');
    
    bar.style.width = `${percent}%`;
    txt.textContent = `${percent}%`;
    label.textContent = text;
    
    // Update stage icons
    document.querySelectorAll('.stage').forEach(el => {
        el.classList.remove('active', 'completed');
        if(el.id === `stage-${stage}`) el.classList.add('active');
    });
}

function showResults(data) {
    // Populate Score
    const score = Math.round(data.overall_score * 100);
    document.getElementById('scoreValue').textContent = `${score}%`;
    
    // Update Ring
    const circle = document.getElementById('scoreCircle');
    const offset = 283 - (283 * data.overall_score);
    circle.style.strokeDashoffset = offset;
    
    // Verdict Text
    const verdict = document.querySelector('.verdict-label');
    const desc = document.querySelector('.verdict-description');
    
    if(score < 30) {
        verdict.textContent = 'LIKELY AUTHENTIC';
        verdict.style.color = 'var(--success)';
        circle.style.stroke = 'var(--success)';
        desc.textContent = 'No significant manipulation detected.';
    } else if(score < 70) {
        verdict.textContent = 'SUSPICIOUS';
        verdict.style.color = 'var(--warning)';
        circle.style.stroke = 'var(--warning)';
        desc.textContent = 'Some anomalies detected. Manual review recommended.';
    } else {
        verdict.textContent = 'HIGHLY LIKELY FAKE';
        verdict.style.color = 'var(--error)';
        circle.style.stroke = 'var(--error)';
        desc.textContent = 'Strong evidence of manipulation found.';
    }

    navigateTo('results');
    VFX.refresh();
}

// --- UTILS ---

function formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024, sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function showAuthModal() {
    document.getElementById('authModal').classList.add('active');
}

// --- INIT ---

document.addEventListener('DOMContentLoaded', () => {
    VFX.init();
    initFileUpload();
    
    // Global Event Listeners
    document.querySelectorAll('[data-page]').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            navigateTo(btn.dataset.page);
        });
    });
    
    document.getElementById('startUploadBtn')?.addEventListener('click', startAnalysis);
    document.getElementById('newAnalysisBtn')?.addEventListener('click', () => navigateTo('upload'));
    document.getElementById('closeModal')?.addEventListener('click', () => {
        document.getElementById('authModal').classList.remove('active');
    });
    
    // Login Logic
    document.getElementById('loginForm')?.addEventListener('submit', async (e) => {
        e.preventDefault();
        const [email, pwd] = e.target.querySelectorAll('input');
        try {
            await api.login(email.value, pwd.value);
            document.getElementById('authModal').classList.remove('active');
            alert('Logged in!');
            updateNavAuth();
        } catch(err) {
            alert(err.message);
        }
    });

    updateNavAuth();
});

function updateNavAuth() {
    const btn = document.getElementById('loginBtn');
    if(state.token) {
        btn.textContent = 'My Account';
    } else {
        btn.textContent = 'Login';
    }
}
