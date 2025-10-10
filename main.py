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
        
        # Protection Analysis with Charts
        if 'protection_analysis' in results:
            st.subheader("🛡️ Protection Solution Analysis")
            protection = results['protection_analysis']
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Most Common Solutions")
                if 'most_common' in protection and protection['most_common']:
                    import plotly.express as px
                    import pandas as pd
                    
                    # Create dataframe for chart
                    df = pd.DataFrame(protection['most_common'], columns=['Solution', 'Count'])
                    
                    # Create bar chart
                    fig = px.bar(df, x='Solution', y='Count', 
                                color='Count',
                                color_continuous_scale='Blues',
                                title='Protection Solutions Usage')
                    fig.update_layout(showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Also show as table
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.info("No protection solution data available")
            
            with col2:
                st.markdown("#### Effectiveness by Solution")
                if 'effectiveness_by_solution' in protection and protection['effectiveness_by_solution']:
                    import plotly.express as px
                    import pandas as pd
                    
                    # Create dataframe
                    df = pd.DataFrame([
                        {'Solution': k, 'Effectiveness': v} 
                        for k, v in protection['effectiveness_by_solution'].items()
                    ])
                    
                    # Create bar chart
                    fig = px.bar(df, x='Solution', y='Effectiveness',
                                color='Effectiveness',
                                color_continuous_scale='RdYlGn',
                                title='Effectiveness Scores',
                                range_y=[0, 100])
                    fig.update_layout(showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Also show as table
                    df['Effectiveness'] = df['Effectiveness'].apply(lambda x: f"{x:.1f}%")
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.info("No effectiveness data available")
            
            # Additional protection insights
            if 'coverage_percentage' in protection:
                st.markdown("#### Protection Coverage")
                coverage = protection['coverage_percentage']
                
                import plotly.graph_objects as go
                
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = coverage,
                    title = {'text': "Apps with Protection"},
                    delta = {'reference': 100},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 50], 'color': "lightgray"},
                            {'range': [50, 75], 'color': "gray"},
                            {'range': [75, 100], 'color': "lightblue"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ))
                
                st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Individual App Results
        if 'apps' in results and results['apps']:
            st.subheader("📱 Individual App Analysis")
            
            # Create comparison chart
            import plotly.express as px
            import pandas as pd
            
            app_data = []
            for app in results['apps']:
                app_data.append({
                    'App': app.get('app_name', 'Unknown'),
                    'Effectiveness': app.get('effectiveness_score', 0),
                    'Protected': 'Yes' if app.get('protection', {}).get('detected') else 'No'
                })
            
            if app_data:
                df = pd.DataFrame(app_data)
                
                # Effectiveness comparison chart
                fig = px.bar(df, x='App', y='Effectiveness', 
                            color='Protected',
                            title='App Security Effectiveness Comparison',
                            color_discrete_map={'Yes': 'green', 'No': 'red'})
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
            
            # Detailed app cards
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
                                    st.progress(prot['confidence'] / 100)
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
                        
                        # Visualize test results
                        if 'test_details' in bypass and bypass['test_details']:
                            test_df = pd.DataFrame(bypass['test_details'])
                            if not test_df.empty and 'test_name' in test_df.columns and 'success' in test_df.columns:
                                test_df['Status'] = test_df['success'].apply(lambda x: 'Passed' if x else 'Failed')
                                
                                fig = px.bar(test_df, x='test_name', y='success',
                                            color='Status',
                                            title='Individual Test Results',
                                            color_discrete_map={'Passed': 'red', 'Failed': 'green'})
                                fig.update_layout(xaxis_title='Test Name', yaxis_title='Success (1=Bypassed)')
                                st.plotly_chart(fig, use_container_width=True)
                    
                    # Effectiveness Score
                    if 'effectiveness_score' in app:
                        st.markdown("##### 📊 Effectiveness Score")
                        score = app['effectiveness_score']
                        
                        # Progress bar with color
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            if score >= 80:
                                st.success(f"Highly Effective")
                            elif score >= 60:
                                st.warning(f"Moderately Effective")
                            else:
                                st.error(f"Low Effectiveness")
                        with col2:
                            st.metric("Score", f"{score:.1f}%")
                        
                        st.progress(score / 100)
        
        st.markdown("---")
        
        # Recommendations
        if 'recommendations' in results:
            st.subheader("💡 Recommendations")
            recs = results['recommendations']
            
            tab1, tab2, tab3 = st.tabs(["🚨 Critical", "⚠️ Important", "💭 Suggestions"])
            
            with tab1:
                if 'critical' in recs and recs['critical']:
                    for i, rec in enumerate(recs['critical'], 1):
                        st.error(f"**{i}.** {rec}")
                else:
                    st.success("No critical issues found!")
            
            with tab2:
                if 'important' in recs and recs['important']:
                    for i, rec in enumerate(recs['important'], 1):
                        st.warning(f"**{i}.** {rec}")
                else:
                    st.info("No important issues found!")
            
            with tab3:
                if 'suggestions' in recs and recs['suggestions']:
                    for i, rec in enumerate(recs['suggestions'], 1):
                        st.info(f"**{i}.** {rec}")
                else:
                    st.success("All best practices are being followed!")
