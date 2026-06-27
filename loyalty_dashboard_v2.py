import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Airline Retention Command Center", layout="wide", initial_sidebar_state="expanded")

st.title("✈️ Airline Loyalty Intelligence Command Center")
st.markdown("**Executive Retention Dashboard** — designed for a first-time user to identify who needs attention and what to do about it, with no manual required.")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('scored_members.csv')
        return df
    except FileNotFoundError:
        st.error("CRITICAL ERROR: 'scored_members.csv' not found. Run the Jupyter notebook pipeline first.")
        return pd.DataFrame()

df = load_data()

# Playbook logic is keyed explicitly by segment name -- one specific,
# concrete action per segment, not a generic message shown to everyone.
PLAYBOOKS = {
    'At-Risk Infrequent Flyers': {
        'risk_driver': "Low flight frequency (9.4 flights/yr avg, vs 18-22 for other segments) — the single strongest predictor of churn in this program.",
        'action': "Automated re-engagement email with a 15% discount, timed to each member's individual historical booking cadence (sent when they are statistically 'due' to book again).",
        'who': "Members in this segment with Churn Risk Score above the selected threshold.",
        'icon': "warning"
    },
    'High-Value Frequent Flyers': {
        'risk_driver': "Highest CLV segment in the program. Risk stems primarily from competitor status-matching, not disinterest.",
        'action': "Immediate, personal outreach from a dedicated account manager, paired with a complimentary 6-month tier upgrade.",
        'who': "Any flagged member in this segment — treat as high-priority regardless of risk score, given their CLV.",
        'icon': "error"
    },
    'Elite Professionals (Low-Frequency)': {
        'risk_driver': "Very high salary (avg $202K) and education (100% Doctor-level), but moderate flight frequency — value may be under-recognized by standard tier benefits.",
        'action': "Offer a complimentary lounge access or fast-track tier review; this segment likely qualifies for elite recognition their current activity level alone wouldn't trigger.",
        'who': "Flagged members in this segment.",
        'icon': "info"
    },
    'Married Loyalists': {
        'risk_driver': "Lowest churn rate in the program (2%). Risk, where present, is likely idiosyncratic rather than segment-driven.",
        'action': "Standard monitoring; no special intervention needed unless individually flagged at high risk.",
        'who': "Only members individually flagged above the risk threshold.",
        'icon': "success"
    },
    'Single Frequent Flyers': {
        'risk_driver': "Behaviorally similar to Married Loyalists (similar flight frequency, CLV) but unmarried — low churn (2%).",
        'action': "Standard monitoring; no special intervention needed unless individually flagged at high risk.",
        'who': "Only members individually flagged above the risk threshold.",
        'icon': "success"
    }
}

if not df.empty:
    st.sidebar.header("🎯 Retention Targeting")
    risk_threshold = st.sidebar.slider("Minimum Churn Risk %", 1, 50, 10)
    target_segment = st.sidebar.selectbox("Filter by Strategic Segment", ["All Segments"] + sorted(df['Strategic_Segment'].unique()))

    filtered_df = df[df['Churn_Risk_Score'] >= (risk_threshold / 100)]
    if target_segment != "All Segments":
        filtered_df = filtered_df[filtered_df['Strategic_Segment'] == target_segment]

    st.error(f"🚨 {len(filtered_df):,} members currently match this risk profile.")

    col1, col2, col3 = st.columns(3)
    col1.metric("Revenue at Risk (CLV)", f"${filtered_df['CLV'].sum():,.0f}")
    col2.metric("Avg Flights (2017)", f"{filtered_df['flights_2017'].mean():,.1f}")
    col3.metric("Avg Churn Risk", f"{filtered_df['Churn_Risk_Score'].mean()*100:.1f}%")

    st.markdown("---")
    st.subheader("📋 Operational Retention Playbook")

    # Only show playbooks for segments ACTUALLY PRESENT in the current
    # filtered view -- this is the real fix. The original dashboard
    # showed all 3 playbooks regardless of filter; this version shows
    # only what's relevant to what the user is currently looking at.
    segments_in_view = filtered_df['Strategic_Segment'].unique() if len(filtered_df) > 0 else []

    if len(segments_in_view) == 0:
        st.info("No members match the current filter. Adjust the risk threshold or segment filter.")
    else:
        for seg in segments_in_view:
            playbook = PLAYBOOKS.get(seg)
            if playbook is None:
                continue
            n_in_segment = len(filtered_df[filtered_df['Strategic_Segment'] == seg])
            box_text = (f"**{seg}** ({n_in_segment:,} members matching filter)\n\n"
                        f"**Risk Driver:** {playbook['risk_driver']}\n\n"
                        f"**Action:** {playbook['action']}\n\n"
                        f"**Who receives it:** {playbook['who']}")
            if playbook['icon'] == 'error':
                st.error(box_text)
            elif playbook['icon'] == 'warning':
                st.warning(box_text)
            elif playbook['icon'] == 'success':
                st.success(box_text)
            else:
                st.info(box_text)

    st.markdown("---")
    st.subheader("🔍 At-Risk Member Manifest")
    display_cols = ['Loyalty Number', 'Strategic_Segment', 'CLV', 'flights_2017', 'Churn_Risk_Score']
    st.dataframe(
        filtered_df[display_cols].sort_values(by='Churn_Risk_Score', ascending=False).head(100).style.format({
            'CLV': '${:,.2f}',
            'Churn_Risk_Score': '{:.1%}'
        })
    )
