# Interview Automation Engine - Directory Overview

## Project Structure

```
interview-engine/
│
├── 📋 Documentation
│   ├── README.md ........................ Complete documentation & guide
│   ├── QUICKSTART.md ................... 30-second setup guide
│   ├── USE_CASE.md ..................... Detailed example walkthrough
│   ├── MANIFEST.md ..................... Project deliverables & status
│   └── INDEX.md (this file) ............ Directory overview
│
├── ⚙️ Setup & Configuration
│   ├── requirements.txt ................ Python dependencies
│   ├── setup.sh ........................ MacOS/Linux setup script
│   ├── setup.bat ....................... Windows setup script
│   ├── demo.py ......................... Demonstration & testing
│   └── .gitignore (optional) ........... Git ignore patterns
│
├── 🔧 Backend (Python/Flask)
│   ├── app.py .......................... Flask API server (425 lines)
│   │   ├── GET /api/config/* .......... Configuration endpoints
│   │   ├── POST /api/interview/start .. Start interview
│   │   ├── POST /api/interview/submit  Submit answer
│   │   ├── GET /api/results/* ......... Results endpoints
│   │   ├── GET /api/report/* .......... Report generation
│   │   └── GET /api/health ............ Health check
│   │
│   ├── interview_engine.py ............ Core interview logic (230 lines)
│   │   ├── initialize_interview() ..... Setup new interview
│   │   ├── submit_answer() ............ Process answer
│   │   ├── _adapt_difficulty() ........ Change difficulty
│   │   ├── _select_next_question() .... Pick question
│   │   └── get_interview_status() ..... Status tracking
│   │
│   ├── config/
│   │   ├── __init__.py ................ Package marker
│   │   ├── config_manager.py .......... Configuration management (50 lines)
│   │   │   ├── get_roles() ............ Available roles
│   │   │   ├── get_experience_levels() Levels
│   │   │   ├── get_domains() .......... Domains
│   │   │   └── validate_role() ........ Validation
│   │   │
│   │   └── defaults.json .............. Configuration & rubric
│   │       ├── roles .................. 5 available roles
│   │       ├── experience_levels ...... 5 experience levels
│   │       ├── domains ................ 4 interview domains
│   │       ├── scoring_rubric ......... Complete 1-5 rubric
│   │       └── interview_settings ..... Interview configuration
│   │
│   ├── questions/
│   │   ├── __init__.py ................ Package marker
│   │   ├── question_manager.py ........ Question management (50 lines)
│   │   │   ├── get_question() ......... Random/specific question
│   │   │   ├── get_questions_for_role_difficulty()
│   │   │   ├── get_all_difficulties_for_role()
│   │   │   └── validate_question() .... Validation
│   │   │
│   │   └── question_bank.json ......... 34+ curated questions
│   │       ├── Software Engineer ...... 10 questions
│   │       ├── Data Scientist ......... 6 questions
│   │       ├── Product Manager ........ 6 questions
│   │       ├── DevOps Engineer ........ 6 questions
│   │       └── Frontend Developer ..... 6 questions
│   │
│   ├── scoring/
│   │   ├── __init__.py ................ Package marker
│   │   └── scoring_engine.py .......... Real-time scoring (280 lines)
│   │       ├── score_response() ....... Main scoring function
│   │       ├── _score_clarity() ....... Clarity dimension
│   │       ├── _score_accuracy() ...... Accuracy dimension
│   │       ├── _score_completeness() . Completeness dimension
│   │       ├── _score_confidence() .... Confidence dimension
│   │       └── _generate_insights() .. Strength/gap analysis
│   │
│   ├── analysis/
│   │   ├── __init__.py ................ Package marker
│   │   └── analysis_engine.py ......... Analysis & insights (240 lines)
│   │       ├── analyze_interview() .... Main analysis function
│   │       ├── _calculate_aggregate_scores()
│   │       ├── _analyze_dimensions() . Per-dimension analysis
│   │       ├── _identify_patterns() .. Pattern detection
│   │       ├── _analyze_consistency() Consistency metrics
│   │       ├── _generate_recommendations()
│   │       └── _generate_summary() ... Executive summary
│   │
│   ├── reports/
│   │   ├── __init__.py ................ Package marker
│   │   ├── report_generator.py ........ Report generation (300 lines)
│   │   │   ├── generate_json_report() JSON export
│   │   │   ├── generate_html_report() HTML export
│   │   │   ├── generate_pdf_report()  PDF export
│   │   │   └── _build_html_report()   HTML builder
│   │   │
│   │   └── output/ (generated)
│   │       └── *.json, *.html, *.pdf
│   │
│   └── __init__.py ..................... Package marker
│
├── 🎨 Frontend (HTML/CSS/JS)
│   ├── index.html ...................... Complete UI (220 lines)
│   │   ├── <!-- Setup Screen -->
│   │   │   └── Candidate information form
│   │   │
│   │   ├── <!-- Interview Screen -->
│   │   │   ├── Progress bar
│   │   │   ├── Question display
│   │   │   ├── Answer textarea
│   │   │   ├── Follow-up support
│   │   │   └── Submit/Skip buttons
│   │   │
│   │   ├── <!-- Results Screen -->
│   │   │   ├── Overall score display
│   │   │   ├── Dimension score cards
│   │   │   ├── Patterns section
│   │   │   ├── Recommendations
│   │   │   ├── Export buttons
│   │   │   └── Restart button
│   │   │
│   │   └── <!-- Loading Screen -->
│   │       └── Spinner animation
│   │
│   ├── styles.css ...................... Professional styling (550 lines)
│   │   ├── Root CSS variables
│   │   ├── Body & container styles
│   │   ├── Navbar styling
│   │   ├── Screen transitions
│   │   ├── Form styling
│   │   ├── Button styling
│   │   ├── Interview UI styles
│   │   ├── Results display styles
│   │   ├── Score visualization
│   │   ├── Responsive design
│   │   └── Animations & transitions
│   │
│   └── script.js ....................... Interactive logic (350 lines)
│       ├── State management
│       ├── API communication
│       │   ├── loadConfiguration()
│       │   ├── handleStartInterview()
│       │   ├── handleSubmitAnswer()
│       │   └── exportReport()
│       │
│       ├── Screen navigation
│       │   ├── showScreen()
│       │   └── displayQuestion()
│       │
│       ├── Results display
│       │   └── displayResults()
│       │
│       ├── Event listeners
│       │   ├── Form submission
│       │   ├── Button clicks
│       │   └── Character counting
│       │
│       └── Utilities
│           ├── downloadFile()
│           ├── showError()
│           └── showSuccess()
│
└── 📦 Root Files
    ├── README.md
    ├── QUICKSTART.md
    ├── USE_CASE.md
    ├── MANIFEST.md
    ├── INDEX.md (this file)
    ├── requirements.txt
    ├── setup.sh
    ├── setup.bat
    └── demo.py
```

---

## Quick Navigation

### I want to...

**Get Started Quickly**
→ Read `QUICKSTART.md`
→ Run `bash setup.sh` (or `setup.bat`)
→ Start `backend/app.py`
→ Open `frontend/index.html`

**Understand the Architecture**
→ Read `README.md` - Architecture section
→ Review `MANIFEST.md` - Technical details
→ Look at `backend/app.py` - API structure

**See How It Works**
→ Read `USE_CASE.md` - Complete example
→ Run `python demo.py` - Live demonstration
→ Review `backend/interview_engine.py` - Logic flow

**Add Custom Questions**
→ Edit `backend/questions/question_bank.json`
→ Add new question object
→ Specify role, difficulty, key points

**Customize Scoring**
→ Edit `backend/scoring/scoring_engine.py`
→ Modify dimension scoring methods
→ Adjust weighting logic

**Deploy to Production**
→ Read `README.md` - Deployment section
→ Add authentication to `backend/app.py`
→ Configure database
→ Use HTTPS/TLS

---

## File Statistics

| Category | Files | Total Lines | Language |
|----------|-------|------------|----------|
| Documentation | 5 | 1500+ | Markdown |
| Backend Core | 2 | 655 | Python |
| Config & Questions | 2 | 50+ | Python/JSON |
| Scoring | 1 | 280 | Python |
| Analysis | 1 | 240 | Python |
| Reporting | 1 | 300 | Python |
| Frontend | 3 | 1120 | HTML/CSS/JS |
| Setup & Test | 3 | 200+ | Shell/Batch/Python |
| **TOTAL** | **19** | **5000+** | - |

---

## Key Components Explained

### Backend (`backend/app.py`)
- RESTful API server using Flask
- Session management for interviews
- Routes for all operations
- CORS enabled for frontend communication

### Interview Engine (`interview_engine.py`)
- Manages interview lifecycle
- Tracks candidate progress
- Handles answer submission
- Implements adaptive difficulty
- Stores interview state

### Scoring Engine (`scoring/scoring_engine.py`)
- Evaluates responses on 4 dimensions
- Uses text analysis for scoring
- Detects key concepts
- Identifies hesitations
- Generates per-question insights

### Analysis Engine (`analysis/analysis_engine.py`)
- Aggregates all scores
- Identifies patterns
- Calculates consistency
- Generates recommendations
- Creates summary assessment

### Report Generator (`reports/report_generator.py`)
- Exports to JSON format
- Creates HTML reports with styling
- Generates PDF documents (optional)
- Stores reports to disk

### Frontend (`index.html`, `styles.css`, `script.js`)
- Responsive web interface
- Real-time interaction
- API communication
- Result visualization
- Report download

---

## API Endpoints at a Glance

```
Configuration
  GET /api/config/roles
  GET /api/config/experience-levels
  GET /api/config/domains
  GET /api/config/settings

Interview Management
  POST /api/interview/start
  GET /api/interview/status/{session_id}
  GET /api/interview/question/{session_id}
  POST /api/interview/submit/{session_id}

Results & Export
  GET /api/results/{session_id}
  GET /api/report/{session_id}/json
  GET /api/report/{session_id}/html
  GET /api/report/{session_id}/pdf

System
  GET /api/health
```

---

## Question Bank Organization

```
question_bank.json
├── Software Engineer (10 questions)
│   ├── Easy (3) ......... Variables, collections, version control
│   ├── Intermediate (3) . OOP, complexity, REST APIs
│   ├── Hard (3) ......... Caching, CAP theorem, debugging
│   └── Expert (1) ....... Large-scale system design
│
├── Data Scientist (6 questions)
│   ├── Easy (2) ......... ML concepts, metrics
│   └── Intermediate (4) . Feature engineering, imbalanced data
│
├── Product Manager (6 questions)
│   ├── Easy (1) ......... PM role explanation
│   └── Intermediate (5) . Feature building, decision making
│
├── DevOps Engineer (6 questions)
│   ├── Easy (1) ......... Docker vs VM
│   └── Intermediate (5) . CI/CD, Kubernetes, resilience
│
└── Frontend Developer (6 questions)
    ├── Easy (1) ......... Rendering concepts
    └── Intermediate (5) . React hooks, state management
```

---

## Scoring Rubric at a Glance

All dimensions use 1-5 scale:

**Clarity:** Is the answer well-organized and easy to understand?
**Accuracy:** Is the answer technically correct?
**Completeness:** Does it cover all aspects with examples?
**Confidence:** Is the candidate speaking with certainty?

Each dimension includes detailed rubric definitions in `config/defaults.json`.

---

## Workflow Overview

```
1. SETUP
   User fills: name, email, role, experience, domain
   ↓
2. INITIALIZATION
   Interview engine starts
   First question selected based on experience level
   ↓
3. INTERVIEW LOOP (for each question)
   a) Question displayed
   b) Candidate types answer
   c) Candidate submits (or skips)
   d) Answer scored in real-time (1-5 each dimension)
   e) Difficulty adapted based on score
   f) Next question selected
   ↓
4. AFTER 10 QUESTIONS
   Interview completed
   ↓
5. ANALYSIS
   All results analyzed
   Patterns identified
   Recommendations generated
   ↓
6. REPORTING
   Results displayed on screen
   Reports generated (JSON/HTML/PDF)
   Candidate can download
```

---

## Technology Stack

**Backend:**
- Python 3.8+
- Flask (web framework)
- Flask-CORS (cross-origin support)

**Frontend:**
- HTML5 (semantic markup)
- CSS3 (modern styling)
- Vanilla JavaScript (no dependencies)

**Reporting:**
- JSON (built-in)
- HTML (Jinja2 templates)
- PDF (WeasyPrint)

**Deployment:**
- Python interpreter
- Flask development server
- HTTP server (Python -m http.server)

---

## Dependencies

See `requirements.txt`:
```
Flask==2.3.2
Flask-CORS==4.0.0
Werkzeug==2.3.6
weasyprint==59.0 (optional, for PDF)
```

---

## Next Steps

1. **First Time?** → Run `bash setup.sh` then `python demo.py`
2. **Want Quick Start?** → See `QUICKSTART.md`
3. **Understanding Flow?** → Read `USE_CASE.md`
4. **Need Full Docs?** → Check `README.md`
5. **System Ready?** → Run backend and frontend servers

---

## File Locations Quick Reference

| What | Where |
|------|-------|
| Main API server | `backend/app.py` |
| Interview logic | `backend/interview_engine.py` |
| Configuration | `backend/config/defaults.json` |
| Questions | `backend/questions/question_bank.json` |
| Scoring logic | `backend/scoring/scoring_engine.py` |
| Analysis logic | `backend/analysis/analysis_engine.py` |
| Report generation | `backend/reports/report_generator.py` |
| Web interface | `frontend/index.html` |
| Styling | `frontend/styles.css` |
| Interaction | `frontend/script.js` |
| Python deps | `requirements.txt` |
| Setup (Unix) | `setup.sh` |
| Setup (Windows) | `setup.bat` |
| Demo script | `demo.py` |

---

**Ready to use!** Start with `QUICKSTART.md` and have fun! 🚀
