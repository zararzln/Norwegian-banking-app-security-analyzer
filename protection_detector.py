"""Protection solution detector"""

import logging
import random

class ProtectionDetector:
    """Detects protection solutions used in mobile apps"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def analyze_protection(self, package_name):
        """Analyze what protection solutions an app uses"""
        self.logger.info(f"Analyzing protection for {package_name}")
        
        protection_info = self._simulate_protection_analysis(package_name)
        return protection_info
    
    def _simulate_protection_analysis(self, package_name):
        """Simulate protection analysis for demo purposes"""
        
        protection_patterns = {
            'major_bank': {
                'solutions': ['Promon SHIELD', 'Root Detection', 'SSL Pinning', 'Anti Debug'],
                'probability': 0.8
            },
            'regional_bank': {
                'solutions': ['Root Detection', 'SSL Pinning'],
                'probability': 0.6
            },
            'fintech': {
                'solutions': ['Root Detection'],
                'probability': 0.4
            }
        }
        
        if any(major in package_name.lower() for major in ['dnb', 'nordea', 'handelsbanken', 'danske']):
            bank_type = 'major_bank'
        elif any(regional in package_name.lower() for regional in ['sparebank', 'skandia', 'sbanken']):
            bank_type = 'regional_bank'
        else:
            bank_type = 'fintech'
        
        pattern = protection_patterns[bank_type]
        detected_solutions = []
        confidence_scores = {}
        protection_features = []
        
        for solution in pattern['solutions']:
            if random.random() < pattern['probability']:
                detected_solutions.append(solution)
                confidence_scores[solution] = random.uniform(0.7, 0.95)
                
                if solution == 'Root Detection':
                    protection_features.extend(['SafetyNet', 'RootBeer checks'])
                elif solution == 'SSL Pinning':
                    protection_features.extend(['Certificate pinning', 'TrustManager override'])
                elif solution == 'Anti Debug':
                    protection_features.extend(['Debugger detection', 'Frida detection'])
                elif solution == 'Promon SHIELD':
                    protection_features.extend(['Runtime protection', 'Advanced obfuscation'])
        
        obfuscation_levels = ['None', 'Basic', 'Moderate', 'Advanced']
        obfuscation_level = random.choice(obfuscation_levels)
        
        return {
            'detected_solutions': detected_solutions,
            'confidence_scores': confidence_scores,
            'protection_features': protection_features,
            'obfuscation_level': obfuscation_level,
            'analysis_notes': f"Analyzed {package_name} - {bank_type} category"
        }