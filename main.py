#!/usr/bin/env python3
"""
Mobile App Shield Effectiveness Analyzer
Streamlit Dashboard
"""
import sys
import os
from pathlib import Path
import logging
import streamlit as st

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from collectors.app_collector import AppCollector
from analysis.protection_detector import ProtectionDetector
from attacks.bypass_tester import BypassTester
from analysis.effectiveness_analyzer import EffectivenessAnalyzer
from reporting.dashboard import create_dashboard
from config.settings import BANKING_APPS, OUTPUT_DIR

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def run_analysis():
    """Run the analysis and return results"""
    logger = logging.getLogger(__name__)
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Initialize components
    collector = AppCollector()
    detector = ProtectionDetector()
    tester = BypassTester()
    analyzer = EffectivenessAnalyzer()
    
    results = []
    total_apps = len(BANKING_APPS)
    
    # Create progress indicators
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Process each banking app
    for i, (app_name, package_name) in enumerate(BANKING_APPS.items(), 1):
        status_text.text(f"[{i}/{total_apps}] Processing {app_name}...")
        
        try:
            # Collect app info
            app_info = collector.get_app_info(package_name)
            
            # Detect protection
            protection_info = detector.analyze_protection(package_name)
            
            # Run bypass tests
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
            
        except Exception as e:
            st.warning(f"Error processing {app_name}: {str(e)}")
            continue
        
        # Update progress
        progress_bar.progress(i / total_apps)
    
    status_text.text("Analyzing overall effectiveness...")
    
    # Analyze overall effectiveness
    analysis = analyzer.analyze_results(results)
    
    progress_bar.empty()
    status_text.empty()
    
    return analysis

def main():
    """Main Streamlit app"""
    setup_logging()
    
    st.set_page_config(
        page_title="Shield Effectiveness Analyzer",
        page_icon="🛡️",
        layout="wide"
    )
    
    st.title("🛡️ Mobile Banking App Shield Effectiveness Analyzer")
    st.markdown("Analyzing security protection solutions across Norwegian banking apps")
    
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("Analysis Settings")
        st.info(f"📱 Total Apps: {len(BANKING_APPS)}")
        
        if st.button("🚀 Run Analysis", type="primary"):
            st.session_state['run_analysis'] = True
    
    # Main content
    if st.session_state.get('run_analysis', False):
        with st.spinner("Running comprehensive analysis..."):
            results = run_analysis()
            st.session_state['results'] = results
            st.session_state['run_analysis'] = False
        st.success("✅ Analysis complete!")
    
    # Display results if available
    if 'results' in st.session_state:
        st.markdown("---")
        st.header("📊 Analysis Results")
        
        # Call the dashboard creation function with results
        create_dashboard(st.session_state['results'])
    else:
        # Show instructions
        st.info("👈 Click 'Run Analysis' in the sidebar to start analyzing banking apps")
        
        st.markdown("### What this analyzer does:")
        st.markdown("""
        - 📱 Collects information from Norwegian banking apps
        - 🔍 Detects protection solutions (ProGuard, DexGuard, AppShield, etc.)
        - ⚔️ Tests bypass techniques
        - 📊 Analyzes overall effectiveness
        - 📈 Generates comprehensive visualizations
        """)

if __name__ == "__main__":
    main()
