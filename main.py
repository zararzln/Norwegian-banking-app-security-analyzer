import streamlit as st
import sys
from pathlib import Path
import importlib


SRC_PATH = Path(__file__).resolve().parent / "src"
sys.path.insert(0, str(SRC_PATH))


import config.settings
importlib.reload(config.settings)
from config.settings import BANKING_APPS, OUTPUT_DIR

from collectors.app_collector import AppCollector
from analysis.protection_detector import ProtectionDetector
from attacks.bypass_tester import BypassTester
from analysis.effectiveness_analyzer import EffectivenessAnalyzer
from reporting.dashboard import create_dashboard


def run_analysis():

    st.write("BANKING_APPS:", BANKING_APPS)
    st.write("Type of BANKING_APPS:", type(BANKING_APPS))

    """Run the complete analysis"""
    collector = AppCollector()
    detector = ProtectionDetector()
    tester = BypassTester()
    
    results = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for idx, app in enumerate(BANKING_APPS):
        status_text.text(f"Processing {app['name']}...")
        # Your analysis logic
        progress_bar.progress((idx + 1) / len(BANKING_APPS))
    
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
