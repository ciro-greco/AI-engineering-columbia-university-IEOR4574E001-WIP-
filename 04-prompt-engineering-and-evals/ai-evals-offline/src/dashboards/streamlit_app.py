#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interactive Streamlit Dashboard for AI Evaluation Analysis
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import pathlib
import statistics
from collections import Counter, defaultdict
from datetime import datetime
import numpy as np

# Page configuration
st.set_page_config(
    page_title="AI Evaluation Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_jsonl(filepath):
    """Load JSONL file into a list of dictionaries."""
    try:
        with open(filepath, 'r') as f:
            return [json.loads(line) for line in f if line.strip()]
    except FileNotFoundError:
        st.error(f"File not found: {filepath}")
        return []
    except json.JSONDecodeError as e:
        st.error(f"JSON decode error: {e}")
        return []

@st.cache_data
def load_evaluation_data():
    """Load all evaluation data files."""
    data = {
        'results': load_jsonl('results.jsonl'),
        'traces': load_jsonl('runs.jsonl'),
        'examples': load_jsonl('data/examples.jsonl')
    }
    return data

def main():
    # Header
    st.title("🚀 AI Evaluation Dashboard")
    st.markdown("**Interactive analysis of model evaluation results and performance metrics**")
    
    # Sidebar
    st.sidebar.title("📋 Dashboard Controls")
    
    # Load data
    with st.spinner("Loading evaluation data..."):
        data = load_evaluation_data()
    
    # Data overview in sidebar
    st.sidebar.markdown("### 📊 Data Overview")
    st.sidebar.metric("Results", len(data['results']))
    st.sidebar.metric("Traces", len(data['traces']))
    st.sidebar.metric("Examples", len(data['examples']))
    
    # Main dashboard tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Results Summary", 
        "⚡ Performance Analysis", 
        "🔍 Chain Comparison", 
        "📝 Output Examples", 
        "💡 Insights & Recommendations"
    ])
    
    # Tab 1: Results Summary
    with tab1:
        st.header("📈 Evaluation Results Summary")
        
        if data['results']:
            results_df = pd.DataFrame(data['results'])
            
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)
            
            n = len(results_df)
            schema_rate = results_df['schema'].mean() if 'schema' in results_df.columns else 0
            short_rate = results_df['short'].mean() if 'short' in results_df.columns else 0
            faith_mean = results_df['faith'].mean() if 'faith' in results_df.columns else 0
            
            with col1:
                st.metric("Dataset Size", n)
            with col2:
                st.metric("Schema Compliance", f"{schema_rate:.1%}")
            with col3:
                st.metric("Length Compliance", f"{short_rate:.1%}")
            with col4:
                st.metric("Avg Faithfulness", f"{faith_mean:.3f}")
            
            # Visualizations
            if 'faith' in results_df.columns and len(results_df) > 1:
                st.subheader("Faithfulness Score Distribution")
                
                # Histogram
                fig_hist = px.histogram(
                    results_df, 
                    x='faith', 
                    nbins=10,
                    title="Distribution of Faithfulness Scores",
                    labels={'faith': 'Faithfulness Score', 'count': 'Frequency'}
                )
                st.plotly_chart(fig_hist, use_container_width=True)
                
                # Box plot
                fig_box = px.box(
                    results_df, 
                    y='faith',
                    title="Faithfulness Score Box Plot"
                )
                st.plotly_chart(fig_box, use_container_width=True)
            
            # Detailed results table
            st.subheader("Detailed Results")
            st.dataframe(results_df, use_container_width=True)
            
        else:
            st.warning("No results data found. Run dataset_eval.py first.")
    
    # Tab 2: Performance Analysis
    with tab2:
        st.header("⚡ Performance Analysis")
        
        if data['traces']:
            traces_df = pd.DataFrame(data['traces'])
            
            # Performance metrics
            col1, col2, col3 = st.columns(3)
            
            total_calls = len(traces_df)
            avg_latency = traces_df['latency_ms'].mean() if 'latency_ms' in traces_df.columns else 0
            success_rate = sum(1 for t in data['traces'] if t.get('output')) / total_calls if total_calls > 0 else 0
            
            with col1:
                st.metric("Total Calls", total_calls)
            with col2:
                st.metric("Avg Latency", f"{avg_latency:.0f}ms")
            with col3:
                st.metric("Success Rate", f"{success_rate:.1%}")
            
            # Latency analysis
            if 'latency_ms' in traces_df.columns:
                st.subheader("Latency Analysis")
                
                # Latency histogram
                fig_latency = px.histogram(
                    traces_df,
                    x='latency_ms',
                    nbins=20,
                    title="Latency Distribution",
                    labels={'latency_ms': 'Latency (ms)', 'count': 'Frequency'}
                )
                st.plotly_chart(fig_latency, use_container_width=True)
                
                # Latency over time
                if 'ts' in traces_df.columns:
                    traces_df['datetime'] = pd.to_datetime(traces_df['ts'], unit='s')
                    fig_timeline = px.scatter(
                        traces_df,
                        x='datetime',
                        y='latency_ms',
                        color='name' if 'name' in traces_df.columns else None,
                        title="Latency Over Time",
                        labels={'datetime': 'Time', 'latency_ms': 'Latency (ms)'}
                    )
                    st.plotly_chart(fig_timeline, use_container_width=True)
            
            # Performance statistics
            st.subheader("Performance Statistics")
            if 'latency_ms' in traces_df.columns:
                perf_stats = traces_df['latency_ms'].describe()
                stats_df = pd.DataFrame({
                    'Metric': ['Count', 'Mean', 'Std', 'Min', '25%', '50%', '75%', 'Max'],
                    'Value (ms)': [
                        f"{perf_stats['count']:.0f}",
                        f"{perf_stats['mean']:.0f}",
                        f"{perf_stats['std']:.0f}",
                        f"{perf_stats['min']:.0f}",
                        f"{perf_stats['25%']:.0f}",
                        f"{perf_stats['50%']:.0f}",
                        f"{perf_stats['75%']:.0f}",
                        f"{perf_stats['max']:.0f}"
                    ]
                })
                st.dataframe(stats_df, use_container_width=True)
                
        else:
            st.warning("No trace data found. Run some evaluations first.")
    
    # Tab 3: Chain Comparison
    with tab3:
        st.header("🔍 Chain Comparison")
        
        if data['traces']:
            traces_df = pd.DataFrame(data['traces'])
            
            if 'name' in traces_df.columns:
                # Chain performance metrics
                chain_stats = []
                for chain in traces_df['name'].unique():
                    chain_data = traces_df[traces_df['name'] == chain]
                    stats = {
                        'Chain': chain,
                        'Calls': len(chain_data),
                        'Avg Latency (ms)': chain_data['latency_ms'].mean(),
                        'Min Latency (ms)': chain_data['latency_ms'].min(),
                        'Max Latency (ms)': chain_data['latency_ms'].max(),
                        'Success Rate': sum(1 for _, row in chain_data.iterrows() if row.get('output')) / len(chain_data)
                    }
                    chain_stats.append(stats)
                
                comparison_df = pd.DataFrame(chain_stats)
                
                # Performance comparison table
                st.subheader("Performance Comparison Table")
                st.dataframe(comparison_df, use_container_width=True)
                
                # Latency comparison chart
                st.subheader("Latency Comparison")
                fig_comparison = px.bar(
                    comparison_df,
                    x='Chain',
                    y='Avg Latency (ms)',
                    title="Average Latency by Chain",
                    color='Chain'
                )
                st.plotly_chart(fig_comparison, use_container_width=True)
                
                # Chain usage pie chart
                st.subheader("Chain Usage Distribution")
                usage_counts = traces_df['name'].value_counts()
                fig_pie = px.pie(
                    values=usage_counts.values,
                    names=usage_counts.index,
                    title="Chain Usage Distribution"
                )
                st.plotly_chart(fig_pie, use_container_width=True)
                
                # Side-by-side latency distributions
                st.subheader("Latency Distribution by Chain")
                fig_violin = px.violin(
                    traces_df,
                    x='name',
                    y='latency_ms',
                    title="Latency Distribution by Chain",
                    labels={'name': 'Chain', 'latency_ms': 'Latency (ms)'}
                )
                st.plotly_chart(fig_violin, use_container_width=True)
                
                # Winner analysis
                if len(comparison_df) >= 2:
                    fastest_chain = comparison_df.loc[comparison_df['Avg Latency (ms)'].idxmin()]
                    st.success(f"🏆 **Performance Winner**: {fastest_chain['Chain']} with {fastest_chain['Avg Latency (ms)']:.0f}ms average latency")
                    
            else:
                st.warning("No chain name data available for comparison.")
        else:
            st.warning("No trace data found for chain comparison.")
    
    # Tab 4: Output Examples
    with tab4:
        st.header("📝 Output Examples")
        
        if data['traces']:
            # Controls
            col1, col2 = st.columns(2)
            with col1:
                num_examples = st.slider("Number of examples to show", 1, 10, 3)
            with col2:
                if 'name' in pd.DataFrame(data['traces']).columns:
                    chain_filter = st.selectbox(
                        "Filter by chain", 
                        ['All'] + list(pd.DataFrame(data['traces'])['name'].unique())
                    )
                else:
                    chain_filter = 'All'
            
            # Filter traces
            filtered_traces = data['traces']
            if chain_filter != 'All':
                filtered_traces = [t for t in data['traces'] if t.get('name') == chain_filter]
            
            # Display examples
            for i, trace in enumerate(filtered_traces[:num_examples], 1):
                with st.expander(f"Example {i}: {trace.get('name', 'unknown')} ({trace.get('latency_ms', 0)}ms)"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Input:**")
                        input_text = trace.get('inputs', {}).get('text', 'No input')
                        st.text_area("", input_text, height=100, key=f"input_{i}")
                    
                    with col2:
                        st.markdown("**Output:**")
                        output = trace.get('output', 'No output')
                        st.text_area("", output, height=100, key=f"output_{i}")
                    
                    # Metadata
                    st.markdown("**Metadata:**")
                    metadata = {
                        'Chain': trace.get('name', 'unknown'),
                        'Latency': f"{trace.get('latency_ms', 0)}ms",
                        'Timestamp': datetime.fromtimestamp(trace.get('ts', 0)).strftime('%Y-%m-%d %H:%M:%S') if trace.get('ts') else 'Unknown'
                    }
                    st.json(metadata)
        else:
            st.warning("No trace data found for examples.")
    
    # Tab 5: Insights & Recommendations
    with tab5:
        st.header("💡 Insights & Recommendations")
        
        # Generate insights based on data
        insights = []
        recommendations = []
        
        if data['results']:
            results_df = pd.DataFrame(data['results'])
            
            # Schema compliance analysis
            if 'schema' in results_df.columns:
                schema_rate = results_df['schema'].mean()
                if schema_rate < 0.9:
                    insights.append("🔍 **Schema Compliance Issue**: Less than 90% of outputs follow the expected JSON format")
                    recommendations.append("📝 Improve prompt clarity and add format validation examples")
                elif schema_rate == 1.0:
                    insights.append("✅ **Excellent Schema Compliance**: 100% of outputs follow the expected format")
            
            # Faithfulness analysis
            if 'faith' in results_df.columns:
                faith_mean = results_df['faith'].mean()
                if faith_mean < 0.5:
                    insights.append("⚠️ **Low Faithfulness**: Model outputs may not align well with reference content")
                    recommendations.append("🎯 Review and improve prompt instructions for better content alignment")
                elif faith_mean > 0.8:
                    insights.append("🎯 **High Faithfulness**: Strong alignment with reference content")
        
        if data['traces']:
            traces_df = pd.DataFrame(data['traces'])
            
            # Performance analysis
            if 'latency_ms' in traces_df.columns:
                avg_latency = traces_df['latency_ms'].mean()
                if avg_latency > 2000:
                    insights.append(f"⏱️ **High Latency**: Average response time is {avg_latency:.0f}ms")
                    recommendations.append("⚡ Consider model optimization or using a faster model variant")
                elif avg_latency < 1000:
                    insights.append(f"🚀 **Good Performance**: Fast response times averaging {avg_latency:.0f}ms")
            
            # Chain comparison
            if 'name' in traces_df.columns and len(traces_df['name'].unique()) >= 2:
                chain_latencies = traces_df.groupby('name')['latency_ms'].mean()
                fastest = chain_latencies.idxmin()
                slowest = chain_latencies.idxmax()
                speed_diff = ((chain_latencies[slowest] - chain_latencies[fastest]) / chain_latencies[slowest]) * 100
                
                insights.append(f"🏆 **Performance Leader**: {fastest} is {speed_diff:.0f}% faster than {slowest}")
                recommendations.append(f"🎯 Consider deploying {fastest} for production use")
        
        # Display insights
        if insights:
            st.subheader("🔍 Key Insights")
            for insight in insights:
                st.markdown(insight)
        else:
            st.info("No specific insights available. Run more evaluations to generate insights.")
        
        # Display recommendations
        if recommendations:
            st.subheader("🎯 Recommendations")
            for i, rec in enumerate(recommendations, 1):
                st.markdown(f"{i}. {rec}")
        else:
            st.info("No specific recommendations available yet.")
        
        # Next steps
        st.subheader("📋 Next Steps")
        next_steps = [
            "🔄 Run evaluations on a larger dataset for more robust statistics",
            "🧪 Experiment with different prompt variations",
            "👥 Consider adding human evaluation for quality assessment",
            "📊 Set up automated monitoring for production deployment",
            "🎯 Define success criteria and SLA targets"
        ]
        
        for step in next_steps:
            st.markdown(f"- {step}")
        
        # Export functionality
        st.subheader("📤 Export Analysis")
        if st.button("Generate Summary Report"):
            report = {
                'timestamp': datetime.now().isoformat(),
                'data_summary': {
                    'results_count': len(data['results']),
                    'traces_count': len(data['traces']),
                    'examples_count': len(data['examples'])
                },
                'insights': insights,
                'recommendations': recommendations
            }
            
            st.download_button(
                label="Download Report (JSON)",
                data=json.dumps(report, indent=2),
                file_name=f"evaluation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

if __name__ == "__main__":
    main()