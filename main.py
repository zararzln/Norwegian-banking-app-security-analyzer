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
  # Display results if available
    if 'results' in st.session_state:
        st.markdown("---")
        st.header("📊 Analysis Results")
        
        results = st.session_state['results']
        
        # Summary Section
        if 'summary' in results:
            st.subheader("📈 Executive Summary")
            summary = results['summary']
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Apps", summary.get('total_apps', 0))
            with col2:
                st.metric("Protected Apps", summary.get('protected_apps', 0))
            with col3:
                st.metric("Avg Effectiveness", f"{summary.get('average_effectiveness', 0):.1f}%")
            with col4:
                st.metric("High Risk Apps", summary.get('high_risk_count', 0))
        
        st.markdown("---")
        
        # Protection Analysis
        if 'protection_analysis' in results:
            st.subheader("🛡️ Protection Solution Analysis")
            protection = results['protection_analysis']
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Most Common Solutions")
                if 'most_common' in protection:
                    for solution, count in protection['most_common']:
                        st.write(f"**{solution}:** {count} apps")
            
            with col2:
                st.markdown("#### Effectiveness by Solution")
                if 'effectiveness_by_solution' in protection:
                    for solution, eff in protection['effectiveness_by_solution'].items():
                        st.write(f"**{solution}:** {eff:.1f}%")
        
        st.markdown("---")
        
        # Individual App Results
        if 'apps' in results and results['apps']:
            st.subheader("📱 Individual App Analysis")
            
            for app in results['apps']:
                app_name = app.get('app_name', 'Unknown App')
                
                with st.expander(f"**{app_name}**", expanded=False):
                    # App Info
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        st.markdown("##### 📋 App Information")
                        st.write(f"**Package:** `{app.get('package_name', 'N/A')}`")
                        
                        if 'app_info' in app:
                            info = app['app_info']
                            st.write(f"**Version:** {info.get('version', 'N/A')}")
                            st.write(f"**Size:** {info.get('size', 'N/A')}")
                    
                    with col2:
                        st.markdown("##### 🛡️ Protection Details")
                        if 'protection' in app:
                            prot = app['protection']
                            
                            if prot.get('detected'):
                                st.success("✅ Protection Detected")
                                
                                if 'solutions' in prot and prot['solutions']:
                                    st.write("**Solutions Found:**")
                                    for solution in prot['solutions']:
                                        st.write(f"• {solution}")
                                
                                if 'confidence' in prot:
                                    st.write(f"**Confidence:** {prot['confidence']:.0f}%")
                            else:
                                st.error("❌ No Protection Detected")
                    
                    # Bypass Results
                    if 'bypass_results' in app:
                        st.markdown("##### ⚔️ Bypass Test Results")
                        bypass = app['bypass_results']
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Tests Run", bypass.get('total_tests', 0))
                        with col2:
                            st.metric("Successful", bypass.get('successful', 0))
                        with col3:
                            success_rate = bypass.get('success_rate', 0)
                            st.metric("Success Rate", f"{success_rate:.1f}%")
                        
                        if 'test_details' in bypass and bypass['test_details']:
                            st.markdown("**Test Details:**")
                            for test in bypass['test_details']:
                                status = "✅" if test.get('success') else "❌"
                                st.write(f"{status} {test.get('test_name', 'Unknown')}")
                    
                    # Effectiveness Score
                    if 'effectiveness_score' in app:
                        st.markdown("##### 📊 Effectiveness Score")
                        score = app['effectiveness_score']
                        
                        # Color based on score
                        if score >= 80:
                            st.success(f"**{score:.1f}%** - Highly Effective")
                        elif score >= 60:
                            st.warning(f"**{score:.1f}%** - Moderately Effective")
                        else:
                            st.error(f"**{score:.1f}%** - Low Effectiveness")
        
        st.markdown("---")
        
        # Recommendations
        if 'recommendations' in results:
            st.subheader("💡 Recommendations")
            recs = results['recommendations']
            
            if 'critical' in recs and recs['critical']:
                st.error("**🚨 Critical Issues:**")
                for rec in recs['critical']:
                    st.write(f"• {rec}")
            
            if 'important' in recs and recs['important']:
                st.warning("**⚠️ Important:**")
                for rec in recs['important']:
                    st.write(f"• {rec}")
            
            if 'suggestions' in recs and recs['suggestions']:
                st.info("**💭 Suggestions:**")
                for rec in recs['suggestions']:
                    st.write(f"• {rec}")
        
        st.markdown("---")
        
        # Download Section
        col1, col2 = st.columns(2)
        
        with col1:
            import json
            st.download_button(
                label="📥 Download Full Results (JSON)",
                data=json.dumps(results, indent=2),
                file_name="analysis_results.json",
                mime="application/json",
                use_container_width=True
            )
        
        with col2:
            with st.expander("🔍 View Raw Data"):
                st.json(results)
if __name__ == "__main__":
    main()
