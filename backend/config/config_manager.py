import json
import os
from typing import Dict, Any, List

class ConfigManager:
    """Manages interview configuration and settings."""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or os.path.join(
            os.path.dirname(__file__), 'defaults.json'
        )
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
    
    def get_roles(self) -> List[str]:
        """Get list of available roles."""
        return self.config.get('roles', [])
    
    def get_experience_levels(self) -> List[str]:
        """Get list of experience levels."""
        return self.config.get('experience_levels', [])
    
    def get_domains(self) -> List[str]:
        """Get list of interview domains."""
        return self.config.get('domains', [])
    
    def get_difficulty_levels(self) -> List[str]:
        """Get list of difficulty levels."""
        return self.config.get('difficulty_levels', [])
    
    def get_rubric(self) -> Dict[str, Dict[str, str]]:
        """Get scoring rubric."""
        return self.config.get('scoring_rubric', {})
    
    def get_interview_settings(self) -> Dict[str, Any]:
        """Get interview settings."""
        return self.config.get('interview_settings', {})
    
    def validate_role(self, role: str) -> bool:
        """Validate if role exists."""
        return role in self.get_roles()
    
    def validate_experience_level(self, level: str) -> bool:
        """Validate if experience level exists."""
        return level in self.get_experience_levels()
