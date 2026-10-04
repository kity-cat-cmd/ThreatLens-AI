/**
 * ThreatLens AI - Frontend Application
 */

const API_BASE = '/api/v1';

// State management
let typeChart = null;
let statusChart = null;
let currentThreats = [];

// Initialize application
document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initCharts();
    loadStatistics();
    initForms();
});

// Navigation handling
function initNavigation() {
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const target = link.getAttribute('href').substring(1);

            // Update active nav link
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            link.classList.add('active');

            // Show target section
            document.querySelectorAll('.content-section').forEach(section => {
                section.style.display = 'none';
            });
            document.getElementById(target).style.display = 'block';

            // Load data for the section
            if (target === 'threats') {
                loadThreats();
            } else if (target === 'reports') {
                loadReports();
            } else if (target === 'dashboard') {
                loadStatistics();
            }
        });
    });
}

// Charts initialization
function initCharts() {
    const typeCtx = document.getElementById('typeChart').getContext('2d');
    typeChart = new Chart(typeCtx, {
        type: 'doughnut',
        data: {
            labels: ['Malware', 'Intrusion', 'Data Breach', 'DoS', 'Policy Violation'],
            datasets: [{
                data: [0, 0, 0, 0, 0],
                backgroundColor: ['#dc3545', '#fd7e14', '#ffc107', '#0dcaf0', '#6c757d']
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'bottom' }
            }
        }
    });

    const statusCtx = document.getElementById('statusChart').getContext('2d');
    statusChart = new Chart(statusCtx, {
        type: 'bar',
        data: {
            labels: ['Open', 'Investigating', 'Resolved', 'False Positive'],
            datasets: [{
                data: [0, 0, 0, 0],
                backgroundColor: ['#0dcaf0', '#ffc107', '#198754', '#6c757d']
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
}

// Load statistics
async function loadStatistics() {
    try {
        const response = await fetch(`${API_BASE}/stats`);
        const stats = await response.json();

        // Update stat cards
        document.getElementById('stat-total').textContent = stats.total || 0;
        document.getElementById('stat-recent').textContent = stats.recent_count || 0;
        document.getElementById('stat-critical').textContent = stats.by_severity?.critical || 0;
        document.getElementById('stat-high').textContent = stats.by_severity?.high || 0;

        const medium = stats.by_severity?.medium || 0;
        const low = stats.by_severity?.low || 0;
        document.getElementById('stat-other').textContent = medium + low;

        // Update charts
        updateCharts(stats);
    } catch (error) {
        console.error('Failed to load statistics:', error);
        showToast('Failed to load statistics', 'danger');
    }
}

// Update charts with data
function updateCharts(stats) {
    const typeData = [
        stats.by_type?.malware || 0,
        stats.by_type?.intrusion || 0,
        stats.by_type?.data_breach || 0,
        stats.by_type?.dos || 0,
        stats.by_type?.policy_violation || 0
    ];
    typeChart.data.datasets[0].data = typeData;
    typeChart.update();

    const statusData = [
        stats.by_status?.open || 0,
        stats.by_status?.investigating || 0,
        stats.by_status?.resolved || 0,
        stats.by_status?.false_positive || 0
    ];
    statusChart.data.datasets[0].data = statusData;
    statusChart.update();
}

// Load threats
async function loadThreats() {
    try {
        const severity = document.getElementById('filter-severity').value;
        const status = document.getElementById('filter-status').value;

        let url = `${API_BASE}/threats?page=1&page_size=100`;
        if (severity) url += `&severity=${severity}`;
        if (status) url += `&status=${status}`;

        const response = await fetch(url);
        const data = await response.json();

        currentThreats = data.threats || [];
        renderThreatsTable(currentThreats);
    } catch (error) {
        console.error('Failed to load threats:', error);
        showToast('Failed to load threats', 'danger');
    }
}

// Render threats table
function renderThreatsTable(threats) {
    const tbody = document.getElementById('threats-table-body');

    if (threats.length === 0) {
        tbody.innerHTML = '<tr><td colspan="8" class="text-center text-muted">No threats found</td></tr>';
        return;
    }

    tbody.innerHTML = threats.map(threat => `
        <tr>
            <td>${threat.id}</td>
            <td>${escapeHtml(threat.title)}</td>
            <td><span class="badge bg-secondary">${threat.type}</span></td>
            <td><span class="badge badge-${threat.severity}">${threat.severity.toUpperCase()}</span></td>
            <td>${threat.source_ip || '-'}</td>
            <td><span class="badge badge-${threat.status}">${formatStatus(threat.status)}</span></td>
            <td>${formatDate(threat.created_at)}</td>
            <td>
                <button class="btn btn-sm btn-primary btn-action" onclick="analyzeThreat(${threat.id})">
                    <i class="fas fa-brain"></i> Analyze
                </button>
            </td>
        </tr>
    `).join('');
}

// Analyze threat
async function analyzeThreat(threatId) {
    const modal = new bootstrap.Modal(document.getElementById('analysisModal'));
    modal.show();

    const content = document.getElementById('analysis-content');
    content.innerHTML = `
        <div class="text-center">
            <div class="spinner-border text-primary" role="status"></div>
            <p class="mt-2">Analyzing threat #${threatId}...</p>
        </div>
    `;

    try {
        const response = await fetch(`${API_BASE}/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ threat_id: threatId, include_recommendations: true })
        });

        if (!response.ok) throw new Error('Analysis failed');

        const result = await response.json();
        renderAnalysisResult(result);
    } catch (error) {
        console.error('Analysis failed:', error);
        content.innerHTML = `
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-triangle me-2"></i>
                Analysis failed. Please try again.
            </div>
        `;
    }
}

// Render analysis result
function renderAnalysisResult(result) {
    const content = document.getElementById('analysis-content');
    const severityClass = result.severity_score >= 8 ? 'severity-critical' :
                          result.severity_score >= 6 ? 'severity-high' :
                          result.severity_score >= 4 ? 'severity-medium' : 'severity-low';

    content.innerHTML = `
        <div class="row">
            <div class="col-md-4 text-center">
                <h6>AI Severity Score</h6>
                <div class="severity-score ${severityClass}">${result.severity_score}/10</div>
                <small class="text-muted">Confidence: ${(result.confidence * 100).toFixed(0)}%</small>
                <div class="mt-2">
                    <small class="text-muted">Model: ${result.model_used}</small>
                </div>
            </div>
            <div class="col-md-8">
                <div class="analysis-section">
                    <h6><i class="fas fa-info-circle me-1"></i>Summary</h6>
                    <p>${escapeHtml(result.summary)}</p>
                </div>
                <div class="analysis-section">
                    <h6><i class="fas fa-search me-1"></i>Technical Analysis</h6>
                    <p>${escapeHtml(result.technical_analysis)}</p>
                </div>
                <div class="analysis-section">
                    <h6><i class="fas fa-lightbulb me-1"></i>Recommendations</h6>
                    <ul>
                        ${result.recommendations.map(r => `<li>${escapeHtml(r)}</li>`).join('')}
                    </ul>
                </div>
            </div>
        </div>
    `;
}

// Load reports
async function loadReports() {
    try {
        const response = await fetch(`${API_BASE}/reports?page=1&page_size=100`);
        const data = await response.json();

        const tbody = document.getElementById('reports-table-body');
        const reports = data.reports || [];

        if (reports.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">No reports yet</td></tr>';
            return;
        }

        tbody.innerHTML = reports.map(report => `
            <tr>
                <td>${report.id}</td>
                <td>${escapeHtml(report.title)}</td>
                <td>${report.threat_id || '-'}</td>
                <td>${formatDate(report.created_at)}</td>
                <td>
                    <button class="btn btn-sm btn-info btn-action" onclick="viewReport(${report.id})">
                        <i class="fas fa-eye"></i> View
                    </button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Failed to load reports:', error);
        showToast('Failed to load reports', 'danger');
    }
}

// View report (placeholder)
function viewReport(reportId) {
    showToast('Report viewing feature coming soon', 'info');
}

// Initialize forms
function initForms() {
    const form = document.getElementById('add-threat-form');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = new FormData(form);
        const threatData = {
            title: formData.get('title'),
            type: formData.get('type'),
            severity: formData.get('severity'),
            source_ip: formData.get('source_ip') || null,
            description: formData.get('description')
        };

        try {
            const response = await fetch(`${API_BASE}/threats`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(threatData)
            });

            if (!response.ok) throw new Error('Failed to create threat');

            showToast('Threat reported successfully', 'success');

            // Close modal and reset form
            bootstrap.Modal.getInstance(document.getElementById('addThreatModal')).hide();
            form.reset();

            // Reload threats
            loadThreats();
        } catch (error) {
            console.error('Failed to create threat:', error);
            showToast('Failed to report threat', 'danger');
        }
    });

    // Filter change handlers
    document.getElementById('filter-severity').addEventListener('change', loadThreats);
    document.getElementById('filter-status').addEventListener('change', loadThreats);
}

// Utility functions
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function formatStatus(status) {
    const statusMap = {
        'open': 'Open',
        'investigating': 'Investigating',
        'resolved': 'Resolved',
        'false_positive': 'False Positive'
    };
    return statusMap[status] || status;
}

// Toast notifications
function showToast(message, type = 'info') {
    const container = document.querySelector('.toast-container') || createToastContainer();
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    container.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    toast.addEventListener('hidden.bs.toast', () => toast.remove());
}

function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
    return container;
}
