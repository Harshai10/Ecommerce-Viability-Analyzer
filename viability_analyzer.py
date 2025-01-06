import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

class CampaignViabilityAnalyzer:
    def __init__(self):
        self.metrics = {
            'customer_reach': 0,
            'conversion_rate': 0,
            'average_order_value': 0,
            'marketing_cost': 0,
            'operational_cost': 0
        }
    
    def set_metrics(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.metrics:
                self.metrics[key] = value
    
    def calculate_roi(self):
        potential_customers = self.metrics['customer_reach']
        conversions = potential_customers * (self.metrics['conversion_rate'] / 100)
        revenue = conversions * self.metrics['average_order_value']
        total_cost = self.metrics['marketing_cost'] + self.metrics['operational_cost']
        
        roi = ((revenue - total_cost) / total_cost) * 100 if total_cost > 0 else 0
        return {
            'potential_customers': potential_customers,
            'conversions': conversions,
            'revenue': revenue,
            'total_cost': total_cost,
            'roi': roi
        }

def main():
    st.title("TACOS Campaign Viability Analyzer")
    
    analyzer = CampaignViabilityAnalyzer()
    
    st.sidebar.header("Campaign Metrics")
    
    # Input metrics
    customer_reach = st.sidebar.number_input("Potential Customer Reach", min_value=0, value=1000)
    conversion_rate = st.sidebar.slider("Conversion Rate (%)", 0.0, 100.0, 2.0)
    avg_order_value = st.sidebar.number_input("Average Order Value ($)", min_value=0.0, value=50.0)
    marketing_cost = st.sidebar.number_input("Marketing Cost ($)", min_value=0.0, value=1000.0)
    operational_cost = st.sidebar.number_input("Operational Cost ($)", min_value=0.0, value=500.0)
    
    analyzer.set_metrics(
        customer_reach=customer_reach,
        conversion_rate=conversion_rate,
        average_order_value=avg_order_value,
        marketing_cost=marketing_cost,
        operational_cost=operational_cost
    )
    
    results = analyzer.calculate_roi()
    
    # Display results
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Expected Conversions", f"{results['conversions']:.0f}")
    with col2:
        st.metric("Total Revenue", f"${results['revenue']:,.2f}")
    with col3:
        st.metric("ROI", f"{results['roi']:.1f}%")
    
    # Visualization
    st.subheader("Cost Breakdown")
    costs_df = pd.DataFrame({
        'Category': ['Marketing', 'Operational'],
        'Cost': [marketing_cost, operational_cost]
    })
    fig = px.pie(costs_df, values='Cost', names='Category', title='Cost Distribution')
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()