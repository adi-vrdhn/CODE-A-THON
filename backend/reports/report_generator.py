import json
from typing import Dict, List, Any
from datetime import datetime
from pathlib import Path

class ReportGenerator:
    """Generates interview reports in multiple formats."""
    
    def __init__(self, output_dir: str = None):
        self.output_dir = output_dir or "./reports"
        Path(self.output_dir).mkdir(exist_ok=True)
    
    def generate_json_report(self, 
                            candidate_info: Dict[str, str],
                            results: List[Dict[str, Any]],
                            analysis: Dict[str, Any],
                            filename: str = None) -> str:
        """
        Generate JSON report.
        
        Returns:
            JSON string and saves to file
        """
        report = {
            "report_metadata": {
                "generated_at": datetime.now().isoformat(),
                "version": "1.0"
            },
            "candidate": candidate_info,
            "results": results,
            "analysis": analysis
        }
        
        if not filename:
            filename = f"{candidate_info.get('name', 'candidate').replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = Path(self.output_dir) / filename
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        return json.dumps(report, indent=2)
    
    def generate_html_report(self,
                            candidate_info: Dict[str, str],
                            results: List[Dict[str, Any]],
                            analysis: Dict[str, Any],
                            filename: str = None) -> str:
        """Generate HTML report."""
        html = self._build_html_report(candidate_info, results, analysis)
        
        if not filename:
            filename = f"{candidate_info.get('name', 'candidate').replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        
        filepath = Path(self.output_dir) / filename
        
        with open(filepath, 'w') as f:
            f.write(html)
        
        return html
    
    def generate_pdf_report(self,
                           candidate_info: Dict[str, str],
                           results: List[Dict[str, Any]],
                           analysis: Dict[str, Any],
                           filename: str = None) -> str:
        """Generate PDF report (requires weasyprint)."""
        try:
            from weasyprint import HTML, CSS
            from io import BytesIO
            
            html = self._build_html_report(candidate_info, results, analysis)
            
            if not filename:
                filename = f"{candidate_info.get('name', 'candidate').replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
            filepath = Path(self.output_dir) / filename
            
            HTML(string=html).write_pdf(str(filepath))
            
            return f"PDF report saved to {filepath}"
        
        except ImportError:
            return "PDF generation requires weasyprint. Install with: pip install weasyprint"
    
    def _build_html_report(self,
                          candidate_info: Dict[str, str],
                          results: List[Dict[str, Any]],
                          analysis: Dict[str, Any]) -> str:
        """Build HTML report content."""
        
        aggregate_scores = analysis.get('aggregate_scores', {})
        summary = analysis.get('summary', {})
        patterns = analysis.get('patterns', [])
        recommendations = analysis.get('recommendations', [])
        
        # Build score bars HTML
        score_bars = ""
        for dimension, score in aggregate_scores.items():
            if dimension != 'overall':
                bar_width = (score / 5) * 200
                score_bars += f"""
                <div class="score-item">
                    <label>{dimension.capitalize()}</label>
                    <div class="score-bar">
                        <div class="bar-fill" style="width: {bar_width}px;"></div>
                    </div>
                    <span>{score}/5</span>
                </div>
                """
        
        # Build results table
        results_table = ""
        for idx, result in enumerate(results, 1):
            result_score = result.get('overall', 0)
            results_table += f"""
            <tr>
                <td>{idx}</td>
                <td>{result.get('question_text', 'N/A')[:80]}...</td>
                <td>{result.get('scores', {}).get('clarity', 0)}/5</td>
                <td>{result.get('scores', {}).get('accuracy', 0)}/5</td>
                <td>{result.get('scores', {}).get('completeness', 0)}/5</td>
                <td>{result.get('scores', {}).get('confidence', 0)}/5</td>
                <td><strong>{result_score:.2f}/5</strong></td>
            </tr>
            """
        
        # Build patterns/recommendations
        patterns_html = ""
        for pattern in patterns:
            patterns_html += f"<li>{pattern}</li>"
        
        recommendations_html = ""
        for rec in recommendations:
            recommendations_html += f"<li>{rec}</li>"
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Interview Report - {candidate_info.get('name', 'Candidate')}</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 40px;
                    color: #333;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 1000px;
                    margin: 0 auto;
                    background: white;
                    padding: 30px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                h1, h2 {{
                    color: #2c3e50;
                    border-bottom: 3px solid #3498db;
                    padding-bottom: 10px;
                }}
                .header {{
                    display: flex;
                    justify-content: space-between;
                    margin-bottom: 30px;
                    border-bottom: 1px solid #ecf0f1;
                    padding-bottom: 20px;
                }}
                .candidate-info {{
                    flex: 1;
                }}
                .candidate-info p {{
                    margin: 5px 0;
                }}
                .overall-score {{
                    text-align: center;
                    font-size: 24px;
                    font-weight: bold;
                    color: #27ae60;
                }}
                .score-grid {{
                    display: grid;
                    grid-template-columns: repeat(4, 1fr);
                    gap: 15px;
                    margin: 20px 0;
                }}
                .score-card {{
                    background: #ecf0f1;
                    padding: 15px;
                    border-radius: 5px;
                    text-align: center;
                }}
                .score-card .value {{
                    font-size: 28px;
                    font-weight: bold;
                    color: #2980b9;
                }}
                .score-card .label {{
                    color: #7f8c8d;
                    margin-top: 5px;
                }}
                .score-item {{
                    margin: 15px 0;
                }}
                .score-item label {{
                    display: block;
                    margin-bottom: 5px;
                    font-weight: 500;
                }}
                .score-bar {{
                    height: 30px;
                    background: #ecf0f1;
                    border-radius: 5px;
                    overflow: hidden;
                    margin: 5px 0;
                }}
                .bar-fill {{
                    height: 100%;
                    background: linear-gradient(90deg, #3498db, #27ae60);
                    transition: width 0.3s;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }}
                table th {{
                    background: #34495e;
                    color: white;
                    padding: 12px;
                    text-align: left;
                    font-weight: 600;
                }}
                table td {{
                    padding: 12px;
                    border-bottom: 1px solid #ecf0f1;
                }}
                table tr:hover {{
                    background: #f8f9fa;
                }}
                .patterns, .recommendations {{
                    background: #f8f9fa;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 15px 0;
                }}
                .patterns ul, .recommendations ul {{
                    margin: 10px 0;
                    padding-left: 20px;
                }}
                .patterns li, .recommendations li {{
                    margin: 8px 0;
                }}
                .strength {{
                    color: #27ae60;
                    font-weight: 500;
                }}
                .improvement {{
                    color: #e74c3c;
                    font-weight: 500;
                }}
                .footer {{
                    text-align: center;
                    color: #7f8c8d;
                    margin-top: 40px;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Interview Assessment Report</h1>
                
                <div class="header">
                    <div class="candidate-info">
                        <h3>{candidate_info.get('name', 'N/A')}</h3>
                        <p><strong>Role:</strong> {candidate_info.get('role', 'N/A')}</p>
                        <p><strong>Experience:</strong> {candidate_info.get('experience_level', 'N/A')}</p>
                        <p><strong>Domain:</strong> {candidate_info.get('domain', 'N/A')}</p>
                    </div>
                    <div class="overall-score">
                        <div>{aggregate_scores.get('overall', 0):.2f}</div>
                        <div style="font-size: 16px; color: #7f8c8d;">Overall Score</div>
                    </div>
                </div>
                
                <h2>Summary</h2>
                <p><strong>Level:</strong> {summary.get('overall_level', 'N/A')}</p>
                <p>{summary.get('interpretation', 'N/A')}</p>
                
                <h2>Dimension Scores</h2>
                <div class="score-grid">
                    <div class="score-card">
                        <div class="value">{aggregate_scores.get('clarity', 0):.1f}</div>
                        <div class="label">Clarity</div>
                    </div>
                    <div class="score-card">
                        <div class="value">{aggregate_scores.get('accuracy', 0):.1f}</div>
                        <div class="label">Accuracy</div>
                    </div>
                    <div class="score-card">
                        <div class="value">{aggregate_scores.get('completeness', 0):.1f}</div>
                        <div class="label">Completeness</div>
                    </div>
                    <div class="score-card">
                        <div class="value">{aggregate_scores.get('confidence', 0):.1f}</div>
                        <div class="label">Confidence</div>
                    </div>
                </div>
                
                <h2>Question Results</h2>
                <table>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Question</th>
                            <th>Clarity</th>
                            <th>Accuracy</th>
                            <th>Completeness</th>
                            <th>Confidence</th>
                            <th>Overall</th>
                        </tr>
                    </thead>
                    <tbody>
                        {results_table}
                    </tbody>
                </table>
                
                <h2>Key Patterns</h2>
                <div class="patterns">
                    <ul>
                        {patterns_html}
                    </ul>
                </div>
                
                <h2>Recommendations</h2>
                <div class="recommendations">
                    <ul>
                        {recommendations_html}
                    </ul>
                </div>
                
                <div class="footer">
                    <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                    <p>Interview Automation Engine v1.0</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html
