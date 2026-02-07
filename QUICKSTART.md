# Quick Start Guide

## 30-Second Setup

### MacOS/Linux:
```bash
cd interview-engine
bash setup.sh
cd backend
python app.py
```

In another terminal:
```bash
cd interview-engine/frontend
python -m http.server 8000
```

Open browser: `http://localhost:8000`

---

### Windows:
```batch
cd interview-engine
setup.bat
cd backend
python app.py
```

In another terminal (Command Prompt):
```batch
cd interview-engine\frontend
python -m http.server 8000
```

Open browser: `http://localhost:8000`

---

## What You Get

✅ **Complete Interview Automation Platform**
- Web-based UI for candidates
- Real-time scoring on 4 dimensions
- Adaptive difficulty adjustment
- Comprehensive analysis
- Multiple report formats (JSON/HTML/PDF)

### 5 Interview Roles
1. Software Engineer (10 questions)
2. Data Scientist (6 questions)
3. Product Manager (6 questions)
4. DevOps Engineer (6 questions)
5. Frontend Developer (6 questions)

### 4 Difficulty Levels
- Easy
- Intermediate
- Hard
- Expert

### Real-Time Scoring
- **Clarity**: Organization & communication
- **Accuracy**: Technical correctness
- **Completeness**: Coverage & examples
- **Confidence**: Tone & certainty

---

## Sample Interview Session

1. **Fill candidate info** (name, email, role, etc.)
2. **Answer 10 questions** (adaptive difficulty)
3. **View results** with scores and analysis
4. **Download report** (JSON/HTML/PDF)

---

## Files Overview

**Backend (Python/Flask):**
- `app.py` - Flask API server
- `interview_engine.py` - Interview execution logic
- `config/config_manager.py` - Settings management
- `questions/question_manager.py` - Question bank
- `scoring/scoring_engine.py` - Real-time scoring
- `analysis/analysis_engine.py` - Results analysis
- `reports/report_generator.py` - Report generation

**Frontend (HTML/CSS/JS):**
- `index.html` - Interview UI interface
- `styles.css` - Professional styling
- `script.js` - Interactive functionality

**Configuration:**
- `config/defaults.json` - Settings & rubric
- `questions/question_bank.json` - 34+ questions

---

## API Endpoints

### Start Interview
```bash
POST /api/interview/start
{
  "name": "John Doe",
  "email": "john@example.com",
  "role": "Software Engineer",
  "experience_level": "Mid-level",
  "domain": "Technical"
}
```

### Submit Answer
```bash
POST /api/interview/submit/{session_id}
{
  "answer": "Your detailed answer here...",
  "follow_up_response": "Optional follow-up answer"
}
```

### Get Results
```bash
GET /api/results/{session_id}
```

### Download Report
```bash
GET /api/report/{session_id}/json
GET /api/report/{session_id}/html
GET /api/report/{session_id}/pdf
```

---

## Architecture Highlights

### 1. Real-Time Scoring
Evaluates 4 dimensions simultaneously:
- Analyzes response text for clarity markers
- Checks key point coverage for accuracy
- Evaluates example presence for completeness
- Detects hesitations for confidence

### 2. Adaptive Difficulty
- Easy (Intern/Junior) → Intermediate → Hard → Expert (Lead)
- Increases on score ≥ 4.5
- Decreases on score < 2.5
- Maintains otherwise

### 3. Analysis Engine
Generates:
- Aggregate scores across all questions
- Per-dimension analysis with trends
- Pattern identification
- Consistency metrics
- Actionable recommendations

### 4. Multi-Format Reports
- **JSON**: Structured data for integration
- **HTML**: Beautiful formatted report
- **PDF**: Professional printable format

---

## Troubleshooting

### Server won't start?
```bash
# Check port 5000 is free
lsof -i :5000  # MacOS/Linux
netstat -ano | findstr :5000  # Windows
```

### Frontend can't connect?
- Backend must run on port 5000
- Frontend must have CORS enabled (it does)
- Try hard refresh: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)

### Missing dependencies?
```bash
pip install -r requirements.txt
```

---

## Features Implemented

✅ **Setup Phase**
- Configuration loading
- Role/experience/domain selection
- User profile capture

✅ **Execution Phase**
- Question presentation (one at a time)
- Answer capture with metadata
- Follow-up question support
- Progress tracking

✅ **Real-Time Scoring**
- Clarity evaluation
- Technical accuracy assessment
- Completeness checking
- Confidence heuristics
- Per-question insights

✅ **Adaptive Difficulty**
- Dynamic question selection
- Performance-based adjustment
- Difficulty progression

✅ **Analysis**: Aggregate scores, patterns, recommendations

✅ **Export**: JSON, HTML, PDF reports

✅ **UI**: Professional web interface with visualizations

---

## Key Rules

1. ✅ **No score reveal during interview**
2. ✅ **Max one follow-up per question**
3. ✅ **Neutral, professional tone**
4. ✅ **Adaptive difficulty based on scores**
5. ✅ **Real-time evaluation**

---

## Next Steps

1. Customize question bank for your domain
2. Adjust scoring weights in `scoring_engine.py`
3. Deploy to production with authentication
4. Integrate with your HR system
5. Add candidate database

---

## Support Resources

- **README.md** - Full documentation
- **USE_CASE.md** - Detailed example walkthrough
- **Code comments** - Inline documentation

---

## Tech Stack

**Backend:**
- Python 3.8+
- Flask (REST API)
- Flask-CORS (Cross-origin support)

**Frontend:**
- HTML5
- CSS3
- Vanilla JavaScript

**Reporting:**
- JSON (native)
- HTML (jinja2 templates)
- PDF (WeasyPrint)

---

**Ready to go!** Start the servers and open your browser. 🚀
