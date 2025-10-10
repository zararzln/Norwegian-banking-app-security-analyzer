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
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    collector = AppCollector()
    detector = ProtectionDetector()
    tester = BypassTester()
    analyzer = EffectivenessAnalyzer()
    
    results = []
    total_apps = len(BANKING_APPS)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, (app_name, package_name) in enumerate(BANKING_APPS.items(), 1):
        status_text.text(f"[{i}/{total_apps}] Processing {app_name}...")
        
        try:
            app_info = collector.get_app_info(package_name)
            protection_info = detector.analyze_protection(package_name)
            bypass_results = tester.run_tests(package_name)
            
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
        
        progress_bar.progress(i / total_apps)
    
    status_text.text("Analyzing overall effectiveness...")
    
    # DEBUG: Show what we have before analysis
    st.write("DEBUG - Raw results before analysis:", results)
    
    analysis = analyzer.analyze_results(results)
    
    # DEBUG: Show what analyzer returns
    st.write("DEBUG - Analysis output:", analysis)
    
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
    
    # Try to load existing results
    import json
    results_file = Path(OUTPUT_DIR) / "analysis_results.json"
    
    if 'results' not in st.session_state and results_file.exists():
        try:
            with open(results_file, 'r') as f:
                st.session_state['results'] = json.load(f)
            st.success("✅ Loaded existing analysis results")
        except Exception as e:
            st.error(f"Error loading results: {e}")
    
    # Sidebar
    with st.sidebar:
        st.header("Analysis Settings")
        st.info(f"📱 Total Apps: {len(BANKING_APPS)}")
        
        if st.button("🔄 Re-run Analysis", type="primary"):
            st.session_state['run_analysis'] = True
    
    # Run analysis if button clicked
    if st.session_state.get('run_analysis', False):
        with st.spinner("Running comprehensive analysis..."):
            results = run_analysis()
            st.session_state['results'] = results
            st.session_state['run_analysis'] = False
        st.success("✅ Analysis complete!")
    
    # Display results if available
    if 'results' in st.session_state:
        # [KEEP ALL YOUR VISUALIZATION CODE HERE - don't change anything below]
        st.markdown("---")
        st.header("📊 Analysis Results")
        
        results = st.session_state['results']
        
        # Import visualization libraries
        import plotly.express as px
        import plotly.graph_objects as go
        import pandas as pd
        
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
                if 'most_common' in protection and protection['most_common']:
                    df = pd.DataFrame(protection['most_common'], columns=['Solution', 'Count'])
                    fig = px.bar(df, x='Solution', y='Count', 
                                title='Protection Solutions Distribution',
                                color='Count',
                                color_continuous_scale='Blues')
                    st.plotly_chart(fig, use_container_width=True)
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.info("No data available")
            
            with col2:
                st.markdown("#### Effectiveness by Solution")
                if 'effectiveness_by_solution' in protection and protection['effectiveness_by_solution']:
                    df = pd.DataFrame([
                        {'Solution': k, 'Effectiveness': v} 
                        for k, v in protection['effectiveness_by_solution'].items()
                    ])
                    fig = px.bar(df, x='Solution', y='Effectiveness',
                                title='Effectiveness Scores by Solution',
                                color='Effectiveness',
                                color_continuous_scale='RdYlGn',
                                range_y=[0, 100])
                    st.plotly_chart(fig, use_container_width=True)
                    
                    df['Effectiveness'] = df['Effectiveness'].apply(lambda x: f"{x:.1f}%")
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.info("No data available")
        
        st.markdown("---")
        
        # Individual Apps
        if 'apps' in results and results['apps']:
            st.subheader("📱 Individual App Analysis")
            
            # Comparison chart
            app_data = []
            for app in results['apps']:
                app_data.append({
                    'App': app.get('app_name', 'Unknown'),
                    'Effectiveness': app.get('effectiveness_score', 0),
                    'Protected': 'Yes' if app.get('protection', {}).get('detected') else 'No'
                })
            
            if app_data:
                df = pd.DataFrame(app_data)
                fig = px.bar(df, x='App', y='Effectiveness', 
                            color='Protected',
                            title='Security Effectiveness Comparison',
                            color_discrete_map={'Yes': 'green', 'No': 'red'})
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
            
            # Detailed cards
            for app in results['apps']:
                app_name = app.get('app_name', 'Unknown App')
                
                with st.expander(f"**{app_name}**"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("##### 📋 App Information")
                        st.write(f"**Package:** `{app.get('package_name', 'N/A')}`")
                        
                        if 'app_info' in app:
                            info = app['app_info']
                            st.write(f"**Version:** {info.get('version', 'N/A')}")
                            st.write(f"**Size:** {info.get('size', 'N/A')}")
                        
                        st.markdown("##### 🛡️ Protection")
                        if 'protection' in app and app['protection'].get('detected'):
                            st.success("✅ Protection Detected")
                            prot = app['protection']
                            if 'solutions' in prot and prot['solutions']:
                                for solution in prot['solutions']:
                                    st.write(f"• {solution}")
                            if 'confidence' in prot:
                                st.progress(prot['confidence'] / 100)
                                st.caption(f"Confidence: {prot['confidence']:.0f}%")
                        else:
                            st.error("❌ No Protection Detected")
                    
                    with col2:
                        st.markdown("##### ⚔️ Bypass Tests")
                        if 'bypass_results' in app:
                            bypass = app['bypass_results']
                            
                            subcol1, subcol2, subcol3 = st.columns(3)
                            with subcol1:
                                st.metric("Tests", bypass.get('total_tests', 0))
                            with subcol2:
                                st.metric("Bypassed", bypass.get('successful', 0))
                            with subcol3:
                                st.metric("Rate", f"{bypass.get('success_rate', 0):.1f}%")
                            
                            if 'test_details' in bypass and bypass['test_details']:
                                st.write("**Test Results:**")
                                for test in bypass['test_details']:
                                    status = "✅" if test.get('success') else "❌"
                                    st.write(f"{status} {test.get('test_name', 'Unknown')}")
                        
                        st.markdown("##### 📊 Effectiveness")
                        if 'effectiveness_score' in app:
                            score = app['effectiveness_score']
                            st.progress(score / 100)
                            
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
        
        # Debug view
        with st.expander("🔍 View Raw Data (Debug)"):
            st.json(results)

if __name__ == "__main__":
    main()
