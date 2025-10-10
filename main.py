#!/usr/bin/env python3
"""
Mobile App Shield Effectiveness Analyzer
Main execution file
"""

import sys
import os
from pathlib import Path
import logging

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from collectors.app_collector import AppCollector
from analysis.protection_detector import ProtectionDetector
from attacks.bypass_tester import BypassTester
from analysis.effectiveness_analyzer import EffectivenessAnalyzer
from src.reporting.dashboard import create_dashboard
from src.config.settings import BANKING_APPS, OUTPUT_DIR

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('shield_analyzer.log'),
            logging.StreamHandler()
        ]
    )

def main():
    """Main execution function"""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("🛡️  Starting Mobile App Shield Effectiveness Analyzer")
    logger.info("="*60)
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Initialize components
    logger.info("Initializing components...")
    collector = AppCollector()
    detector = ProtectionDetector()
    tester = BypassTester()
    analyzer = EffectivenessAnalyzer()
    
    results = []
    total_apps = len(BANKING_APPS)
    
    # Process each banking app
    for i, (app_name, package_name) in enumerate(BANKING_APPS.items(), 1):
        logger.info(f"[{i}/{total_apps}] Processing {app_name}...")
        
        try:
            # Step 1: Collect app info
            logger.info(f"  📱 Collecting app information...")
            app_info = collector.get_app_info(package_name)
            
            # Step 2: Detect protection
            logger.info(f"  🔍 Analyzing protection solutions...")
            protection_info = detector.analyze_protection(package_name)
            
            # Step 3: Run bypass tests
            logger.info(f"  ⚔️  Running bypass tests...")
            bypass_results = tester.run_tests(package_name)
            
            # Combine results
            app_result = {
                'app_name': app_name,
                'package_name': package_name,
                'app_info': app_info,
                'protection': protection_info,
                'bypass_results': bypass_results
            }
            
            results.append(app_result)
            logger.info(f"  ✅ Completed analysis for {app_name}")
            
        except Exception as e:
            logger.error(f"  ❌ Error processing {app_name}: {str(e)}")
            continue
        
        logger.info("-" * 50)
    
    # Analyze overall effectiveness
    logger.info("📊 Analyzing overall effectiveness...")
    analysis = analyzer.analyze_results(results)
    
    # Generate reports
    logger.info("📈 Generating dashboard...")
    create_dashboard(analysis)
    
    logger.info("="*60)
    logger.info("🎉 Analysis complete!")
    logger.info("📱 Dashboard available at: http://localhost:8501")
    logger.info("📄 Run 'streamlit run src/reporting/dashboard.py' to view results")

if __name__ == "__main__":
    main()
