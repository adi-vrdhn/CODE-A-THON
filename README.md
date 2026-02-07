# CODE-A-THON

# Interview Automation Engine

A comprehensive automated technical interview platform with real-time scoring, adaptive difficulty, and detailed analysis.

## Features

### 1. SETUP
- ✅ Interview configuration management (role, experience level, domain)
- ✅ Dynamic question bank with 20+ curated questions
- ✅ 1–5 scale scoring rubric
- ✅ Interview settings management

### 2. EXECUTION
- ✅ Real-time question presentation
- ✅ Candidate response capture with metadata
- ✅ Per-question follow-up questions
- ✅ Adaptive difficulty adjustment based on performance
- ✅ Progress tracking across interview

### 3. REAL-TIME SCORING
Four dimension evaluation:
- **Clarity** (1–5): Organization, grammar, structure, ease of understanding
- **Technical Accuracy** (1–5): Correctness, depth, proper terminology  
- **Completeness** (1–5): All aspects, examples, edge cases
- **Confidence** (1–5): Hesitation, tone, consistency, response length

### 4. ANALYSIS
- ✅ Aggregate scoring across all questions
- ✅ Pattern identification (strengths, weak areas)
- ✅ Performance consistency analysis
- ✅ Dimension-wise performance trends
- ✅ Actionable recommendations

### 5. EXPORT
- ✅ JSON report with full data
- ✅ HTML report with visualizations
- ✅ PDF report (optional)
- ✅ All scores stored and analyzed

## Architecture

```
interview-engine/
├── backend/
│   ├── config/
│   │   ├── config_manager.py       # Configuration management
│   │   └── defaults.json           # Default settings & rubric
│   ├── questions/
│   │   ├── question_manager.py     # Question bank management
│   │   └── question_bank.json      # 20+ questions by role/difficulty
│   ├── scoring/
│   │   └── scoring_engine.py       # Real-time scoring engine
│   ├── analysis/
│   │   └── analysis_engine.py      # Results analysis & insights
│   ├── reports/
│   │   └── report_generator.py     # Report generation (JSON/HTML/PDF)
│   ├── interview_engine.py         # Core interview execution logic
│   └── app.py                      # Flask API server
└── frontend/
    ├── index.html                  # UI markup
    ├── styles.css                  # Styling
    └── script.js                   # Interactive functionality
```

## Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js/npm (optional, for frontend tooling)

### Backend Setup

1. **Clone and navigate:**
   ```bash
   cd interview-engine
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Flask backend:**
   ```bash
   cd backend
   python app.py
   ```
   - Server runs on `http://localhost:5000`

### Frontend Setup

1. **Open frontend in browser:**
   ```bash
   cd frontend
   # Open index.html in your browser or use a local server
   python -m http.server 8000
   ```
   - Navigate to `http://localhost:8000`

## Usage

### 1. Start Interview
- Fill candidate information (name, email, role, experience)
- Select interview domain
- Click "Start Interview"

### 2. Answer Questions
- Read question carefully
- Type detailed answer (min. 10 chars)
- Optionally answer follow-up question
- Click "Submit Answer" or "Skip Question"

### 3. Real-Time Scoring
System evaluates on 4 dimensions:
- Responses are scored 1–5 in real-time
- **Scores are not revealed during interview** (as per requirements)
- Difficulty adapts dynamically based on performance

### 4. View Results
After interview completion:
- Overall score (1–5)
- Per-dimension scores with visualizations
- Key patterns identified
- Personalized recommendations

### 5. Export Report
- **JSON**: Full structured data
- **HTML**: Formatted report with charts
- **PDF**: Professional PDF report (requires weasyprint)

## API Endpoints

### Configuration
- `GET /api/config/roles` - Available roles
- `GET /api/config/experience-levels` - Experience levels
- `GET /api/config/domains` - Interview domains
- `GET /api/config/settings` - Interview settings

### Interview Management
- `POST /api/interview/start` - Start new interview
- `GET /api/interview/status/<session_id>` - Get interview status
- `GET /api/interview/question/<session_id>` - Get current question
- `POST /api/interview/submit/<session_id>` - Submit answer

### Results & Analysis
- `GET /api/results/<session_id>` - Get results and analysis
- `GET /api/report/<session_id>/json` - Generate JSON report
- `GET /api/report/<session_id>/html` - Generate HTML report
- `GET /api/report/<session_id>/pdf` - Generate PDF report

## Question Bank

### Roles Covered
1. **Software Engineer** - Technical, system design, algorithms
2. **Data Scientist** - ML, statistics, feature engineering
3. **Product Manager** - Product strategy, decision-making
4. **DevOps Engineer** - Infrastructure, CI/CD, containers
5. **Frontend Developer** - Web, React, performance

### Difficulty Levels
- **Easy**: 3 questions per role
- **Intermediate**: 3 questions per role
- **Hard**: 3 questions per role
- **Expert**: 1 question per role

### Adaptive Difficulty
- Starts based on experience level
- Increases on scores ≥ 4.5
- Decreases on scores < 2.5
- Maintains difficulty otherwise

## Scoring Methodology

### Clarity (1–5)
- **1**: Incoherent, difficult to understand
- **2**: Somewhat unclear, needs clarification
- **3**: Adequately clear, minor issues
- **4**: Clear and well-organized
- **5**: Excellent clarity, perfect organization

Evaluated on:
- Organization of thought
- Grammar and structure
- Ease of understanding
- Absence of filler words

### Technical Accuracy (1–5)
- **1**: Incorrect concepts, major errors
- **2**: Partially correct, some errors
- **3**: Mostly correct with minor gaps
- **4**: Correct with proper terminology
- **5**: Highly accurate, expert-level understanding

Evaluated on:
- Coverage of key points
- Correctness of concepts
- Use of proper terminology
- Depth of explanation

### Completeness (1–5)
- **1**: Minimal response, many gaps
- **2**: Partial answer, notable omissions
- **3**: Addresses main points, few examples
- **4**: Comprehensive with examples
- **5**: Complete with edge cases, thorough examples

Evaluated on:
- All aspects addressed
- Examples provided
- Edge cases considered
- Response length and detail

### Confidence (1–5)
- **1**: Very uncertain, many hesitations
- **2**: Uncertain, some hesitations
- **3**: Moderately confident
- **4**: Confident answer
- **5**: Very confident and consistent

Heuristic based on:
- Hesitation indicators (um, uh, like, maybe)
- Uncertainty phrases
- Confident/assertive language
- Response consistency

## Configuration Files

### defaults.json
```json
{
  "roles": ["Software Engineer", "Data Scientist", ...],
  "experience_levels": ["Intern", "Junior", "Mid-level", "Senior", "Lead"],
  "domains": ["Technical", "Behavioral", "Problem-Solving", "System Design"],
  "scoring_rubric": { ... },
  "interview_settings": {
    "max_questions": 10,
    "max_followups_per_question": 1,
    "reveal_scores": false
  }
}
```

### question_bank.json
```json
{
  "Software Engineer": {
    "Easy": [...],
    "Intermediate": [...],
    "Hard": [...],
    "Expert": [...]
  },
  ...
}
```

## Analysis Output

### Aggregate Scores
```json
{
  "clarity": 3.8,
  "accuracy": 4.1,
  "completeness": 3.5,
  "confidence": 3.2,
  "overall": 3.65
}
```

### Patterns Identified
- Strongest/weakest dimensions
- Consistency analysis
- Performance trends
- Technical vs communication balance

### Recommendations
- Personalized improvement areas
- Actionable next steps
- Role-specific guidance

## Rules & Guidelines

1. **No Score Reveal**: Scores are never shown during interview
2. **One Follow-up Per Question**: Max one follow-up questions per query
3. **Professional Tone**: System remains neutral and professional
4. **Adaptive Difficulty**: Questions adjust based on performance
5. **Data Persistence**: All results stored for review/export

## Customization

### Add New Questions
Edit `backend/questions/question_bank.json`:
```json
{
  "id": "SE-E-004",
  "text": "Your question here?",
  "domain": "Technical",
  "context": "Optional context",
  "sample_answer": "...",
  "key_points": ["point1", "point2"],
  "follow_up": "Follow-up question?"
}
```

### Adjust Scoring Weights
Modify `backend/scoring/scoring_engine.py` scoring methods to change weighting.

### Change Interview Settings
Update `backend/config/defaults.json`:
```json
{
  "max_questions": 10,
  "reveal_scores": false
}
```

## Future Enhancements

- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] Authentication & user management
- [ ] Interview session persistence
- [ ] Advanced analytics dashboard
- [ ] AI-powered follow-ups
- [ ] Live video interview support
- [ ] Mobile app
- [ ] Multi-language support

## Troubleshooting

### Flask server won't start
```bash
# Make sure port 5000 is available
# Kill existing process on port 5000
lsof -ti :5000 | xargs kill -9
```

### CORS errors
- Flask-CORS is configured for all origins
- Update `app.py` for production security

### PDF generation fails
```bash
# Install weasyprint dependencies
pip install weasyprint
```

## File Structure

```
interview-engine/
├── backend/
│   ├── __init__.py
│   ├── app.py (425 lines)
│   ├── interview_engine.py (230 lines)
│   ├── config/
│   │   ├── config_manager.py (50 lines)
│   │   └── defaults.json
│   ├── questions/
│   │   ├── question_manager.py (50 lines)
│   │   └── question_bank.json (350+ questions)
│   ├── scoring/
│   │   └── scoring_engine.py (280 lines)
│   ├── analysis/
│   │   └── analysis_engine.py (240 lines)
│   └── reports/
│       └── report_generator.py (300 lines)
├── frontend/
│   ├── index.html (220 lines)
│   ├── styles.css (550 lines)
│   └── script.js (350 lines)
├── requirements.txt
└── README.md (this file)
```

## Technical Stack

- **Backend**: Python, Flask, Flask-CORS
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Reporting**: JSON, HTML, WeasyPrint (PDF)
- **Architecture**: RESTful API with session management

## License

Open source - Use freely for codeathons and interviews.

## Support

For issues or questions, check the architecture documentation above or review the inline code comments.

---

**Made with ❤️ for Interview Automation**
