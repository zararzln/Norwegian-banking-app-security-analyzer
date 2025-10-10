import streamlit as st
import sys
from pathlib import Path
import importlib.util

# Force load the correct config/settings.py
ROOT_DIR = Path(__file__).resolve().parent
SETTINGS_PATH = ROOT_DIR / "src" / "config" / "settings.py"

spec = importlib.util.spec_from_file_location("settings", SETTINGS_PATH)
settings = importlib.util.module_from_spec(spec)
spec.loader.exec_module(settings)

BANKING_APPS = settings.BANKING_APPS
OUTPUT_DIR = settings.OUTPUT_DIR

# Import the rest AFTER
from collectors.app_collector import AppCollector
from analysis.protection_detector import ProtectionDetector
from attacks.bypass_tester import BypassTester
from analysis.effectiveness_analyzer import EffectivenessAnalyzer
from reporting.dashboard import create_dashboard



def run_analysis():
    """Run the complete analysis"""
    collector = AppCollector()
    detector = ProtectionDetector()
    tester = BypassTester()
    analyzer = EffectivenessAnalyzer()
    
    results = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for idx, app_package in enumerate(BANKING_APPS):
        # Handle string package names
        status_text.text(f"Processing {app_package}...")
        
        try:
            # Collect app info
            app_info = collector.collect_app_info(app_package)
            
            # Detect protections
            protections = detector.detect_protection(app_package)
            
            # Run bypass tests
            bypass_results = tester.run_bypass_tests(app_package)
            
            # Analyze effectiveness
            effectiveness = analyzer.analyze(app_package, protections, bypass_results)
            
            results.append({
                'package': app_package,
                'info': app_info,
                'protections': protections,
                'bypass_results': bypass_results,
                'effectiveness': effectiveness
            })
            
        except Exception as e:
            st.error(f"Error processing {app_package}: {str(e)}")
        
        progress_bar.progress((idx + 1) / len(BANKING_APPS))
    
    status_text.text("Analysis complete!")
    return results

def main():
    st.set_page_config(
        page_title="Mobile App Shield Analyzer",
        page_icon="🛡️",
        layout="wide"
    )
    
    st.title("🛡️ Mobile App Shield Effectiveness Analyzer")
    st.markdown("### Analyze mobile banking app security protections")
    
    # Sidebar controls
    with st.sidebar:
        st.header("Controls")
        if st.button("▶️ Start Analysis", type="primary"):
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
        create_dashboard(st.session_state['results'])
    else:
        st.info("👈 Click 'Start Analysis' in the sidebar to begin")
        
        # Show preview/description
        st.markdown("""
        This tool analyzes mobile banking applications for:
        - 🔍 Protection solution detection
        - 🛡️ Shield effectiveness evaluation
        - ⚠️ Vulnerability assessment
        - 📊 Comprehensive reporting
        """)

if __name__ == "__main__":
    main()
