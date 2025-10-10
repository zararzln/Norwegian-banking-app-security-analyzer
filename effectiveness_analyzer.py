"""Effectiveness analysis and reporting"""

import logging
import pandas as pd
from datetime import datetime
import json

class EffectivenessAnalyzer:
    """Analyzes overall protection effectiveness across apps"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def analyze_results(self, results):
        """Analyze all test results and generate insights"""
        self.logger.info("Analyzing effectiveness across all tested apps")
        
        if not results:
            self.logger.warning("No results to analyze")
            return {}
        
        analysis = {
            'summary': self._generate_summary(results),
            'protection_analysis': self._analyze_protection_solutions(results),
            'bypass_analysis': self._analyze_bypass_effectiveness(results),
            'bank_categories': self._analyze_by_bank_type(results),
            'recommendations': self._generate_recommendations(results),
            'raw_data': results,
            'generated_at': datetime.now().isoformat()
        }
        
        # Save analysis to file
        self._save_analysis(analysis)
        
        return analysis
    
    def _generate_summary(self, results):
        """Generate high-level summary statistics"""
        total_apps = len(results)
        
        # Count protection solutions
        protection_counts = {}
        bypass_success_rates = []
        
        for result in results:
            # Count protection solutions
            for solution in result['protection']['detected_solutions']:
                protection_counts[solution] = protection_counts.get(solution, 0) + 1
            
            # Calculate bypass success rate for this app
            bypass_results = result['bypass_results']
            app_successes = sum(1 for test in bypass_results.values() if test['bypass_successful'])
            app_success_rate = app_successes / len(bypass_results) if bypass_results else 0
            bypass_success_rates.append(app_success_rate)
        
        avg_bypass_success = sum(bypass_success_rates) / len(bypass_success_rates) if bypass_success_rates else 0
        
        return {
            'total_apps_tested': total_apps,
            'avg_bypass_success_rate': avg_bypass_success,
            'most_common_protection': max(protection_counts, key=protection_counts.get) if protection_counts else "None",
            'protection_adoption_rate': len([r for r in results if r['protection']['detected_solutions']]) / total_apps,
            'apps_with_strong_protection': len([r for r in results if len(r['protection']['detected_solutions']) >= 3]),
            'completely_unprotected_apps': len([r for r in results if not r['protection']['detected_solutions']])
        }
    
    def _analyze_protection_solutions(self, results):
        """Analyze effectiveness of different protection solutions"""
        solution_stats = {}
        
        for result in results:
            solutions = result['protection']['detected_solutions']
            bypass_results = result['bypass_results']
            
            # Calculate success rate for this app
            app_successes = sum(1 for test in bypass_results.values() if test['bypass_successful'])
            app_success_rate = app_successes / len(bypass_results) if bypass_results else 0
            
            for solution in solutions:
                if solution not in solution_stats:
                    solution_stats[solution] = {
                        'apps_using': 0,
                        'total_bypass_attempts': 0,
                        'successful_bypasses': 0,
                        'avg_effectiveness': 0
                    }
                
                solution_stats[solution]['apps_using'] += 1
                solution_stats[solution]['total_bypass_attempts'] += len(bypass_results)
                solution_stats[solution]['successful_bypasses'] += app_successes
        
        # Calculate effectiveness scores
        for solution, stats in solution_stats.items():
            if stats['total_bypass_attempts'] > 0:
                stats['avg_effectiveness'] = 1 - (stats['successful_bypasses'] / stats['total_bypass_attempts'])
            else:
                stats['avg_effectiveness'] = 0
        
        return solution_stats
    
    def _analyze_bypass_effectiveness(self, results):
        """Analyze which bypass techniques are most successful"""
        bypass_stats = {}
        
        for result in results:
            for test_id, test_result in result['bypass_results'].items():
                if test_id not in bypass_stats:
                    bypass_stats[test_id] = {
                        'total_attempts': 0,
                        'successful_attempts': 0,
                        'success_rate': 0,
                        'avg_execution_time': 0,
                        'most_successful_technique': None
                    }
                
                bypass_stats[test_id]['total_attempts'] += 1
                if test_result['bypass_successful']:
                    bypass_stats[test_id]['successful_attempts'] += 1
        
        # Calculate success rates
        for test_id, stats in bypass_stats.items():
            if stats['total_attempts'] > 0:
                stats['success_rate'] = stats['successful_attempts'] / stats['total_attempts']
        
        return bypass_stats
    
    def _analyze_by_bank_type(self, results):
        """Analyze protection effectiveness by bank category"""
        categories = {
            'major_banks': [],
            'regional_banks': [],
            'fintech': []
        }
        
        for result in results:
            package_name = result['package_name'].lower()
            
            if any(major in package_name for major in ['dnb', 'nordea', 'handelsbanken', 'danske']):
                category = 'major_banks'
            elif any(regional in package_name for regional in ['sparebank', 'skandia', 'sbanken']):
                category = 'regional_banks'
            else:
                category = 'fintech'
            
            # Calculate bypass success rate for this app
            bypass_results = result['bypass_results']
            app_successes = sum(1 for test in bypass_results.values() if test['bypass_successful'])
            app_success_rate = app_successes / len(bypass_results) if bypass_results else 0
            
            categories[category].append({
                'app_name': result['app_name'],
                'protection_count': len(result['protection']['detected_solutions']),
                'bypass_success_rate': app_success_rate,
                'protections': result['protection']['detected_solutions']
            })
        
        # Calculate category averages
        category_analysis = {}
        for category, apps in categories.items():
            if apps:
                avg_protection_count = sum(app['protection_count'] for app in apps) / len(apps)
                avg_bypass_success = sum(app['bypass_success_rate'] for app in apps) / len(apps)
                
                category_analysis[category] = {
                    'app_count': len(apps),
                    'avg_protection_count': avg_protection_count,
                    'avg_bypass_success_rate': avg_bypass_success,
                    'effectiveness_score': 1 - avg_bypass_success,
                    'apps': apps
                }
        
        return category_analysis
    
    def _generate_recommendations(self, results):
        """Generate actionable recommendations"""
        recommendations = []
        
        # Analyze common vulnerabilities
        unprotected_apps = [r for r in results if not r['protection']['detected_solutions']]
        if unprotected_apps:
            recommendations.append({
                'priority': 'High',
                'category': 'Unprotected Apps',
                'recommendation': f"{len(unprotected_apps)} apps have no detectable protection. Immediate security assessment needed.",
                'affected_apps': [app['app_name'] for app in unprotected_apps]
            })
        
        # Analyze bypass success rates
        high_bypass_apps = []
        for result in results:
            bypass_results = result['bypass_results']
            app_successes = sum(1 for test in bypass_results.values() if test['bypass_successful'])
            app_success_rate = app_successes / len(bypass_results) if bypass_results else 0
            
            if app_success_rate > 0.7:  # More than 70% bypass success
                high_bypass_apps.append(result['app_name'])
        
        if high_bypass_apps:
            recommendations.append({
                'priority': 'High',
                'category': 'Vulnerable Protection',
                'recommendation': f"{len(high_bypass_apps)} apps are highly vulnerable to bypass attacks. Consider upgrading protection.",
                'affected_apps': high_bypass_apps
            })
        
        # Analyze missing common protections
        apps_without_root_detection = [r for r in results if 'Root Detection' not in r['protection']['detected_solutions']]
        if len(apps_without_root_detection) > len(results) * 0.3:  # More than 30% missing root detection
            recommendations.append({
                'priority': 'Medium',
                'category': 'Missing Root Detection',
                'recommendation': f"{len(apps_without_root_detection)} apps lack root detection. This is a basic security requirement for banking apps.",
                'affected_apps': [app['app_name'] for app in apps_without_root_detection]
            })
        
        return recommendations
    
    def _save_analysis(self, analysis):
        """Save analysis results to JSON file"""
        try:
            import os
            os.makedirs('output', exist_ok=True)
            
            with open('output/analysis_results.json', 'w') as f:
                json.dump(analysis, f, indent=2, default=str)
                
            self.logger.info("Analysis results saved to output/analysis_results.json")
        except Exception as e:
            self.logger.error(f"Failed to save analysis: {str(e)}")