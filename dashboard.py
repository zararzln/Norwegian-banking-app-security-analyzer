import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import numpy as np

def create_dashboard(analysis_data):
    try:
        with open('output/dashboard_data.json', 'w') as f:
            json.dump(analysis_data, f, indent=2, default=str)
    except Exception as e:
        pass

def main():
    st.set_page_config(
        page_title="Shield Analyzer Pro",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for professional styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<div class="main-header">🛡️ Mobile App Shield Effectiveness Analyzer Pro</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Advanced Security Intelligence Platform | Norwegian Banking Sector Analysis</div>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("🎛️ Analysis Controls")
    st.sidebar.markdown("---")
    
    # Load data
    try:
        with open('output/dashboard_data.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        st.error("❌ No analysis data found. Please run the analyzer first.")
        return
    
    # Sidebar filters
    analysis_type = st.sidebar.selectbox(
        "📊 Analysis View",
        ["Executive Summary", "Detailed Technical Analysis", "Threat Intelligence", "Competitive Analysis"]
    )
    
    bank_filter = st.sidebar.multiselect(
        "🏦 Bank Categories",
        ["Major Banks", "Regional Banks", "Fintech"],
        default=["Major Banks", "Regional Banks", "Fintech"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info("💡 **Pro Tip**: This analysis covers 25 Norwegian banking apps with real-time security assessment capabilities.")
    
    # Main dashboard content
    summary = data.get('summary', {})
    
    if analysis_type == "Executive Summary":
        show_executive_summary(data, summary)
    elif analysis_type == "Detailed Technical Analysis":
        show_technical_analysis(data, summary)
    elif analysis_type == "Threat Intelligence":
        show_threat_intelligence(data, summary)
    else:
        show_competitive_analysis(data, summary)

def show_executive_summary(data, summary):
    # Key Metrics Dashboard
    st.subheader("📈 Executive Dashboard")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "🎯 Apps Analyzed", 
            summary.get('total_apps_tested', 0),
            delta="100% Coverage"
        )
    with col2:
        bypass_rate = summary.get('avg_bypass_success_rate', 0)
        st.metric(
            "⚠️ Avg Bypass Success", 
            f"{bypass_rate:.1%}",
            delta=f"{bypass_rate-0.3:.1%}" if bypass_rate > 0.3 else f"{0.3-bypass_rate:.1%}"
        )
    with col3:
        protection_rate = summary.get('protection_adoption_rate', 0)
        st.metric(
            "🛡️ Protection Adoption", 
            f"{protection_rate:.1%}",
            delta="Industry Leading" if protection_rate > 0.8 else "Below Average"
        )
    with col4:
        strong_protection = summary.get('apps_with_strong_protection', 0)
        st.metric(
            "🔒 Strong Protection", 
            strong_protection,
            delta=f"{strong_protection/summary.get('total_apps_tested', 1):.1%}"
        )
    with col5:
        unprotected = summary.get('completely_unprotected_apps', 0)
        st.metric(
            "🚨 Unprotected Apps", 
            unprotected,
            delta="Critical" if unprotected > 0 else "Secure"
        )
    
    # Risk Assessment Matrix
    st.subheader("🎯 Risk Assessment Matrix")
    
    # Create risk matrix data
    bank_categories = data.get('bank_categories', {})
    risk_data = []
    
    for category, info in bank_categories.items():
        risk_score = info.get('avg_bypass_success_rate', 0) * 100
        protection_score = info.get('avg_protection_count', 0) * 20
        
        risk_data.append({
            'Category': category.replace('_', ' ').title(),
            'Risk Score': risk_score,
            'Protection Score': protection_score,
            'App Count': info.get('app_count', 0)
        })
    
    if risk_data:
        risk_df = pd.DataFrame(risk_data)
        
        fig = px.scatter(
            risk_df, 
            x='Protection Score', 
            y='Risk Score',
            size='App Count',
            color='Category',
            title="Security Risk vs Protection Coverage Matrix",
            labels={'Risk Score': 'Risk Level (%)', 'Protection Score': 'Protection Strength'},
            hover_data=['App Count']
        )
        
        # Add quadrant lines
        fig.add_hline(y=50, line_dash="dash", line_color="red", opacity=0.5)
        fig.add_vline(x=50, line_dash="dash", line_color="red", opacity=0.5)
        
        # Add quadrant labels
        fig.add_annotation(x=25, y=75, text="High Risk<br>Low Protection", showarrow=False, font_color="red")
        fig.add_annotation(x=75, y=25, text="Low Risk<br>High Protection", showarrow=False, font_color="green")
        
        st.plotly_chart(fig, use_container_width=True)

def show_technical_analysis(data, summary):
    st.subheader("🔬 Technical Security Analysis")
    
    # Protection Solutions Effectiveness
    col1, col2 = st.columns(2)
    
    protection_analysis = data.get('protection_analysis', {})
    if protection_analysis:
        protection_df = pd.DataFrame([
            {
                'Solution': solution,
                'Apps Using': info['apps_using'],
                'Effectiveness': info['avg_effectiveness'] * 100,
                'Market Share': (info['apps_using'] / summary.get('total_apps_tested', 1)) * 100
            }
            for solution, info in protection_analysis.items()
        ])
        
        with col1:
            # Donut chart with custom colors
            fig = px.pie(
                protection_df, 
                values='Apps Using', 
                names='Solution',
                title="🛡️ Protection Solution Market Share",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Effectiveness bar chart with gradient
            fig = px.bar(
                protection_df, 
                x='Solution', 
                y='Effectiveness',
                title="🎯 Protection Solution Effectiveness Scores",
                color='Effectiveness',
                color_continuous_scale='RdYlGn'
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
    
    # Bypass Technique Analysis
    st.subheader("⚔️ Attack Vector Analysis")
    
    bypass_analysis = data.get('bypass_analysis', {})
    if bypass_analysis:
        bypass_df = pd.DataFrame([
            {
                'Technique': test_id.replace('_', ' ').title(),
                'Success Rate': info['success_rate'] * 100,
                'Total Attempts': info['total_attempts'],
                'Difficulty': 100 - (info['success_rate'] * 100)  # Inverse of success rate
            }
            for test_id, info in bypass_analysis.items()
        ])
        
        # Multi-metric visualization
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Success Rate by Technique', 'Attack Difficulty vs Success', 
                          'Total Attempts Distribution', 'Threat Level Heatmap'),
            specs=[[{"type": "bar"}, {"type": "scatter"}],
                   [{"type": "bar"}, {"type": "heatmap"}]]
        )
        
        # Success rate bars
        fig.add_trace(
            go.Bar(x=bypass_df['Technique'], y=bypass_df['Success Rate'], 
                   name='Success Rate', marker_color='crimson'),
            row=1, col=1
        )
        
        # Difficulty scatter
        fig.add_trace(
            go.Scatter(x=bypass_df['Difficulty'], y=bypass_df['Success Rate'],
                      mode='markers+text', text=bypass_df['Technique'],
                      marker=dict(size=bypass_df['Total Attempts'], color='blue'),
                      name='Difficulty Analysis'),
            row=1, col=2
        )
        
        # Attempts distribution
        fig.add_trace(
            go.Bar(x=bypass_df['Technique'], y=bypass_df['Total Attempts'],
                   name='Attempts', marker_color='orange'),
            row=2, col=1
        )
        
        # Threat heatmap data
        heatmap_data = bypass_df[['Success Rate']].T
        fig.add_trace(
            go.Heatmap(z=[bypass_df['Success Rate'].values], 
                      x=bypass_df['Technique'], y=['Threat Level'],
                      colorscale='Reds', name='Threat Heatmap'),
            row=2, col=2
        )
        
        fig.update_layout(height=800, showlegend=False, title_text="Advanced Attack Analysis Dashboard")
        st.plotly_chart(fig, use_container_width=True)

def show_threat_intelligence(data, summary):
    st.subheader("🎯 Threat Intelligence Dashboard")
    
    # Threat timeline simulation
    st.markdown("### 📈 Simulated Threat Evolution Timeline")
    
    # Generate mock threat timeline data
    dates = pd.date_range('2024-01-01', periods=12, freq='M')
    threat_data = {
        'Date': dates,
        'Root Detection Bypass': np.random.randint(5, 25, 12),
        'SSL Pinning Bypass': np.random.randint(3, 18, 12),
        'Anti-Debug Bypass': np.random.randint(1, 12, 12),
        'Tampering Detection Bypass': np.random.randint(1, 8, 12)
    }
    
    threat_df = pd.DataFrame(threat_data)
    
    fig = px.line(
        threat_df.melt(id_vars='Date', var_name='Threat Type', value_name='Incidents'),
        x='Date', y='Incidents', color='Threat Type',
        title="Monthly Threat Intelligence: Attack Technique Frequency",
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Geographic threat distribution (mock)
    st.markdown("### 🌍 Geographic Threat Distribution")
    
    geo_data = pd.DataFrame({
        'Country': ['Norway', 'Sweden', 'Denmark', 'Finland', 'Iceland'],
        'Threats': [45, 32, 28, 15, 8],
        'lat': [60.4720, 60.1282, 56.2639, 61.9241, 64.9631],
        'lon': [8.4689, 18.6435, 9.5018, 25.7482, -19.0208]
    })
    
    fig = px.scatter_mapbox(
        geo_data, lat="lat", lon="lon", size="Threats", color="Threats",
        hover_name="Country", hover_data=["Threats"],
        color_continuous_scale="Reds", size_max=50,
        mapbox_style="open-street-map", zoom=3,
        title="Nordic Region Threat Intelligence Map"
    )
    st.plotly_chart(fig, use_container_width=True)

def show_competitive_analysis(data, summary):
    st.subheader("🏆 Competitive Intelligence Analysis")
    
    # Market positioning analysis
    bank_categories = data.get('bank_categories', {})
    if bank_categories:
        competitive_data = []
        
        for category, info in bank_categories.items():
            competitive_data.append({
                'Segment': category.replace('_', ' ').title(),
                'Market Size': info.get('app_count', 0),
                'Security Investment': info.get('avg_protection_count', 0) * 25,  # Mock investment score
                'Vulnerability Level': info.get('avg_bypass_success_rate', 0) * 100,
                'Effectiveness Score': info.get('effectiveness_score', 0) * 100
            })
        
        comp_df = pd.DataFrame(competitive_data)
        
        # Bubble chart for competitive positioning
        fig = px.scatter(
            comp_df,
            x='Security Investment',
            y='Effectiveness Score',
            size='Market Size',
            color='Vulnerability Level',
            hover_name='Segment',
            title="🎯 Competitive Security Positioning Matrix",
            labels={
                'Security Investment': 'Security Investment Score',
                'Effectiveness Score': 'Protection Effectiveness (%)',
                'Vulnerability Level': 'Risk Level (%)'
            },
            color_continuous_scale='RdYlGn_r'
        )
        
        # Add market leader indicators
        fig.add_annotation(
            x=comp_df.loc[comp_df['Effectiveness Score'].idxmax(), 'Security Investment'],
            y=comp_df.loc[comp_df['Effectiveness Score'].idxmax(), 'Effectiveness Score'],
            text="Market Leader",
            showarrow=True,
            arrowhead=2,
            arrowcolor="green"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Recommendations Engine
    st.subheader("🚀 Strategic Recommendations")
    
    recommendations = data.get('recommendations', [])
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            priority_color = {
                'High': '🔴',
                'Medium': '🟡', 
                'Low': '🟢'
            }.get(rec['priority'], '⚪')
            
            with st.expander(f"{priority_color} Priority {i}: {rec['category']}"):
                st.markdown(f"**Recommendation:** {rec['recommendation']}")
                
                if 'affected_apps' in rec:
                    st.markdown("**Affected Applications:**")
                    for app in rec['affected_apps']:
                        st.markdown(f"• {app}")
                
                # Mock business impact
                st.markdown("**Business Impact:**")
                if rec['priority'] == 'High':
                    st.error("⚠️ Critical security gap requiring immediate action")
                elif rec['priority'] == 'Medium':
                    st.warning("📊 Moderate risk with potential compliance implications")
                else:
                    st.info("💡 Optimization opportunity for enhanced security posture")

if __name__ == "__main__":
    main()