const API_BASE = 'http://localhost:5000/api';

let currentSession = null;
let currentQuestionIndex = 0;
let pendingFollowup = false;

document.addEventListener('DOMContentLoaded', async () => {
    await loadConfig();
    setupEventListeners();
});

async function loadConfig() {
    try {
        const response = await fetch(`${API_BASE}/config`);
        const config = await response.json();
        
        populateSelect('role', config.roles);
        populateSelect('experience', config.experience_levels);
        populateSelect('domain', config.domains);
    } catch (error) {
        console.error('Error loading config:', error);
        alert('Failed to load configuration');
    }
}

function populateSelect(id, options) {
    const select = document.getElementById(id);
    if (!select) return;
    
    options.forEach(opt => {
        const option = document.createElement('option');
        option.value = opt;
        option.textContent = opt;
        select.appendChild(option);
    });
}

function setupEventListeners() {
    const setupForm = document.getElementById('setup-form');
    const submitBtn = document.getElementById('submit-btn');
    const skipBtn = document.getElementById('skip-btn');
    const restartBtn = document.getElementById('restart-btn');
    const exportJsonBtn = document.getElementById('export-json-btn');
    const exportHtmlBtn = document.getElementById('export-html-btn');
    const answerTextarea = document.getElementById('answer-textarea');
    
    if (setupForm) setupForm.addEventListener('submit', startInterview);
    if (submitBtn) submitBtn.addEventListener('click', submitAnswer);
    if (skipBtn) skipBtn.addEventListener('click', skipQuestion);
    if (restartBtn) restartBtn.addEventListener('click', restartInterview);
    if (exportJsonBtn) exportJsonBtn.addEventListener('click', () => exportReport('json'));
    if (exportHtmlBtn) exportHtmlBtn.addEventListener('click', () => exportReport('html'));
    if (answerTextarea) answerTextarea.addEventListener('input', updateCharCount);
}

function updateCharCount() {
    const textarea = document.getElementById('answer-textarea');
    const charCount = document.getElementById('char-count');
    charCount.textContent = textarea.value.length;
}

async function startInterview(e) {
    e.preventDefault();
    
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const role = document.getElementById('role').value;
    const experience = document.getElementById('experience').value;
    const domain = document.getElementById('domain').value;
    
    if (!name || !email || !role || !experience || !domain) {
        alert('Please fill all fields');
        return;
    }
    
    showLoadingScreen(true);
    
    try {
        const response = await fetch(`${API_BASE}/session/start`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, role, experience, domain })
        });
        
        const data = await response.json();
        
        if (data.error) {
            alert(`Error: ${data.error}`);
            return;
        }
        
        currentSession = data.session_id;
        currentQuestionIndex = 0;
        
        document.getElementById('total-questions').textContent = data.total_questions;
        
        switchScreen('interview-screen');
        loadQuestion(0);
    } catch (error) {
        console.error('Error starting interview:', error);
        alert('Failed to start interview');
    } finally {
        showLoadingScreen(false);
    }
}

async function loadQuestion(index) {
    showLoadingScreen(true);
    
    try {
        const response = await fetch(`${API_BASE}/session/${currentSession}/question/${index}`);
        const question = await response.json();
        
        if (question.error) {
            completeInterview();
            return;
        }
        
        document.getElementById('question-text').textContent = question.text;
        document.getElementById('difficulty-badge').textContent = question.difficulty || 'Medium';
        document.getElementById('difficulty-badge').className = `difficulty-badge ${(question.difficulty || 'medium').toLowerCase()}`;
        document.getElementById('question-number').textContent = index + 1;
        
        if (question.context) {
            document.getElementById('question-context').innerHTML = `<p><strong>Context:</strong> ${question.context}</p>`;
        } else {
            document.getElementById('question-context').innerHTML = '';
        }
        
        document.getElementById('answer-textarea').value = '';
        document.getElementById('followup-textarea').value = '';
        document.getElementById('follow-up-question').textContent = '';
        document.getElementById('follow-up-section').style.display = 'none';
        document.getElementById('score-display').style.display = 'none';
        document.getElementById('submit-btn').textContent = 'Submit Answer';
        
        currentQuestionIndex = index;
        pendingFollowup = false;
        updateProgressBar();
    } catch (error) {
        console.error('Error loading question:', error);
        alert('Failed to load question');
    } finally {
        showLoadingScreen(false);
    }
}

async function submitAnswer() {
    const answer = document.getElementById('answer-textarea').value.trim();
    
    if (!answer) {
        alert('Please provide an answer');
        return;
    }
    
    if (pendingFollowup) {
        // Move to next question after followup
        const total = parseInt(document.getElementById('total-questions').textContent);
        if (currentQuestionIndex + 1 < total) {
            loadQuestion(currentQuestionIndex + 1);
        } else {
            completeInterview();
        }
        return;
    }
    
    showLoadingScreen(true);
    
    try {
        const response = await fetch(`${API_BASE}/session/${currentSession}/answer`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                question_index: currentQuestionIndex,
                answer: answer
            })
        });
        
        const data = await response.json();
        
        // Show score
        const scoreDisplay = document.getElementById('score-display');
        scoreDisplay.textContent = `✅ Score: ${Math.round(data.score.score)}/100 - ${data.score.feedback}`;
        scoreDisplay.style.display = 'block';
        
        // Show AI-generated follow-up if available
        if (data.followup_question) {
            document.getElementById('follow-up-question').textContent = data.followup_question;
            document.getElementById('follow-up-section').style.display = 'block';
            document.getElementById('submit-btn').textContent = 'Next Question';
            pendingFollowup = true;
        } else {
            // Move to next question after short delay
            setTimeout(() => {
                const total = parseInt(document.getElementById('total-questions').textContent);
                if (data.next_question_index < total) {
                    loadQuestion(data.next_question_index);
                } else {
                    completeInterview();
                }
            }, 1500);
        }
    } catch (error) {
        console.error('Error submitting answer:', error);
        alert('Failed to submit answer');
    } finally {
        showLoadingScreen(false);
    }
}

function skipQuestion() {
    const total = parseInt(document.getElementById('total-questions').textContent);
    if (currentQuestionIndex + 1 < total) {
        loadQuestion(currentQuestionIndex + 1);
    } else {
        completeInterview();
    }
}

async function completeInterview() {
    showLoadingScreen(true);
    
    try {
        const response = await fetch(`${API_BASE}/session/${currentSession}/complete`, {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayResults(data.report);
        } else {
            alert('Failed to complete interview');
        }
    } catch (error) {
        console.error('Error completing interview:', error);
        alert('Failed to complete interview');
    } finally {
        showLoadingScreen(false);
    }
}

function displayResults(report) {
    // Overall score
    document.getElementById('overall-score').textContent = Math.round(report.overall_score);
    
    // Metrics
    const metrics = [
        { id: 'clarity', value: report.clarity },
        { id: 'accuracy', value: report.accuracy },
        { id: 'completeness', value: report.completeness },
        { id: 'confidence', value: report.confidence }
    ];
    
    metrics.forEach(m => {
        document.getElementById(`score-${m.id}`).textContent = Math.round(m.value);
        const bar = document.getElementById(`bar-${m.id}`);
        bar.style.width = `${m.value}%`;
        
        if (m.value >= 75) {
            bar.style.backgroundColor = '#10b981';
        } else if (m.value >= 50) {
            bar.style.backgroundColor = '#f59e0b';
        } else {
            bar.style.backgroundColor = '#ef4444';
        }
    });
    
    // Interpretation
    const score = report.overall_score;
    let interpretation = '';
    if (score >= 80) {
        interpretation = '🌟 Excellent performance! Strong technical understanding and communication skills.';
    } else if (score >= 60) {
        interpretation = '✅ Good performance. Some areas to strengthen further.';
    } else if (score >= 40) {
        interpretation = '📈 Fair performance. Focus on core concepts and practice.';
    } else {
        interpretation = '⚠️ Needs improvement. Review fundamentals and concepts.';
    }
    document.getElementById('level-interpretation').textContent = interpretation;
    
    // Recommendations
    const recList = document.getElementById('recommendations-list');
    recList.innerHTML = '';
    if (report.recommendations && report.recommendations.length > 0) {
        report.recommendations.forEach(rec => {
            const li = document.createElement('li');
            li.textContent = rec;
            recList.appendChild(li);
        });
    }
    
    switchScreen('results-screen');
}

async function exportReport(format) {
    try {
        const response = await fetch(`${API_BASE}/session/${currentSession}/export/${format}`);
        
        if (format === 'json') {
            const data = await response.json();
            downloadJSON(data, `interview_${currentSession}.json`);
        } else if (format === 'html') {
            const html = await response.text();
            downloadHTML(html, `interview_${currentSession}.html`);
        }
    } catch (error) {
        console.error('Error exporting report:', error);
        alert('Failed to export report');
    }
}

function downloadJSON(obj, filename) {
    const blob = new Blob([JSON.stringify(obj, null, 2)], { type: 'application/json' });
    downloadFile(blob, filename);
}

function downloadHTML(html, filename) {
    const blob = new Blob([html], { type: 'text/html' });
    downloadFile(blob, filename);
}

function downloadFile(blob, filename) {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
}

function switchScreen(screenId) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById(screenId).classList.add('active');
}

function showLoadingScreen(show) {
    const loadingScreen = document.getElementById('loading-screen');
    if (show) {
        loadingScreen.classList.add('active');
    } else {
        loadingScreen.classList.remove('active');
    }
}

function restartInterview() {
    location.reload();
}

function updateProgressBar() {
    const current = currentQuestionIndex + 1;
    const total = parseInt(document.getElementById('total-questions').textContent);
    const progress = (current / total) * 100;
    document.getElementById('progress-fill').style.width = `${progress}%`;
}