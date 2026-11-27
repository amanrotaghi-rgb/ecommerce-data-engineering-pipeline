from pathlib import Path

import pandas as pd
import streamlit as st


# ==========================================================
# 1. PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="DataFlow | Engineering Control Center",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

DEMO_DATA_PATH = (
    Path(__file__).parent / "demo_data" / "orders_demo.csv"
)
EXPECTED_COLUMNS = [
    "order_id",
    "customer_id",
    "product",
    "category",
    "quantity",
    "price",
    "order_date",
]


# ==========================================================
# 2. PROFESSIONAL DATA ENGINEERING THEME
# ==========================================================

st.markdown(
    """
    <style>
    .stApp {
        background: #080f1c;
        color: #e6edf7;
        font-family: "Segoe UI", sans-serif;
    }
    .block-container {
        max-width: 1500px;
        padding: 2rem 2.5rem 3rem 2.5rem;
    }
    h1, h2, h3, h4 {
        color: #edf6ff !important;
        font-weight: 750 !important;
    }
    p { color: #bdcad9; line-height: 1.65; }
    section[data-testid="stSidebar"] {
        background: #101c2e;
        border-right: 1px solid #263d56;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #eaf4ff !important;
    }
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {
        color: #b8c8db !important;
    }
    .pipeline-header {
        background: linear-gradient(115deg, #11243b 0%, #123448 55%, #10404a 100%);
        border: 1px solid #286078;
        border-radius: 18px;
        padding: 35px 38px;
        margin-bottom: 32px;
        box-shadow: 0 12px 32px rgba(0,0,0,0.22);
    }
    .pipeline-eyebrow {
        color: #70cde8 !important;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 2.5px;
        margin-bottom: 12px;
    }
    .pipeline-title {
        color: #48d5ff !important;
        font-size: 32px;
        font-weight: 850;
        letter-spacing: 0.8px;
        line-height: 1.3;
    }
    .pipeline-subtitle {
        color: #c0d2e3 !important;
        font-size: 14px;
        margin-top: 12px;
        line-height: 1.8;
    }
    .pipeline-header-status {
        color: #f6c76a !important;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1px;
        margin-top: 20px;
    }
    .section-heading {
        color: #43d3ff !important;
        font-size: 20px;
        font-weight: 800;
        letter-spacing: 0.4px;
        margin-top: 18px;
        margin-bottom: 12px;
    }
    .metric-card {
        background: linear-gradient(145deg, #162940, #101c2e);
        border: 1px solid #2d4965;
        border-radius: 14px;
        padding: 21px;
        min-height: 125px;
    }
    .metric-label {
        color: #aebfd2 !important;
        font-size: 11px;
        font-weight: 750;
        text-transform: uppercase;
        letter-spacing: 1.1px;
    }
    .metric-value {
        color: #49d5ff !important;
        font-size: 26px;
        font-weight: 850;
        margin-top: 11px;
        overflow-wrap: anywhere;
    }
    .metric-description {
        color: #9aacc0 !important;
        font-size: 11px;
        margin-top: 7px;
    }
    .pipeline-node {
        background: linear-gradient(145deg, #172b43, #122137);
        border: 1px solid #31516e;
        border-radius: 14px;
        padding: 20px 12px;
        min-height: 145px;
        text-align: center;
    }
    .node-title {
        color: #edf6ff !important;
        font-size: 13px;
        font-weight: 800;
    }
    .node-subtitle {
        color: #b0c2d6 !important;
        font-size: 11px;
        margin-top: 7px;
    }
    .status-text {
        color: #f6c76a !important;
        font-size: 10px;
        font-weight: 800;
        margin-top: 10px;
    }
    div[data-testid="stMetric"] {
        background: #14243a;
        border: 1px solid #2d4965;
        border-radius: 13px;
        padding: 17px;
    }
    div[data-testid="stMetricLabel"] { color: #b1c2d5 !important; }
    div[data-testid="stMetricValue"] {
        color: #49d5ff !important;
        font-weight: 800;
    }
    .stButton > button {
        background: linear-gradient(110deg, #12415a, #15536a);
        color: #effaff;
        border: 1px solid #287c9c;
        border-radius: 9px;
        font-weight: 700;
    }
    .stButton > button:hover {
        background: #176782;
        color: white;
        border-color: #47d8ff;
    }
    .stTextInput input, .stDateInput input {
        background: #14243a !important;
        color: #edf6ff !important;
        border-radius: 8px;
    }
    .stTextInput label, .stDateInput label {
        color: #b9cadc !important;
    }
    div[data-testid="stDataFrame"] {
        border: 1px solid #2b4561;
        border-radius: 12px;
        overflow: hidden;
    }
    button[data-baseweb="tab"] {
        color: #b4c5d8 !important;
        font-weight: 650;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #45d5ff !important;
    }
    div[data-testid="stAlert"] { border-radius: 10px; }
    hr {
        border-color: #2b4058;
        margin-top: 24px;
        margin-bottom: 24px;
    }
    @media (max-width: 768px) {
        .block-container { padding-left: 1rem; padding-right: 1rem; }
        .pipeline-header { padding: 24px; }
        .pipeline-title { font-size: 24px; }
        .metric-value { font-size: 22px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# 3. DATA LOADING AND REUSABLE HELPERS
# ==========================================================

@st.cache_data(ttl=300)
def load_data():
    """Load the anonymized, public-demo CSV bundled with this app."""
    if not DEMO_DATA_PATH.is_file():
        raise FileNotFoundError(
            "Demo dataset not found. Expected file: "
            "dashboard/demo_data/orders_demo.csv"
        )

    data = pd.read_csv(DEMO_DATA_PATH)

    missing_columns = [
        column for column in EXPECTED_COLUMNS
        if column not in data.columns
    ]
    if missing_columns:
        raise ValueError(
            f"Demo dataset is missing required columns: {missing_columns}"
        )

    return data


def metric_card(label, value, description):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-description">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_heading(text):
    st.markdown(
        f'<div class="section-heading">▰ {text}</div>',
        unsafe_allow_html=True,
    )


def format_ist_date(value):
    if pd.isna(value):
        return "Not available"
    return pd.Timestamp(value).strftime("%d %b %Y")


# ==========================================================
# 4. DASHBOARD HEADER
# ==========================================================

st.markdown(
    """
    <div class="pipeline-header">
        <div class="pipeline-eyebrow">
            DATA ENGINEERING PLATFORM / PUBLIC DEMO
        </div>
        <div class="pipeline-title">
            ⚙ DATAFLOW CONTROL CENTER
        </div>
        <div class="pipeline-subtitle">
            End-to-End E-Commerce Data Pipeline Demonstration
            <br>
            PYTHON ETL &nbsp; • &nbsp;
            APACHE AIRFLOW &nbsp; • &nbsp;
            POSTGRESQL &nbsp; • &nbsp;
            AWS S3
        </div>
        <div class="pipeline-header-status">
            ● ANONYMIZED DEMO DATA LOADED
            &nbsp; | &nbsp;
            LIVE DATABASE AND AIRFLOW CONNECTIONS DISABLED
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# 5. SIDEBAR AND NAVIGATION
# ==========================================================

st.sidebar.markdown("## ⚙ DATAFLOW")
st.sidebar.caption("ENGINEERING CONTROL CENTER")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Pipeline Overview",
        "Data Quality",
        "Warehouse Analytics",
        "Raw Data Explorer",
    ],
)

st.sidebar.divider()

if st.sidebar.button("🔄 Refresh Dashboard", use_container_width=True):
    st.cache_data.clear()
    st.rerun()

st.sidebar.caption("Data source: Anonymized Demo CSV")
st.sidebar.caption("Records: Loaded from bundled dataset")
st.sidebar.caption("Airflow: Not connected in public demo")
st.sidebar.caption("PostgreSQL: Not connected in public demo")


# ==========================================================
# 6. LOAD AND PREPARE DATA
# ==========================================================

try:
    df = load_data()

    if df.empty:
        st.warning("The demo dataset contains no records.")
        st.stop()

    # Standardize data types for analysis.
    df["order_date"] = pd.to_datetime(
        df["order_date"], errors="coerce"
    )
    df["quantity"] = pd.to_numeric(
        df["quantity"], errors="coerce"
    )
    df["price"] = pd.to_numeric(
        df["price"], errors="coerce"
    )

    # Remove rows with unusable dates from date-filtered analysis.
    # The original loaded dataset remains unchanged in df.
    analysis_df = df.dropna(subset=["order_date"]).copy()

    if analysis_df.empty:
        st.error("No valid order dates were found in the demo dataset.")
        st.stop()

    analysis_df["revenue"] = (
        analysis_df["quantity"] * analysis_df["price"]
    )

    total_rows = len(df)
    total_orders = df["order_id"].nunique()
    total_customers = df["customer_id"].nunique()
    min_date = analysis_df["order_date"].min().date()
    max_date = analysis_df["order_date"].max().date()

    # Date filter
    st.sidebar.divider()
    st.sidebar.markdown("### DATA FILTER")

    date_filter = st.sidebar.date_input(
        "Order date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    if isinstance(date_filter, (tuple, list)) and len(date_filter) == 2:
        start_date, end_date = date_filter
        filtered_df = analysis_df[
            analysis_df["order_date"].dt.date.between(
                start_date, end_date
            )
        ].copy()
    else:
        filtered_df = analysis_df.copy()

    if filtered_df.empty:
        st.warning("No records found for the selected date range.")
        st.stop()

    filtered_df["revenue"] = (
        filtered_df["quantity"] * filtered_df["price"]
    )

    # ======================================================
    # 7. PIPELINE OVERVIEW
    # ======================================================

    if page == "Pipeline Overview":
        section_heading("PIPELINE ARCHITECTURE")
        st.caption(
            "Conceptual architecture of the implemented project. "
            "The public dashboard displays sample data; it does not "
            "execute or monitor a live pipeline."
        )

        pipeline = [
            ("📄", "RAW CSV", "Source dataset"),
            ("🐍", "PYTHON ETL", "Inspect & transform"),
            ("🛡️", "VALIDATION", "Data quality checks"),
            ("🐘", "POSTGRESQL", "Warehouse target"),
            ("☁️", "AWS S3", "Object storage target"),
        ]

        cols = st.columns(5)
        for col, item in zip(cols, pipeline):
            with col:
                st.markdown(
                    f"""
                    <div class="pipeline-node">
                        <div style="font-size:25px">{item[0]}</div>
                        <div class="node-title">{item[1]}</div>
                        <div class="node-subtitle">{item[2]}</div>
                        <div class="status-text">● PROJECT COMPONENT</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.divider()
        section_heading("AIRFLOW ORCHESTRATION")
        st.info(
            "Airflow is part of the project architecture, but live Airflow "
            "API monitoring is disabled in this public demo. DAG runs can "
            "be demonstrated separately in the local Airflow environment."
        )

        st.divider()
        section_heading("DEMO DATASET SUMMARY")

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            metric_card(
                "DEMO ROWS",
                f"{total_rows:,}",
                "Records in anonymized CSV",
            )
        with c2:
            metric_card(
                "UNIQUE ORDERS",
                f"{total_orders:,}",
                "Distinct order IDs",
            )
        with c3:
            metric_card(
                "CUSTOMERS",
                f"{total_customers:,}",
                "Distinct anonymized customer IDs",
            )
        with c4:
            metric_card(
                "DATA COLUMNS",
                f"{len(df.columns)}",
                "Fields in demo dataset",
            )

        st.divider()
        section_heading("ORDER VOLUME OVER TIME")

        monthly = (
            filtered_df.groupby(
                filtered_df["order_date"].dt.to_period("M")
            )
            .size()
            .reset_index(name="records")
        )
        monthly.columns = ["month", "records"]
        monthly["month"] = monthly["month"].astype(str)

        st.area_chart(
            monthly,
            x="month",
            y="records",
            color="#22d3ee",
        )

        st.caption(
            "Charts and metrics are calculated from the bundled "
            "anonymized demo CSV, not queried live from PostgreSQL."
        )

    # ======================================================
    # 8. DATA QUALITY
    # ======================================================

    elif page == "Data Quality":
        section_heading("DATA QUALITY MONITOR")

        missing_values = int(df.isna().sum().sum())
        duplicate_rows = int(df.duplicated().sum())

        invalid_quantity_mask = (
            df["quantity"].isna() | (df["quantity"] <= 0)
        )
        invalid_price_mask = (
            df["price"].isna() | (df["price"] < 0)
        )
        invalid_dates_mask = df["order_date"].isna()

        invalid_rows_mask = (
            df[EXPECTED_COLUMNS].isna().any(axis=1)
            | (df["quantity"] <= 0)
            | (df["price"] < 0)
        )

        valid_rows = int((~invalid_rows_mask).sum())

        q1, q2, q3, q4 = st.columns(4)
        with q1:
            metric_card(
                "DEMO ROWS",
                f"{total_rows:,}",
                "Loaded records",
            )
        with q2:
            metric_card(
                "NULL CELLS",
                f"{missing_values:,}",
                "Missing field values",
            )
        with q3:
            metric_card(
                "DUPLICATE ROWS",
                f"{duplicate_rows:,}",
                "Exact duplicate rows",
            )
        with q4:
            metric_card(
                "INVALID DATES",
                f"{int(invalid_dates_mask.sum()):,}",
                "Unparseable dates",
            )

        st.divider()
        st.markdown("### Validation checks")

        quality_df = pd.DataFrame(
            {
                "Quality Check": [
                    "Missing values",
                    "Duplicate rows",
                    "Invalid or non-positive quantity",
                    "Invalid or negative price",
                    "Invalid order dates",
                    "Rows passing basic checks",
                ],
                "Issue Count": [
                    missing_values,
                    duplicate_rows,
                    int(invalid_quantity_mask.sum()),
                    int(invalid_price_mask.sum()),
                    int(invalid_dates_mask.sum()),
                    valid_rows,
                ],
            }
        )

        st.dataframe(
            quality_df,
            use_container_width=True,
            hide_index=True,
        )

        st.caption(
            "These checks run against the anonymized demo CSV. "
            "They are not a live PostgreSQL quality report or a copy "
            "of the pipeline's historical rejected-record report."
        )

        st.markdown("### Column-level null analysis")
        null_df = df.isna().sum().reset_index()
        null_df.columns = ["Column", "Missing Values"]

        st.bar_chart(
            null_df,
            x="Column",
            y="Missing Values",
            color="#f59e0b",
        )

    # ======================================================
    # 9. WAREHOUSE ANALYTICS
    # ======================================================

    elif page == "Warehouse Analytics":
        section_heading("WAREHOUSE ANALYTICS")

        revenue = filtered_df["revenue"].sum()
        order_count = filtered_df["order_id"].nunique()
        average_order_value = revenue / order_count if order_count else 0

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            metric_card(
                "ORDERS",
                f"{order_count:,}",
                "Selected date range",
            )
        with c2:
            metric_card(
                "REVENUE",
                f"₹{revenue:,.0f}",
                "Calculated sales value",
            )
        with c3:
            metric_card(
                "CUSTOMERS",
                f"{filtered_df['customer_id'].nunique():,}",
                "Unique customers",
            )
        with c4:
            metric_card(
                "AVG ORDER VALUE",
                f"₹{average_order_value:,.2f}",
                "Revenue per unique order",
            )

        st.divider()
        st.markdown("### Monthly revenue")

        monthly_revenue = (
            filtered_df.groupby(
                filtered_df["order_date"].dt.to_period("M")
            )["revenue"]
            .sum()
            .reset_index()
        )
        monthly_revenue.columns = ["month", "revenue"]
        monthly_revenue["month"] = monthly_revenue["month"].astype(str)

        st.line_chart(
            monthly_revenue,
            x="month",
            y="revenue",
            color="#22d3ee",
        )

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Category performance")
            category_df = (
                filtered_df.groupby("category")["revenue"]
                .sum()
                .sort_values(ascending=False)
                .head(10)
                .reset_index()
            )
            st.bar_chart(
                category_df,
                x="category",
                y="revenue",
                color="#2dd4bf",
            )

        with col2:
            st.markdown("### Top 10 products")
            product_df = (
                filtered_df.groupby("product")["revenue"]
                .sum()
                .sort_values(ascending=False)
                .head(10)
                .reset_index()
            )
            st.bar_chart(
                product_df,
                x="product",
                y="revenue",
                color="#a78bfa",
            )

        st.caption(
            "Revenue is calculated as quantity × price from the "
            "anonymized demo records. Currency is displayed as INR "
            "for presentation."
        )

    # ======================================================
    # 10. RAW DATA EXPLORER
    # ======================================================

    elif page == "Raw Data Explorer":
        section_heading("DEMO DATA EXPLORER")
        st.caption(
            "Explore records from the anonymized CSV bundled with this demo."
        )

        search = st.text_input(
            "Search product, category, or customer ID"
        )

        display_df = filtered_df.copy()

        if search:
            search_columns = [
                "product",
                "category",
                "customer_id",
                "order_id",
            ]
            mask = pd.Series(False, index=display_df.index)

            for column in search_columns:
                mask |= display_df[column].astype(str).str.contains(
                    search,
                    case=False,
                    na=False,
                )

            display_df = display_df[mask]

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
        )

        st.caption(f"Showing {len(display_df):,} records.")

        csv_data = display_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇ Download CSV",
            data=csv_data,
            file_name="anonymized_demo_data_export.csv",
            mime="text/csv",
        )


except Exception as error:
    st.error("The public demo dashboard could not load its dataset.")
    st.exception(error)


# ==========================================================
# 11. FOOTER
# ==========================================================

st.divider()
st.markdown(
    """
    <div style="
        text-align:center;
        color:#64748b;
        font-size:12px;
        padding:10px;
    ">
        DATAFLOW CONTROL CENTER |
        PYTHON · AIRFLOW · POSTGRESQL · AWS S3
        <br>
        E-Commerce Data Engineering Project
        <br>
        Public demo uses anonymized CSV data; live services are not connected.
    </div>
    """,
    unsafe_allow_html=True,
)