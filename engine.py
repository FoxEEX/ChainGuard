import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------
# CONFIGURATION
# -------------------------------
HIGH_AMOUNT_THRESHOLD = 10000
MEDIUM_AMOUNT_THRESHOLD = 5000
NEW_WALLET_DAYS = 30

st.set_page_config(page_title="ChainGuard AI", layout="wide")

# -------------------------------
# HERO SECTION (CENTERED + PREMIUM)
# -------------------------------
st.markdown(
    """
    <div style="text-align:center; margin-top:20px;">
        <h1 style="
            font-size:48px;
            font-weight:700;
            letter-spacing:1px;
            margin-bottom:10px;">
            ChainGuard AI
        </h1>
        <h3 style="
            color:#9ca3af;
            font-weight:400;
            margin-top:0;">
            Explainable Fraud Detection for Blockchain Transactions
        </h3>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="
        text-align:center;
        max-width:850px;
        margin: 0 auto 30px auto;
        font-size:18px;
        color:#d1d5db;
        line-height:1.6;">
        ChainGuard AI analyzes blockchain transaction data and generates an 
        <span style="color:white; font-weight:600;">explainable risk score (0–100)</span> 
        to help analysts prioritize suspicious activity with clarity and confidence.
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="
        display:flex;
        justify-content:center;
        gap:40px;
        margin-bottom:30px;
        color:#9ca3af;
        font-size:15px;">
        <div>Deterministic Rule Engine</div>
        <div>Fully Explainable Alerts</div>
        <div>SOC-Style Workflow</div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<hr style='border:1px solid #1f2937;'>", unsafe_allow_html=True)

# -------------------------------
# FILE UPLOAD
# -------------------------------
uploaded_file = st.file_uploader("📂 Upload transactions CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # -------------------------------
    # HELPER DATA
    # -------------------------------
    tx_count = df.groupby("sender")["tx_id"].count().to_dict()
    avg_amount = df.groupby("sender")["amount"].mean().to_dict()
    incoming_counts = df.groupby("receiver")["tx_id"].count().to_dict()

    # -------------------------------
    # FRAUD SCORING FUNCTION
    # -------------------------------
    def calculate_risk(row):
        score = 0
        rules = []

        if row["amount"] > HIGH_AMOUNT_THRESHOLD:
            score += 30
            rules.append("High Transaction Amount")

        if tx_count.get(row["sender"], 0) >= 3:
            score += 20
            rules.append("Burst Transactions")

        if row["wallet_age_days"] < NEW_WALLET_DAYS and row["amount"] > MEDIUM_AMOUNT_THRESHOLD:
            score += 20
            rules.append("New Wallet High Activity")

        if 0 <= row["timestamp"].hour <= 4:
            score += 10
            rules.append("Unusual Transaction Time")

        if incoming_counts.get(row["sender"], 0) == 0:
            score += 10
            rules.append("One-Way Money Flow")

        avg = avg_amount.get(row["sender"], 0)
        if avg > 0 and row["amount"] > 2 * avg:
            score += 10
            rules.append("Sudden Behavior Change")

        score = min(score, 100)

        if score <= 30:
            level = "Low"
        elif score <= 70:
            level = "Medium"
        else:
            level = "High"

        return score, level, ", ".join(rules)

    df[["risk_score", "risk_level", "triggered_rules"]] = df.apply(
        lambda row: pd.Series(calculate_risk(row)), axis=1
    )

    # -------------------------------
    # RISK OVERVIEW
    # -------------------------------
    st.subheader("📊 Risk Overview")

    high_count = len(df[df["risk_level"] == "High"])
    medium_count = len(df[df["risk_level"] == "Medium"])
    low_count = len(df[df["risk_level"] == "Low"])

    col1, col2, col3 = st.columns(3)

    box_style = """
        background-color:#1f2933;
        padding:25px;
        border-radius:12px;
        text-align:center;
        border:1px solid #374151;
    """

    with col1:
        st.markdown(
            f"""
            <div style="{box_style}">
                <h4 style="color:#9ca3af;">High Risk</h4>
                <h1 style="color:white; font-size:48px;">{high_count}</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div style="{box_style}">
                <h4 style="color:#9ca3af;">Medium Risk</h4>
                <h1 style="color:white; font-size:48px;">{medium_count}</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div style="{box_style}">
                <h4 style="color:#9ca3af;">Low Risk</h4>
                <h1 style="color:white; font-size:48px;">{low_count}</h1>
            </div>
            """,
            unsafe_allow_html=True
        )

    # -------------------------------
    # ALERT INVESTIGATION
    # -------------------------------
    st.subheader("🚨 Alert Investigation")

    risk_filter = st.selectbox(
        "Filter by Risk Level",
        ["All", "High", "Medium", "Low"],
        index=0
    )

    filtered_df = df if risk_filter == "All" else df[df["risk_level"] == risk_filter]

    st.dataframe(
        filtered_df[
            [
                "tx_id",
                "sender",
                "receiver",
                "amount",
                "risk_score",
                "risk_level",
                "triggered_rules",
            ]
        ],
        use_container_width=True,
    )

    # -------------------------------
    # RISK INSIGHTS
    # -------------------------------
    st.subheader("📈 Risk Insights")

    left_col, right_col = st.columns(2)

    with left_col:
        risk_counts = (
            df["risk_level"]
            .value_counts()
            .reindex(["High", "Medium", "Low"], fill_value=0)
        )

        fig, ax = plt.subplots(figsize=(3, 3), facecolor="#111827")
        ax.set_facecolor("#0b0f14")

        ax.pie(
            risk_counts.values,
            labels=risk_counts.index,
            autopct="%1.1f%%",
            startangle=90,
            colors=["#ff4b4b", "#f7c948", "#4caf50"],
            wedgeprops={"edgecolor": "#111827"},
            textprops={"fontsize": 9, "color": "white"}
        )

        ax.axis("equal")
        st.pyplot(fig, use_container_width=False)

    with right_col:
        rules_series = (
            df["triggered_rules"]
            .dropna()
            .str.split(", ")
            .explode()
        )

        rules_series = rules_series[rules_series.str.strip() != ""]
        rule_counts = rules_series.value_counts()

        if not rule_counts.empty:
            rule_df = rule_counts.reset_index()
            rule_df.columns = ["Rule Name", "Times Triggered"]
            st.dataframe(rule_df, use_container_width=True)
        else:
            st.info("No detection rules were triggered.")

else:
    st.info("Upload a CSV file to start the analysis.")
