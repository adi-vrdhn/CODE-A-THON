#!/usr/bin/env python3
import os
import sys
import json
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.dirname(__file__))

from config.config_manager import ConfigManager
from questions.question_manager import QuestionManager
from scoring.scoring_engine import ScoringEngine
from analysis.analysis_engine import AnalysisEngine
from llm_agent import InterviewAgent
from reports.report_generator import ReportGenerator

app = Flask(__name__)
CORS(app)

config_manager = ConfigManager()
question_manager = QuestionManager()
scoring_engine = ScoringEngine()
analysis_engine = AnalysisEngine()
llm_agent = InterviewAgent()
report_generator = ReportGenerator()

sessions = {}

@app.route('/api/config', methods=['GET'])
def get_config():
    return jsonify({
        "roles": config_manager.get_roles(),
        "experience_levels": config_manager.get_experience_levels(),
        "domains": config_manager.get_domains(),
        "difficulties": config_manager.get_difficulty_levels(),
        "settings": config_manager.get_interview_settings()
    })

@app.route('/api/session/start', methods=['POST'])
def start_session():
    data = request.json
    session_id = f"{data['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    sessions[session_id] = {
        "candidate_name": data['name'],
        "candidate_email": data['email'],
        "role": data['role'],
        "experience": data['experience'],
        "domain": data['domain'],
        "answers": [],
        "scores": [],
        "start_time": datetime.now().isoformat()
    }
    
    num_questions = config_manager.get_interview_settings().get('max_questions', 5)
    questions = question_manager.get_questions(
        role=data['role'],
        domain=data['domain'],
        experience_level=data['experience'],
        count=num_questions
    )
    
    sessions[session_id]["questions"] = questions
    
    return jsonify({
        "session_id": session_id,
        "total_questions": len(questions),
        "first_question": questions[0] if questions else None
    })

@app.route('/api/session/<session_id>/question/<int:index>', methods=['GET'])
def get_question(session_id, index):
    if session_id not in sessions:
        return jsonify({"error": "Session not found"}), 404
    
    questions = sessions[session_id]["questions"]
    if index >= len(questions):
        return jsonify({"error": "Index out of range"}), 400
    
    return jsonify(questions[index])

@app.route('/api/session/<session_id>/answer', methods=['POST'])
def submit_answer(session_id):
    if session_id not in sessions:
        return jsonify({"error": "Session not found"}), 404
    
    data = request.json
    question_index = data.get('question_index', 0)
    answer = data.get('answer', '')
    
    # ===== DEBUG LOGS =====
    print("\n" + "="*60)
    print(f"📝 RECEIVED ANSWER: {answer[:100]}...")
    print("="*60)
    
    session = sessions[session_id]
    questions = session["questions"]
    question = questions[question_index]
    
    print(f"🤖 CALLING LLM to score question: {question.get('text', '')[:80]}...")
    print(f"   Expected concepts: {question.get('keywords', [])}")
    
    try:
        # LLM Score
        print("   ⏳ Waiting for LLM response...")
        score_result = llm_agent.score_answer(
            question=question.get('text', ''),
            answer=answer,
            expected_concepts=question.get('keywords', [])
        )
        
        print(f"✅ SCORE RESULT RECEIVED:")
        print(f"   Score: {score_result.get('score')}")
        print(f"   Clarity: {score_result.get('clarity')}")
        print(f"   Accuracy: {score_result.get('accuracy')}")
        print(f"   Completeness: {score_result.get('completeness')}")
        print(f"   Confidence: {score_result.get('confidence')}")
        print(f"   Feedback: {score_result.get('feedback')[:100]}...")
        
    except Exception as e:
        print(f"❌ ERROR SCORING ANSWER: {e}")
        score_result = {
            "score": 50,
            "clarity": 50,
            "accuracy": 50,
            "completeness": 50,
            "confidence": 50,
            "feedback": f"Error: {str(e)}"
        }
    
    session["answers"].append({
        "question_index": question_index,
        "question": question.get('text', ''),
        "answer": answer
    })
    session["scores"].append(score_result)
    
    # LLM Follow-up
    followup_question = None
    try:
        print(f"🤖 GENERATING FOLLOW-UP QUESTION...")
        followup_question = llm_agent.generate_followup(
            question=question.get('text', ''),
            answer=answer,
            question_context=question.get('context', '')
        )
        print(f"✅ FOLLOW-UP GENERATED: {followup_question[:100]}...")
    except Exception as e:
        print(f"❌ ERROR GENERATING FOLLOW-UP: {e}")
        followup_question = None
    
    print("="*60 + "\n")
    
    return jsonify({
        "score": score_result,
        "followup_question": followup_question,
        "next_question_index": question_index + 1,
        "total_questions": len(questions)
    })

@app.route('/api/session/<session_id>/complete', methods=['POST'])
def complete_interview(session_id):
    if session_id not in sessions:
        return jsonify({"error": "Session not found"}), 404
    
    session = sessions[session_id]
    scores = session["scores"]
    answers = session["answers"]
    
    overall_score = sum(s.get('score', 0) for s in scores) / len(scores) if scores else 0
    clarity = sum(s.get('clarity', 0) for s in scores) / len(scores) if scores else 0
    accuracy = sum(s.get('accuracy', 0) for s in scores) / len(scores) if scores else 0
    completeness = sum(s.get('completeness', 0) for s in scores) / len(scores) if scores else 0
    confidence = sum(s.get('confidence', 0) for s in scores) / len(scores) if scores else 0
    
    print("\n" + "="*60)
    print("🎯 GENERATING AI RECOMMENDATIONS...")
    
    try:
        recommendations = llm_agent.generate_recommendations(answers, scores)
        print(f"✅ RECOMMENDATIONS GENERATED:")
        for rec in recommendations.get('recommendations', []):
            print(f"   • {rec}")
    except Exception as e:
        print(f"❌ ERROR GENERATING RECOMMENDATIONS: {e}")
        recommendations = {"recommendations": ["Review fundamentals", "Practice more", "Build projects"]}
    
    print("="*60 + "\n")
    
    report_data = {
        "candidate_name": session["candidate_name"],
        "candidate_email": session["candidate_email"],
        "role": session["role"],
        "experience": session["experience"],
        "domain": session["domain"],
        "overall_score": overall_score,
        "clarity": clarity,
        "accuracy": accuracy,
        "completeness": completeness,
        "confidence": confidence,
        "answers": answers,
        "scores": scores,
        "recommendations": recommendations.get('recommendations', []),
        "timestamp": datetime.now().isoformat()
    }
    
    html_report = report_generator.generate_html_report(report_data)
    
    report_dir = os.path.join(os.path.dirname(__file__), 'reports')
    os.makedirs(report_dir, exist_ok=True)
    
    filename = f"{session['candidate_name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    with open(os.path.join(report_dir, f"{filename}.json"), 'w') as f:
        json.dump(report_data, f, indent=2)
    
    with open(os.path.join(report_dir, f"{filename}.html"), 'w') as f:
        f.write(html_report)
    
    return jsonify({
        "success": True,
        "report": report_data,
        "html_report": html_report
    })

@app.route('/api/session/<session_id>/export/<format>', methods=['GET'])
def export_report(session_id, format):
    if session_id not in sessions:
        return jsonify({"error": "Session not found"}), 404
    
    session = sessions[session_id]
    scores = session["scores"]
    
    if format == 'json':
        return jsonify({"candidate": session["candidate_name"], "scores": scores})
    
    return jsonify({"error": "Invalid format"}), 400

if __name__ == '__main__':
    print("\n" + "🎯 "*20)
    print("INTERVIEW ENGINE STARTED")
    print("🎯 "*20 + "\n")
    app.run(debug=True, port=5000, host='0.0.0.0')