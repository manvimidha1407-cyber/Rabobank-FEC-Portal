import streamlit as st
import pandas as pd
import numpy as np
import io

# Page Configuration
st.set_page_config(page_title="Rabobank FEC Portal", layout="wide", initial_sidebar_state="expanded")

# --- CLEAN ENTERPRISE STYLING ---
st.markdown("""
    <style>
    .stApp {
        background-color: #FAFAFA;
        color: #1F2937;
    }
    .feature-card {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        padding: 24px;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        height: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# --- TOP HEADER & NAVIGATION BAR ---
col_logo, col_space, col_user = st.columns([3, 3, 2])

with col_logo:
    try:
        st.image("rabo.jpg", width=220)
    except:
        st.markdown("<h2 style='color: #002B49; margin: 0;'>Rabobank</h2>", unsafe_allow_html=True)

with col_user:
    st.markdown("""
        <div style="text-align: right; padding-top: 8px;">
            <span style="background-color: #002B49; color: white; padding: 8px 16px; border-radius: 6px; font-weight: 600; font-size: 13px;">
                👤 Compliance Officer ▼
            </span>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- INTERACTIVE CLICKABLE TABS ---
nav_tab1, nav_tab2, nav_tab3, nav_tab4 = st.tabs(["📊 Dashboard", "🌾 Trade Finance", "🛡️ Risk Compliance", "📋 Audit Logs"])

# ==========================================
# TAB 1: DASHBOARD
# ==========================================
with nav_tab1:
    
    hero_col1, hero_col2 = st.columns([3, 2])

    with hero_col1:
        st.markdown("<p style='font-size: 13px; font-weight: 700; color: #002B49; letter-spacing: 1px; text-transform: uppercase;'>Global Financial Economic Crime Compliance</p>", unsafe_allow_html=True)
        st.markdown("<h1 style='font-size: 36px; font-weight: 800; color: #111827; line-height: 1.2; margin-top: 0px;'>Automated Trade-Based Money Laundering (TBML) Screening</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 15px; color: #6B7280;'>Safeguarding Rabobank's agricultural commodity supply chains against price anomalies, capital flight, and high-risk offshore routing.</p>", unsafe_allow_html=True)

    with hero_col2:
        st.markdown("""
            <div style="background-color: #EEF2F6; padding: 20px; border-radius: 10px; border-left: 5px solid #002B49;">
                <h4 style="margin-top: 0; color: #002B49; font-size: 15px;">🔍 Intelligent Risk Engine Active</h4>
                <p style="font-size: 13px; color: #4B5563; margin-bottom: 0;">Real-time automated matching against global commodity baselines (Wheat, Corn, Soybean, Coffee, Cocoa) and FATF high-risk jurisdictions.</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    card1, card2, card3 = st.columns(3)
    with card1:
        st.markdown("""<div class="feature-card"><h3 style="font-size: 17px; color: #002B49; margin-top: 0;">🌾 Agro-Commodity Intelligence</h3><p style="font-size: 13px; color: #6B7280; margin-bottom: 0;">Dynamic price variance tracking designed specifically for Rabobank's core agricultural portfolio.</p></div>""", unsafe_allow_html=True)
    with card2:
        st.markdown("""<div class="feature-card"><h3 style="font-size: 17px; color: #002B49; margin-top: 0;">⚡ Instant Anomaly Triage</h3><p style="font-size: 13px; color: #6B7280; margin-bottom: 0;">Automated multi-factor scoring flags over-invoicing and offshore routing in seconds.</p></div>""", unsafe_allow_html=True)
    with card3:
        st.markdown("""<div class="feature-card"><h3 style="font-size: 17px; color: #002B49; margin-top: 0;">📄 Executive SAR Readiness</h3><p style="font-size: 13px; color: #6B7280; margin-bottom: 0;">One-click generation of compliance audit packages formatted for executive sign-off.</p></div>""", unsafe_allow_html=True)

    st.markdown("<br><hr><br>", unsafe_allow_html=True)

    MARKET_BASELINES = {"Wheat": 300, "Corn": 250, "Soybean": 500, "Coffee": 4000, "Cocoa": 3200}
    HIGH_RISK_JURISDICTIONS = ["Panama", "Cayman Islands", "Bermuda", "Seychelles", "Marshall Islands"]

    st.sidebar.markdown("### 🎛️ Terminal Control Center")
    upload_option = st.sidebar.radio("Data Stream:", ["Load 100-Item Simulated Batch", "Upload Custom File"])

    df_to_scan = None
    if upload_option == "Upload Custom File":
        uploaded_file = st.sidebar.file_uploader("Upload CSV / Excel Batch", type=["csv", "xlsx"])
        if uploaded_file is not None:
            try:
                df_to_scan = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
                st.sidebar.success("Dataset successfully ingested.")
            except Exception as e:
                st.sidebar.error(f"Error: {e}")
    else:
        np.random.seed(42)
        commodities = list(MARKET_BASELINES.keys())
        origins = ["Brazil", "Ukraine", "Argentina", "Colombia", "Ghana", "United States", "France", "Vietnam"]
        destinations = ["Netherlands", "Germany", "Spain", "Belgium", "Italy", "Japan", "Panama", "Cayman Islands", "Bermuda", "Seychelles"]
        
        rows = []
        for i in range(1, 101):
            comm = np.random.choice(commodities)
            base = MARKET_BASELINES[comm]
            orig = np.random.choice(origins)
            dest = np.random.choice(destinations)
            
            r_type = np.random.rand()
            if r_type < 0.70:
                price = int(base * np.random.uniform(0.90, 1.10))
                if dest in HIGH_RISK_JURISDICTIONS: dest = "Netherlands"
            elif r_type < 0.90:
                price = int(base * np.random.uniform(2.0, 4.5))
            else:
                price = int(base * np.random.uniform(0.3, 0.6))
                
            tons = int(np.random.choice([100, 250, 500, 1000, 1500, 2500, 5000]))
            rows.append({"Invoice_ID": f"INV-{9000 + i}", "Commodity": comm, "Volume_Tons": tons, "Declared_Price_Ton": price, "Origin_Country": orig, "Destination": dest})
        df_to_scan = pd.DataFrame(rows)

    if df_to_scan is not None and not df_to_scan.empty:
        def analyze_trade(row):
            comm = row.get("Commodity", "Wheat")
            declared = row.get("Declared_Price_Ton", 0)
            dest = row.get("Destination", "")
            base_price = MARKET_BASELINES.get(comm, 300)
            price_dev = ((declared - base_price) / base_price) * 100
            
            risk_score = 0
            risk_factors = []
            if price_dev > 30:
                risk_score += 60
                risk_factors.append(f"Over-Invoicing (+{price_dev:.1f}%)")
            elif price_dev < -30:
                risk_score += 40
                risk_factors.append(f"Under-Invoicing ({price_dev:.1f}%)")
            if dest in HIGH_RISK_JURISDICTIONS:
                risk_score += 40
                risk_factors.append(f"Offshore Zone ({dest})")
                
            if risk_score >= 60: classification = "🚨 HIGH RISK (Flagged)"
            elif risk_score >= 30: classification = "⚠️ MEDIUM RISK (Review)"
            else: classification = "✅ LOW RISK (Approved)"
            return pd.Series([base_price, f"{price_dev:+.1f}%", classification, ", ".join(risk_factors) if risk_factors else "None"])

        df_to_scan[["Market_Baseline", "Price_Variance", "Risk_Status", "Triggered_Alerts"]] = df_to_scan.apply(analyze_trade, axis=1)

        total_trades = len(df_to_scan)
        high_risks = len(df_to_scan[df_to_scan["Risk_Status"].str.contains("HIGH")])
        med_risks = len(df_to_scan[df_to_scan["Risk_Status"].str.contains("MEDIUM")])
        flagged_exposure = df_to_scan[df_to_scan["Risk_Status"].str.contains("HIGH|MEDIUM")]["Declared_Price_Ton"].sum()

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("📊 Total Audited Invoices", f"{total_trades}")
        m2.metric("🚨 High-Risk Alerts", f"{high_risks}", delta=f"{(high_risks/total_trades)*100:.1f}% flagged", delta_color="inverse")
        m3.metric("⚠️ Medium-Risk Reviews", f"{med_risks}")
        m4.metric("💰 Flagged Exposure Value", f"${flagged_exposure:,.0f}")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### 📋 Active Financial Crime Audit Queue")
        st.dataframe(df_to_scan, use_container_width=True, height=420)

        st.markdown("---")
        st.markdown("### 📄 Executive Action & SAR Reporting")
        col_dl1, col_dl2 = st.columns([2, 1])
        with col_dl1:
            st.write("Generate a standardized Financial Crime Compliance audit bundle formatted for executive sign-off.")
        with col_dl2:
            flagged_df = df_to_scan[df_to_scan["Risk_Status"].str.contains("HIGH|MEDIUM")]
            csv_buffer = io.StringIO()
            flagged_df.to_csv(csv_buffer, index=False)
            st.download_button(label="📥 Download SAR Bundle (CSV)", data=csv_buffer.getvalue(), file_name="Rabobank_FEC_HighRisk_Audit.csv", mime="text/csv", use_container_width=True)

# ==========================================
# TAB 2: TRADE FINANCE
# ==========================================
with nav_tab2:
    st.markdown("### 🌾 Agricultural Trade Finance & Market Baselines")
    st.write("Live reference pricing feed for Rabobank's core commodity financing portfolios across global exchanges.")
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown("#### 📈 Current Global Commodity Benchmarks")
        market_df = pd.DataFrame([
            {"Commodity": "Wheat (Soft Red)", "Exchange": "CME / CBOT", "Baseline Price ($/Ton)": "$300", "24h Trend": "+1.2%"},
            {"Commodity": "Corn (No.2 Yellow)", "Exchange": "CBOT", "Baseline Price ($/Ton)": "$250", "24h Trend": "-0.4%"},
            {"Commodity": "Soybeans", "Exchange": "CBOT", "Baseline Price ($/Ton)": "$500", "24h Trend": "+2.1%"},
            {"Commodity": "Coffee (Arabica)", "Exchange": "ICE", "Baseline Price ($/Ton)": "$4,000", "24h Trend": "+3.5%"},
            {"Commodity": "Cocoa Beans", "Exchange": "ICE Europe", "Baseline Price ($/Ton)": "$3,200", "24h Trend": "-1.1%"}
        ])
        st.dataframe(market_df, use_container_width=True)
        
    with col_t2:
        st.markdown("#### 🚢 Letter of Credit (LC) Financing Status")
        st.info("Active Letters of Credit currently under automated compliance review: **142 active transactions**.")
        st.success("Port of Rotterdam & Antwerp customs integration: **Connected & Synced**.")
        st.warning("Pending SWIFT MT799 message verifications: **3 transactions**.")

# ==========================================
# TAB 3: RISK COMPLIANCE
# ==========================================
with nav_tab3:
    st.markdown("### 🛡️ Risk & Compliance Policy Engine Settings")
    st.write("Configure the sensitivity parameters and jurisdictional watchlists governing automated trade screening.")
    
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.markdown("#### ⚙️ Algorithmic Risk Parameters")
        st.slider("Over-Invoicing Price Deviation Trigger (%)", min_value=10, max_value=50, value=30, step=5)
        st.slider("Under-Invoicing Discount Trigger (%)", min_value=10, max_value=60, value=30, step=5)
        st.selectbox("FATF High-Risk Jurisdiction Tier", ["Tier 1 (Strict Block & Alert)", "Tier 2 (Mandatory Manual Review)", "Tier 3 (Standard Monitoring)"])
        
    with col_r2:
        st.markdown("#### 🚨 Active Offshore Tax Haven Watchlist")
        st.text_area("Restricted Routing Zones", value="Panama, Cayman Islands, Bermuda, Seychelles, Marshall Islands, British Virgin Islands", height=120)
        st.button("Update Compliance Matrix")

# ==========================================
# TAB 4: AUDIT LOGS
# ==========================================
with nav_tab4:
    st.markdown("### 📋 System Audit Logs & Regulatory Trail")
    st.write("Immutable record of system screenings, user exports, and risk override actions.")
    
    audit_logs_df = pd.DataFrame([
        {"Timestamp": "2026-10-29 14:22:10", "User": "Compliance Officer (AM)", "Action": "Downloaded SAR High-Risk Bundle", "Status": "Success"},
        {"Timestamp": "2026-10-29 13:05:44", "User": "System Automated Engine", "Action": "Batch Scan Completed (100 Invoices)", "Status": "6 Alerts Flagged"},
        {"Timestamp": "2026-10-29 11:15:30", "User": "Compliance Officer (AM)", "Action": "Updated Commodity Baseline for Cocoa", "Status": "Modified to $3,200"},
        {"Timestamp": "2026-10-29 09:00:01", "User": "System Automated Engine", "Action": "Daily SWIFT & Trade Ledger Sync", "Status": "Connected"}
    ])
    st.dataframe(audit_logs_df, use_container_width=True)