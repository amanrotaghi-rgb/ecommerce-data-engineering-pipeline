
import streamlit as st
import psycopg2
import pandas as pd
import requests


# ==========================================================
# 1. PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="DataFlow | Engineering Control Center",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)


#
# ==========================================================
# 2. PROFESSIONAL DATA ENGINEERING THEME
# ==========================================================

st.markdown("""
<style>

/* GLOBAL */
.stApp {
    background: #080f1c;
    color: #e6edf7;
    font-family: "Segoe UI", sans-serif;
}

.block-container {
    max-width: 1500px;
    padding: 2rem 2.5rem 3rem 2.5rem;
}

/* TYPOGRAPHY */
h1, h2, h3, h4 {
    color: #edf6ff !important;
    font-weight: 750 !important;
}

p {
    color: #bdcad9;
    line-height: 1.65;
}

/* SIDEBAR */
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

/* HEADER */
.pipeline-header {
    background: linear-gradient(
        115deg,
        #11243b 0%,
        #123448 55%,
        #10404a 100%
    );
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
    color: #4ce0bd !important;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1px;
    margin-top: 20px;
}

/* SECTION HEADINGS */
.section-heading {
    color: #43d3ff !important;
    font-size: 20px;
    font-weight: 800;
    letter-spacing: 0.4px;
    margin-top: 18px;
    margin-bottom: 12px;
}

.section-description {
    color: #a9bbce !important;
    font-size: 13px;
    margin-bottom: 18px;
}

/* METRIC CARDS */
.metric-card {
    background: linear-gradient(145deg, #162940, #101c2e);
    border: 1px solid #2d4965;
    border-radius: 14px;
    padding: 21px;
    min-height: 125px;
    transition: 0.2s ease;
}

.metric-card:hover {
    border-color: #43c9ef;
    transform: translateY(-3px);
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

/* PIPELINE NODES */
.pipeline-node {
    background: linear-gradient(145deg, #172b43, #122137);
    border: 1px solid #31516e;
    border-radius: 14px;
    padding: 20px 12px;
    min-height: 145px;
    text-align: center;
    transition: 0.2s ease;
}

.pipeline-node:hover {
    border-color: #43d3ff;
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.2);
}

.node-icon {
    font-size: 27px;
    margin-bottom: 10px;
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
    color: #45ddc0 !important;
    font-size: 10px;
    font-weight: 800;
    margin-top: 10px;
}

/* INFORMATION PANELS */
.info-panel {
    background: #121f32;
    border: 1px solid #2b435d;
    border-radius: 14px;
    padding: 21px;
    margin-bottom: 15px;
}

.info-panel-title {
    color: #45d5ff !important;
    font-size: 15px;
    font-weight: 800;
}

.info-panel-text {
    color: #bdcad9 !important;
    font-size: 13px;
}

/* STREAMLIT METRICS */
div[data-testid="stMetric"] {
    background: #14243a;
    border: 1px solid #2d4965;
    border-radius: 13px;
    padding: 17px;
}

div[data-testid="stMetricLabel"] {
    color: #b1c2d5 !important;
}

div[data-testid="stMetricValue"] {
    color: #49d5ff !important;
    font-weight: 800;
}

/* BUTTONS */
.stButton > button {
    background: linear-gradient(110deg, #12415a, #15536a);
    color: #effaff;
    border: 1px solid #287c9c;
    border-radius: 9px;
    font-weight: 700;
    transition: 0.2s ease;
}

.stButton > button:hover {
    background: #176782;
    color: white;
    border-color: #47d8ff;
}

/* INPUTS */
.stTextInput input,
.stNumberInput input,
.stDateInput input {
    background: #14243a !important;
    color: #edf6ff !important;
    border-radius: 8px;
}

.stTextInput label,
.stNumberInput label,
.stDateInput label {
    color: #b9cadc !important;
}

/* TABLES */
div[data-testid="stDataFrame"] {
    border: 1px solid #2b4561;
    border-radius: 12px;
    overflow: hidden;
}

/* TABS */
button[data-baseweb="tab"] {
    color: #b4c5d8 !important;
    font-weight: 650;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #45d5ff !important;
}

/* ALERTS */
div[data-testid="stAlert"] {
    border-radius: 10px;
}

/* DIVIDERS */
hr {
    border-color: #2b4058;
    margin-top: 24px;
    margin-bottom: 24px;
}

/* RESPONSIVE */
@media (max-width: 768px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .pipeline-header {
        padding: 24px;
    }

    .pipeline-title {
        font-size: 24px;
    }

    .metric-value {
        font-size: 22px;
    }
}

</style>
""", unsafe_allow_html=True)



# ==========================================================
# 3. PROFESSIONAL DASHBOARD HEADER
# ==========================================================

st.html("""
<div class="pipeline-header">

    <div class="pipeline-eyebrow">
        DATA ENGINEERING PLATFORM / MONITORING
    </div>

    <div class="pipeline-title">
        ⚙ DATAFLOW CONTROL CENTER
    </div>

    <div class="pipeline-subtitle">
        End-to-End E-Commerce Data Pipeline Monitoring
        <br>
        PYTHON ETL &nbsp; • &nbsp;
        APACHE AIRFLOW &nbsp; • &nbsp;
        POSTGRESQL &nbsp; • &nbsp;
        AWS S3
    </div>

    <div class="pipeline-header-status">
        ● DATA WAREHOUSE CONNECTED
        &nbsp; | &nbsp;
        ORCHESTRATION MONITORING
    </div>

</div>
""")

# ==========================================================
# 3. DATABASE CONNECTION
# ==========================================================

def get_connection():

    return psycopg2.connect(
        host=st.secrets["postgres"]["host"],
        port=st.secrets["postgres"]["port"],
        database=st.secrets["postgres"]["database"],
        user=st.secrets["postgres"]["user"],
        password=st.secrets["postgres"]["password"]
    )


# ==========================================================
# 4. LOAD DATA FROM POSTGRESQL
# ==========================================================

@st.cache_data(ttl=300)
def load_data():

    connection = get_connection()

    try:

        query = """
            SELECT
                order_id,
                customer_id,
                product,
                category,
                quantity,
                price,
                order_date
            FROM orders;
        """

        df = pd.read_sql_query(query, connection)

    finally:
        connection.close()

    return df


# ==========================================================
# 5. AIRFLOW API CONNECTION
# ==========================================================

@st.cache_data(ttl=30)
def get_airflow_runs():

    try:

        airflow_url = st.secrets["airflow"]["base_url"]
        username = st.secrets["airflow"]["username"]
        password = st.secrets["airflow"]["password"]

        # Step 1: Authenticate with Airflow
        auth_response = requests.post(
            f"{airflow_url}/auth/token",
            json={
                "username": username,
                "password": password
            },
            timeout=10
        )

        auth_response.raise_for_status()

        # Step 2: Read authentication response
        auth_data = auth_response.json()

        if "access_token" not in auth_data:

            st.error(
                "Airflow did not return an access token. "
                f"Response keys: {list(auth_data.keys())}"
            )

            return []

        token = auth_data["access_token"]

        # Step 3: Fetch DAG runs
        runs_response = requests.get(
            f"{airflow_url}/api/v2/dags/ecommerce_data_pipeline/dagRuns",
            headers={
                "Authorization": f"Bearer {token}"
            },
            params={
                "limit": 5,
                "order_by": "-logical_date"
            },
            timeout=10
        )

        runs_response.raise_for_status()

        runs_data = runs_response.json()

        return runs_data.get("dag_runs", [])

    except requests.RequestException as error:

        st.error(
            f"Airflow HTTP/API error: {error}"
        )

        return []

    except KeyError as error:

        st.error(
            f"Missing Airflow secret key: {error}"
        )

        return []

    except ValueError as error:

        st.error(
            f"Airflow returned invalid JSON: {error}"
        )

        return []

    except Exception as error:

        st.error(
            f"Airflow monitoring error: {error}"
        )

        return []


# ==========================================================
# 6. REUSABLE METRIC CARD
# ==========================================================

def metric_card(label, value, description):

    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-description">{description}</div>
        </div>
    """, unsafe_allow_html=True)



# ==========================================================
# 8. SIDEBAR
# ==========================================================

st.sidebar.markdown("## ⚙ DATAFLOW")

st.sidebar.caption(
    "ENGINEERING CONTROL CENTER"
)

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Pipeline Overview",
        "Data Quality",
        "Warehouse Analytics",
        "Raw Data Explorer"
    ]
)

st.sidebar.divider()

if st.sidebar.button(
    "🔄 Refresh Dashboard",
    use_container_width=True
):

    st.cache_data.clear()
    st.rerun()

st.sidebar.caption("Data source: PostgreSQL")
st.sidebar.caption("Database: ecommerce_dw")
st.sidebar.caption("Orchestration: Apache Airflow")


# ==========================================================
# 9. LOAD AND PREPARE DATA
# ==========================================================

try:

    df = load_data()

    if df.empty:

        st.warning(
            "No records found in PostgreSQL."
        )

        st.stop()

    # Convert columns to appropriate data types

    df["order_date"] = pd.to_datetime(
        df["order_date"],
        errors="coerce"
    )

    df["quantity"] = pd.to_numeric(
        df["quantity"],
        errors="coerce"
    )

    df["price"] = pd.to_numeric(
        df["price"],
        errors="coerce"
    )

    df["revenue"] = (
        df["quantity"] * df["price"]
    )

    # Warehouse metrics

    total_rows = len(df)

    total_orders = df["order_id"].nunique()

    total_customers = df["customer_id"].nunique()

    total_revenue = df["revenue"].sum()

    min_date = df["order_date"].min()

    max_date = df["order_date"].max()

    # ------------------------------------------------------
    # DATASET FILTER
    # ------------------------------------------------------

    st.sidebar.divider()

    st.sidebar.markdown(
        "### DATA FILTER"
    )

    date_filter = st.sidebar.date_input(
        "Order date range",
        value=(
            min_date.date(),
            max_date.date()
        ),
        min_value=min_date.date(),
        max_value=max_date.date()
    )

    if len(date_filter) == 2:

        start_date, end_date = date_filter

        filtered_df = df[
            (df["order_date"].dt.date >= start_date)
            &
            (df["order_date"].dt.date <= end_date)
        ].copy()

    else:

        filtered_df = df.copy()

    if filtered_df.empty:

        st.warning(
            "No records for selected date range."
        )

        st.stop()

    filtered_df["revenue"] = (
        filtered_df["quantity"] * filtered_df["price"]
    )


    # ======================================================
    # 10. PIPELINE OVERVIEW
    # ======================================================

    if page == "Pipeline Overview":

        # --------------------------------------------------
        # PIPELINE ARCHITECTURE
        # --------------------------------------------------

        st.markdown(
            '<div class="section-heading">'
            '▰ PIPELINE ARCHITECTURE'
            '</div>',
            unsafe_allow_html=True
        )

        st.caption(
            "Configured data flow — execution status is "
            "monitored separately through Airflow."
        )

        pipeline = [
            ("📄", "RAW CSV", "Source Dataset"),
            ("🐍", "PYTHON ETL", "Inspect & Transform"),
            ("🛡", "VALIDATION", "Data Quality Checks"),
            ("🐘", "POSTGRESQL", "Data Warehouse"),
            ("☁", "AWS S3", "Processed Storage")
        ]

        cols = st.columns(5)

        for col, item in zip(cols, pipeline):

            with col:

                st.markdown(f"""
                <div class="pipeline-node">
                    <div style="font-size:25px">{item[0]}</div>
                    <div class="node-title">{item[1]}</div>
                    <div class="node-subtitle">{item[2]}</div>
                    <div class="status-text">● CONFIGURED</div>
                </div>
                """, unsafe_allow_html=True)

        st.divider()

        # --------------------------------------------------
        # AIRFLOW LIVE MONITORING
        # --------------------------------------------------

        st.markdown(
            '<div class="section-heading">'
            '▰ AIRFLOW ORCHESTRATION MONITORING'
            '</div>',
            unsafe_allow_html=True
        )

        airflow_runs = get_airflow_runs()

        if airflow_runs:

            latest_run = airflow_runs[0]

            run_state = (
                latest_run.get("state") or "unknown"
            )

            start_time = latest_run.get("start_date")

            end_time = latest_run.get("end_date")

            # Convert timestamps into Indian Standard Time

            start_display = (
                pd.to_datetime(
                    start_time,
                    utc=True
                )
                .tz_convert("Asia/Kolkata")
                .strftime("%d %b %Y, %I:%M:%S %p")
                if start_time else "Not available"
            )

            end_display = (
                pd.to_datetime(
                    end_time,
                    utc=True
                )
                .tz_convert("Asia/Kolkata")
                .strftime("%d %b %Y, %I:%M:%S %p")
                if end_time else "Running / Not available"
            )

            # Calculate actual execution duration

            duration_display = "Not available"

            if start_time and end_time:

                start_dt = pd.to_datetime(
                    start_time,
                    utc=True
                )

                end_dt = pd.to_datetime(
                    end_time,
                    utc=True
                )

                duration_seconds = (
                    end_dt - start_dt
                ).total_seconds()

                duration_display = (
                    f"{duration_seconds:.1f} seconds"
                )

            # Airflow metrics

            a1, a2, a3, a4 = st.columns(4)

            with a1:

                metric_card(
                    "LATEST DAG STATUS",
                    run_state.upper(),
                    "Actual Airflow execution state"
                )

            with a2:

                metric_card(
                    "DAG IDENTIFIER",
                    "ECOMMERCE",
                    "ecommerce_data_pipeline"
                )

            with a3:

                metric_card(
                    "EXECUTION DURATION",
                    duration_display,
                    "Latest DAG run"
                )

            with a4:

                metric_card(
                    "LATEST EXECUTION",
                    start_display,
                    "Start time in IST"
                )

            st.caption(
                f"Latest run completed: {end_display}"
            )

            st.markdown(
                "### Recent DAG Executions"
            )

            # Create recent DAG runs table

            runs_df = pd.DataFrame([

                {
                    "Run ID": run.get("dag_run_id"),

                    "State": (
                        run.get("state") or "unknown"
                    ).upper(),

                    "Start Time (IST)": (
                        pd.to_datetime(
                            run["start_date"],
                            utc=True
                        )
                        .tz_convert("Asia/Kolkata")
                        .strftime("%d %b %Y, %I:%M:%S %p")
                        if run.get("start_date")
                        else "Not available"
                    ),

                    "End Time (IST)": (
                        pd.to_datetime(
                            run["end_date"],
                            utc=True
                        )
                        .tz_convert("Asia/Kolkata")
                        .strftime("%d %b %Y, %I:%M:%S %p")
                        if run.get("end_date")
                        else "Running / Not available"
                    )
                }

                for run in airflow_runs

            ])

            st.dataframe(
                runs_df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.warning(
                "No DAG runs returned by Airflow. "
                "Check the Airflow API and credentials."
            )

        st.divider()

        # --------------------------------------------------
        # WAREHOUSE MONITORING
        # --------------------------------------------------

        st.markdown(
            '<div class="section-heading">'
            '▰ WAREHOUSE MONITORING'
            '</div>',
            unsafe_allow_html=True
        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            metric_card(
                "WAREHOUSE ROWS",
                f"{total_rows:,}",
                "Records in orders table"
            )

        with c2:

            metric_card(
                "UNIQUE ORDERS",
                f"{total_orders:,}",
                "Distinct order IDs"
            )

        with c3:

            metric_card(
                "CUSTOMERS",
                f"{total_customers:,}",
                "Distinct customer IDs"
            )

        with c4:

            metric_card(
                "DATA COLUMNS",
                f"{len(df.columns) - 1}",
                "Business columns"
            )

        st.divider()

        # --------------------------------------------------
        # PIPELINE DATA DISTRIBUTION
        # --------------------------------------------------

        st.markdown(
            '<div class="section-heading">'
            '▰ PIPELINE DATA DISTRIBUTION'
            '</div>',
            unsafe_allow_html=True
        )

        monthly = (
            filtered_df
            .groupby(
                filtered_df["order_date"].dt.to_period("M")
            )
            .size()
            .reset_index(name="records")
        )

        monthly.columns = [
            "month",
            "records"
        ]

        monthly["month"] = (
            monthly["month"].astype(str)
        )

        st.area_chart(
            monthly,
            x="month",
            y="records",
            color="#22d3ee"
        )

        st.caption(
            "Warehouse metrics are queried from PostgreSQL. "
            "DAG execution history is retrieved from the "
            "Airflow REST API."
        )


    # ======================================================
    # 11. DATA QUALITY
    # ======================================================

    elif page == "Data Quality":

        st.markdown(
            '<div class="section-heading">'
            '▰ DATA QUALITY MONITOR'
            '</div>',
            unsafe_allow_html=True
        )

        missing_values = int(
            df.isnull().sum().sum()
        )

        duplicate_rows = int(
            df.duplicated().sum()
        )

        invalid_quantity = int(
            (
                df["quantity"].isna()
                | (df["quantity"] <= 0)
            ).sum()
        )

        invalid_price = int(
            (
                df["price"].isna()
                | (df["price"] < 0)
            ).sum()
        )

        invalid_dates = int(
            df["order_date"].isna().sum()
        )

        invalid_rows = (
            df.isnull().any(axis=1)
            | (df["quantity"] <= 0)
            | (df["price"] < 0)
        )

        valid_rows = total_rows - int(
            invalid_rows.sum()
        )

        q1, q2, q3, q4 = st.columns(4)

        with q1:

            metric_card(
                "WAREHOUSE ROWS",
                f"{total_rows:,}",
                "Loaded records"
            )

        with q2:

            metric_card(
                "NULL CELLS",
                f"{missing_values:,}",
                "Missing field values"
            )

        with q3:

            metric_card(
                "DUPLICATE ROWS",
                f"{duplicate_rows:,}",
                "Exact duplicate rows"
            )

        with q4:

            metric_card(
                "INVALID DATES",
                f"{invalid_dates:,}",
                "Unparseable dates"
            )

        st.divider()

        st.markdown(
            "### Validation checks"
        )

        quality_df = pd.DataFrame({

            "Quality Check": [
                "Missing values",
                "Duplicate rows",
                "Invalid quantity",
                "Invalid price",
                "Invalid order dates"
            ],

            "Issue Count": [
                missing_values,
                duplicate_rows,
                invalid_quantity,
                invalid_price,
                invalid_dates
            ]

        })

        st.dataframe(
            quality_df,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "These checks run against the currently loaded "
            "PostgreSQL table, not the historical rejected CSV."
        )

        st.markdown(
            "### Column-level null analysis"
        )

        null_df = (
            df.isnull()
            .sum()
            .reset_index()
        )

        null_df.columns = [
            "Column",
            "Missing Values"
        ]

        st.bar_chart(
            null_df,
            x="Column",
            y="Missing Values",
            color="#f59e0b"
        )


    # ======================================================
    # 12. WAREHOUSE ANALYTICS
    # ======================================================

    elif page == "Warehouse Analytics":

        st.markdown(
            '<div class="section-heading">'
            '▰ WAREHOUSE ANALYTICS'
            '</div>',
            unsafe_allow_html=True
        )

        revenue = filtered_df["revenue"].sum()

        average_order_value = (

            revenue / filtered_df["order_id"].nunique()

            if filtered_df["order_id"].nunique() > 0

            else 0

        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            metric_card(
                "ORDERS",
                f"{filtered_df['order_id'].nunique():,}",
                "Selected period"
            )

        with c2:

            metric_card(
                "REVENUE",
                f"₹{revenue:,.0f}",
                "Calculated sales value"
            )

        with c3:

            metric_card(
                "CUSTOMERS",
                f"{filtered_df['customer_id'].nunique():,}",
                "Unique customers"
            )

        with c4:

            metric_card(
                "AVG ORDER VALUE",
                f"₹{average_order_value:,.2f}",
                "Revenue per order"
            )

        st.divider()

        st.markdown(
            "### Monthly revenue"
        )

        monthly_revenue = (
            filtered_df
            .groupby(
                filtered_df["order_date"].dt.to_period("M")
            )["revenue"]
            .sum()
            .reset_index()
        )

        monthly_revenue.columns = [
            "month",
            "revenue"
        ]

        monthly_revenue["month"] = (
            monthly_revenue["month"].astype(str)
        )

        st.line_chart(
            monthly_revenue,
            x="month",
            y="revenue",
            color="#22d3ee"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.markdown(
                "### Category performance"
            )

            category_df = (
                filtered_df
                .groupby("category")["revenue"]
                .sum()
                .sort_values(ascending=False)
                .head(10)
                .reset_index()
            )

            st.bar_chart(
                category_df,
                x="category",
                y="revenue",
                color="#2dd4bf"
            )

        with col2:

            st.markdown(
                "### Top 10 products"
            )

            product_df = (
                filtered_df
                .groupby("product")["revenue"]
                .sum()
                .sort_values(ascending=False)
                .head(10)
                .reset_index()
            )

            st.bar_chart(
                product_df,
                x="product",
                y="revenue",
                color="#a78bfa"
            )


    # ======================================================
    # 13. RAW DATA EXPLORER
    # ======================================================

    elif page == "Raw Data Explorer":

        st.markdown(
            '<div class="section-heading">'
            '▰ WAREHOUSE DATA EXPLORER'
            '</div>',
            unsafe_allow_html=True
        )

        st.caption(
            "Explore records loaded from PostgreSQL."
        )

        search = st.text_input(
            "Search product, category or customer ID"
        )

        display_df = filtered_df.copy()

        if search:

            mask = (

                display_df["product"].astype(str).str.contains(
                    search,
                    case=False,
                    na=False
                )

                |

                display_df["category"].astype(str).str.contains(
                    search,
                    case=False,
                    na=False
                )

                |

                display_df["customer_id"].astype(str).str.contains(
                    search,
                    case=False,
                    na=False
                )

            )

            display_df = display_df[mask]

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            f"Showing {len(display_df):,} records."
        )

        csv_data = (
            display_df.to_csv(index=False)
            .encode("utf-8")
        )

        st.download_button(
            "⬇ Download CSV",
            data=csv_data,
            file_name="warehouse_data_export.csv",
            mime="text/csv"
        )


# ==========================================================
# 14. ERROR HANDLING
# ==========================================================

except Exception as error:

    st.error(
        "Dashboard could not load data from PostgreSQL."
    )

    st.exception(error)


# ==========================================================
# 15. FOOTER
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
    </div>
    """,
    unsafe_allow_html=True
)
