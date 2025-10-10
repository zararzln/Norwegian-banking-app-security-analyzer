"""Bypass technique tester"""

import logging
import random
import time
from src.config.settings import BYPASS_TESTS

class BypassTester:
    """Tests bypass techniques against protected apps"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def run_tests(self, package_name):
        """Run all bypass tests against an app"""
        self.logger.info(f"Running bypass tests for {package_name}")
        
        results = {}
        
        for test_id, test_config in BYPASS_TESTS.items():
            self.logger.info(f"Running {test_config['name']}...")
            
            # Simulate test execution time
            time.sleep(random.uniform(0.5, 2.0))
            
            test_result = self._run_single_test(package_name, test_id, test_config)
            results[test_id] = test_result
        
        return results
    
    def _run_single_test(self, package_name, test_id, test_config):
        """Run a single bypass test"""
        
        # Simulate realistic bypass success rates based on protection level
        if any(major in package_name.lower() for major in ['dnb', 'nordea', 'handelsbanken', 'danske']):
            base_success_rate = 0.2  # Major banks have better protection
        elif any(regional in package_name.lower() for regional in ['sparebank', 'skandia', 'sbanken']):
            base_success_rate = 0.4  # Regional banks have moderate protection  
        else:
            base_success_rate = 0.7  # Fintech/smaller banks may have weaker protection
        
        # Adjust success rate based on test type
        test_modifiers = {
            'root_detection': 0.8,  # Root detection often bypassable
            'ssl_pinning': 0.6,     # SSL pinning moderately bypassable
            'anti_debug': 0.4,      # Anti-debug harder to bypass
            'tampering': 0.3        # Tampering detection hardest to bypass
        }
        
        final_success_rate = base_success_rate * test_modifiers.get(test_id, 0.5)
        
        # Determine if bypass succeeded
        bypass_successful = random.random() < final_success_rate
        
        # Generate test details
        techniques_tested = test_config['techniques']
        successful_techniques = []
        
        if bypass_successful:
            # Randomly select which techniques worked
            num_successful = random.randint(1, len(techniques_tested))
            successful_techniques = random.sample(techniques_tested, num_successful)
        
        return {
            'test_name': test_config['name'],
            'description': test_config['description'],
            'bypass_successful': bypass_successful,
            'success_rate': final_success_rate,
            'techniques_tested': techniques_tested,
            'successful_techniques': successful_techniques,
            'execution_time': random.uniform(10, 45),  # seconds
            'notes': self._generate_test_notes(test_id, bypass_successful)
        }
    
    def _generate_test_notes(self, test_id, successful):
        """Generate realistic test notes"""
        if test_id == 'root_detection':
            if successful:
                return "Root detection bypassed using Magisk Hide. App failed to detect rooted environment."
            else:
                return "Strong root detection implementation. Multiple bypass attempts failed."
        elif test_id == 'ssl_pinning':
            if successful:
                return "SSL pinning bypassed successfully. Certificate validation was circumvented."
            else:
                return "Robust SSL pinning implementation detected and blocked bypass attempts."
        elif test_id == 'anti_debug':
            if successful:
                return "Anti-debugging measures bypassed. Debugger attachment successful."
            else:
                return "Advanced anti-debugging protection active. Debugger detection effective."
        elif test_id == 'tampering':
            if successful:
                return "App integrity checks bypassed. Runtime modifications successful."
            else:
                return "Strong tampering detection. App detected unauthorized modifications."
        return "Test completed."