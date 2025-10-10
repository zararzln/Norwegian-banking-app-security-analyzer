#!/usr/bin/env python3
"""
Mobile App Shield Effectiveness Analyzer - Interactive Dashboard
"""
import sys
import os
from pathlib import Path
import logging
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json

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
    analysis = analyzer.analyze_results(results)
    
    progress_bar.empty()
    status_text.empty()
    
    return analysis

def create_visualizations(results):
    """Create comprehensive visualizations"""
    
    # Hero Metrics
    st.markdown("### 📊 Overview Dashboard")
    
    # Extract data
    apps = results.get('apps', [])
    summary = results.get('summary', {})
    protection = results.get('protection_analysis', {})
    
    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_apps = len(apps) if apps else summary.get('total_apps', 0)
    protected_count = sum(1 for app in apps if app.get('protection', {}).get('detected')) if apps else summary.get('protected_apps', 0)
    avg_effectiveness = sum(app.get('effectiveness_score', 0) for app in apps) / len(apps) if apps else summary.get('average_effectiveness', 0)
    high_risk = sum(1 for app in apps if app.get('effectiveness_score', 0) < 60) if apps else summary.get('high_risk_count', 0)
    
    with col1:
        st.metric("Total Apps Analyzed", total_apps, delta=None)
    with col2:
        st.metric("Protected Apps", protected_count, delta=f"{(protected_count/total_apps*100) if total_apps else 0:.0f}%")
    with col3:
        st.metric("Avg Effectiveness", f"{avg_effectiveness:.1f}%", delta="Good" if avg_effectiveness >= 70 else "Low")
    with col4:
        st.metric("High Risk Apps", high_risk, delta="Critical" if high_risk > 0 else "Safe", delta_color="inverse")
    
    st.markdown("---")
    
    # Main visualizations
    if apps:
        # Create two columns for charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🛡️ Protection Coverage")
            
            # Protection pie chart
            protected = sum(1 for app in apps if app.get('protection', {}).get('detected'))
            unprotected = len(apps) - protected
            
            fig = go.Figure(data=[go.Pie(
                labels=['Protected', 'Unprotected'],
                values=[protected, unprotected],
                hole=.4,
                marker_colors=['#2ecc71', '#e74c3c']
            )])
            fig.update_layout(
                title_text="App Protection Status",
                showlegend=True,
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 📈 Effectiveness Distribution")
            
            # Effectiveness histogram
            effectiveness_scores = [app.get('effectiveness_score', 0) for app in apps]
            
            fig = go.Figure(data=[go.Histogram(
                x=effectiveness_scores,
                nbinsx=10,
                marker_color='#3498db',
                opacity=0.75
            )])
            fig.update_layout(
                title_text="Effectiveness Score Distribution",
                xaxis_title="Effectiveness (%)",
                yaxis_title="Number of Apps",
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # App comparison bar chart
        st.markdown("#### 📱 App Security Comparison")
        
        app_names = [app.get('app_name', 'Unknown') for app in apps]
        effectiveness = [app.get('effectiveness_score', 0) for app in apps]
        protection_status = ['Protected' if app.get('protection', {}).get('detected') else 'Unprotected' for app in apps]
        
        df = pd.DataFrame({
            'App': app_names,
            'Effectiveness': effectiveness,
            'Status': protection_status
        })
        
        fig = px.bar(df, x='App', y='Effectiveness', 
                    color='Status',
                    title='Security Effectiveness by App',
                    color_discrete_map={'Protected': '#2ecc71', 'Unprotected': '#e74c3c'},
                    height=400)
        fig.update_layout(xaxis_tickangle=-45)
        fig.update_traces(hovertemplate='<b>%{x}</b><br>Effectiveness: %{y:.1f}%<extra></extra>')
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Protection solutions analysis
        if protection and protection.get('most_common'):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🔒 Protection Solutions Used")
                
                solutions_data = protection['most_common']
                solutions_df = pd.DataFrame(solutions_data, columns=['Solution', 'Count'])
                
                fig = px.bar(solutions_df, x='Solution', y='Count',
                            title='Most Common Protection Solutions',
                            color='Count',
                            color_continuous_scale='Blues',
                            height=350)
                fig.update_traces(hovertemplate='<b>%{x}</b><br>Apps: %{y}<extra></extra>')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("#### ⚡ Solution Effectiveness")
                
                if protection.get('effectiveness_by_solution'):
                    eff_data = protection['effectiveness_by_solution']
                    eff_df = pd.DataFrame([
                        {'Solution': k, 'Effectiveness': v} 
                        for k, v in eff_data.items()
                    ])
                    
                    fig = px.bar(eff_df, x='Solution', y='Effectiveness',
                                title='Effectiveness by Protection Solution',
                                color='Effectiveness',
                                color_continuous_scale='RdYlGn',
                                range_y=[0, 100],
                                height=350)
                    fig.update_traces(hovertemplate='<b>%{x}</b><br>Effectiveness: %{y:.1f}%<extra></extra>')
                    st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Detailed app cards
        st.markdown("#### 🔍 Detailed App Analysis")
        
        # Create tabs for each app
        tabs = st.tabs([app.get('app_name', f'App {i}') for i, app in enumerate(apps)])
        
        for tab, app in zip(tabs, apps):
            with tab:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("##### 📋 Information")
                    st.write(f"**Package:** `{app.get('package_name', 'N/A')}`")
                    if 'app_info' in app:
                        info = app['app_info']
                        st.write(f"**Version:** {info.get('version', 'N/A')}")
                        st.write(f"**Size:** {info.get('size', 'N/A')}")
                
                with col2:
                    st.markdown("##### 🛡️ Protection")
                    if app.get('protection', {}).get('detected'):
                        st.success("✅ Protected")
                        prot = app['protection']
                        if prot.get('solutions'):
                            st.write("**Solutions:**")
                            for sol in prot['solutions']:
                                st.write(f"• {sol}")
                        if 'confidence' in prot:
                            st.progress(prot['confidence'] / 100)
                            st.caption(f"Confidence: {prot['confidence']:.0f}%")
                    else:
                        st.error("❌ No Protection")
                
                with col3:
                    st.markdown("##### 📊 Score")
                    score = app.get('effectiveness_score', 0)
                    
                    # Gauge chart for score
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = score,
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "Effectiveness"},
                        gauge = {
                            'axis': {'range': [None, 100]},
                            'bar': {'color': "darkblue"},
                            'steps': [
                                {'range': [0, 60], 'color': "lightcoral"},
                                {'range': [60, 80], 'color': "lightyellow"},
                                {'range': [80, 100], 'color': "lightgreen"}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': 70
                            }
                        }
                    ))
                    fig.update_layout(height=200, margin=dict(l=10, r=10, t=30, b=10))
                    st.plotly_chart(fig, use_container_width=True)
                
                # Bypass tests
                if 'bypass_results' in app:
                    st.markdown("##### ⚔️ Bypass Test Results")
                    bypass = app['bypass_results']
                    
                    subcol1, subcol2, subcol3 = st.columns(3)
                    with subcol1:
                        st.metric("Tests Run", bypass.get('total_tests', 0))
                    with subcol2:
                        st.metric("Bypassed", bypass.get('successful', 0))
                    with subcol3:
                        st.metric("Success Rate", f"{bypass.get('success_rate', 0):.1f}%")
                    
                    if 'test_details' in bypass and bypass['test_details']:
                        test_data = []
                        for test in bypass['test_details']:
                            test_data.append({
                                'Test': test.get('test_name', 'Unknown'),
                                'Result': 'Bypassed' if test.get('success') else 'Blocked',
                                'Value': 1 if test.get('success') else 0
                            })
                        
                        if test_data:
                            test_df = pd.DataFrame(test_data)
                            fig = px.bar(test_df, x='Test', y='Value',
                                        color='Result',
                                        title='Individual Test Results',
                                        color_discrete_map={'Bypassed': '#e74c3c', 'Blocked': '#2ecc71'},
                                        height=300)
                            fig.update_layout(yaxis_title='', showlegend=True, xaxis_tickangle=-45)
                            fig.update_yaxis(showticklabels=False)
                            st.plotly_chart(fig, use_container_width=True)
    
    # Recommendations
    # Recommendations
    st.markdown("---")
    if 'recommendations' in results:
        st.markdown("#### 💡 Security Recommendations")
        recs = results['recommendations']
        
        # Check if recs is a list or dict
        if isinstance(recs, list):
            # If it's a list, just display all items
            for i, rec in enumerate(recs, 1):
                st.info(f"**{i}.** {rec}")
        elif isinstance(recs, dict):
            # If it's a dict, use tabs
            tab1, tab2, tab3 = st.tabs(["🚨 Critical", "⚠️ Important", "💭 Suggestions"])
            
            with tab1:
                if recs.get('critical'):
                    for i, rec in enumerate(recs['critical'], 1):
                        st.error(f"**{i}.** {rec}")
                else:
                    st.success("✅ No critical issues found!")
            
            with tab2:
                if recs.get('important'):
                    for i, rec in enumerate(recs['important'], 1):
                        st.warning(f"**{i}.** {rec}")
                else:
                    st.info("✅ No important issues found!")
            
            with tab3:
                if recs.get('suggestions'):
                    for i, rec in enumerate(recs['suggestions'], 1):
                        st.info(f"**{i}.** {rec}")
                else:
                    st.success("✅ Following all best practices!")

def main():
    """Main Streamlit app"""
    setup_logging()
    
    st.set_page_config(
        page_title="Shield Analyzer",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .main > div {
            padding-top: 2rem;
        }
        .stMetric {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.title("🛡️ Norwegian Banking App Security Analyzer")
    st.markdown("**Comprehensive analysis of mobile app protection solutions and their effectiveness**")
    
    # Try to load existing results
    results_file = Path(OUTPUT_DIR) / "analysis_results.json"
    
    if 'results' not in st.session_state and results_file.exists():
        try:
            with open(results_file, 'r') as f:
                st.session_state['results'] = json.load(f)
        except Exception as e:
            pass
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Control Panel")
        st.markdown("---")
        
        st.info(f"📱 **Total Apps:** {len(BANKING_APPS)}")
        
        if st.button("🔄 Run New Analysis", type="primary", use_container_width=True):
            st.session_state['run_analysis'] = True
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        This dashboard analyzes:
        - 🔍 Protection detection
        - ⚔️ Bypass vulnerability
        - 📊 Effectiveness scoring
        - 💡 Security recommendations
        """)
    
    # Run analysis if requested
    if st.session_state.get('run_analysis', False):
        with st.spinner("🔄 Running comprehensive security analysis..."):
            results = run_analysis()
            st.session_state['results'] = results
            st.session_state['run_analysis'] = False
        st.success("✅ Analysis complete!")
        st.balloons()
    
    # Display results
    if 'results' in st.session_state:
        st.markdown("---")
        create_visualizations(st.session_state['results'])
        
        # Debug expander at bottom
        with st.expander("🔧 Debug: Raw Data"):
            st.json(st.session_state['results'])
    else:
        # Welcome screen
        st.info("👈 **Click 'Run New Analysis' in the sidebar to begin**")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("### 🔍 Detection")
            st.markdown("Identifies protection solutions used in banking apps")
        with col2:
            st.markdown("### ⚔️ Testing")
            st.markdown("Tests bypass techniques against protections")
        with col3:
            st.markdown("### 📊 Analysis")
            st.markdown("Scores effectiveness and provides recommendations")

if __name__ == "__main__":
    main()
