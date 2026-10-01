import sys
from pathlib import Path

import pandas as pd
import streamlit as st


# ---------------------------------------------------------------------
# Project path setup
# ---------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


# ---------------------------------------------------------------------
# Application services
# ---------------------------------------------------------------------

from memristor_app.services.data_service import DataService
from memristor_app.services.integration_service import IntegrationService


# ---------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------

st.set_page_config(
    page_title="Memristor Analysis",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------

st.markdown(
    """
    <style>
        .main-title {
            font-size: 2.4rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }

        .subtitle {
            font-size: 1.05rem;
            color: #666;
            margin-bottom: 1.5rem;
        }

        .metric-card {
            padding: 1rem;
            border-radius: 10px;
            border: 1px solid #ddd;
            background-color: #fafafa;
        }

        .section-title {
            font-size: 1.4rem;
            font-weight: 600;
            margin-top: 1.5rem;
            margin-bottom: 0.8rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------

data_service = DataService()
integration_service = IntegrationService()


# ---------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------

def detect_voltage_current_pairs(dataframe: pd.DataFrame):
    """
    Detect Voltage-Current column pairs automatically.

    First tries column names such as:
        V1, I1
        Voltage1, Current1

    If no valid named pairs are found, falls back to
    alternating columns:
        column 1 -> Voltage
        column 2 -> Current
        column 3 -> Voltage
        column 4 -> Current
        ...
    """

    columns = list(dataframe.columns)
    pairs = []

    for index in range(len(columns) - 1):
        voltage_column = columns[index]
        current_column = columns[index + 1]

        voltage_text = str(voltage_column).strip().lower()
        current_text = str(current_column).strip().lower()

        voltage_is_valid = (
            voltage_text.startswith("v")
            or voltage_text.startswith("voltage")
        )

        current_is_valid = (
            current_text.startswith("i")
            or current_text.startswith("current")
        )

        if voltage_is_valid and current_is_valid:
            pairs.append((voltage_column, current_column))

    # Alternating-column fallback
    if not pairs and len(columns) >= 2:
        if len(columns) % 2 == 0:
            for index in range(0, len(columns), 2):
                pairs.append((columns[index], columns[index + 1]))

    return pairs


def dataframe_to_excel(
    cycles_df,
    measure_df,
    mean_df,
    variance_df,
):
    """
    Create the same four-sheet Excel structure used
    by the desktop application.
    """

    import io

    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        cycles_df.to_excel(
            writer,
            sheet_name="Cycles",
            index=True,
        )

        measure_df.to_excel(
            writer,
            sheet_name="Measure",
            index=True,
        )

        mean_df.to_excel(
            writer,
            sheet_name="mean Function",
            index=False,
        )

        variance_df.to_excel(
            writer,
            sheet_name="Variance function",
            index=True,
        )

    output.seek(0)

    return output.getvalue()


def get_measure_value(measure_df, metric_name):
    """
    Safely retrieve a metric from the Measure dataframe.

    The original analysis output stores:
        - "Mean" as the row index
        - metric names as columns

    This function also supports the alternative layout
    where metric names are stored in the index.
    """

    if measure_df is None or measure_df.empty:
        return None

    try:
        # Main layout used by the current IntegrationService:
        # Index = "Mean"
        # Columns = metric names
        if metric_name in measure_df.columns:

            if "Mean" in measure_df.index:
                value = measure_df.loc["Mean", metric_name]
            else:
                value = measure_df.iloc[0][metric_name]

            if pd.isna(value):
                return None

            return float(value)

        # Alternative layout:
        # Index = metric names
        # Column = "Mean"
        if metric_name in measure_df.index and "Mean" in measure_df.columns:

            value = measure_df.loc[metric_name, "Mean"]

            if pd.isna(value):
                return None

            return float(value)

    except (KeyError, TypeError, ValueError, IndexError):
        return None

    return None

# ---------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------

st.markdown(
    '<div class="main-title">⚡ Memristor Analysis</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    "Numerical analysis of Voltage–Current memristor data"
    "</div>",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------

with st.sidebar:

    st.header("Analysis")

    integration_method = st.selectbox(
        "Integration Method",
        [
            "Trapezoidal Rule",
            "Simpson's 1/3 Rule",
            "Simpson's 3/8 Rule",
        ],
        index=1,
    )

    st.divider()

    st.markdown("### About")

    st.write(
        "This web application uses the same analysis "
        "service as the Memristor Analysis desktop "
        "application."
    )

    st.write(
        "Voltage–Current pairs are detected automatically. "
        "No manual X/Y variable selection is required."
    )


# ---------------------------------------------------------------------
# File upload
# ---------------------------------------------------------------------

st.markdown(
    '<div class="section-title">1. Load Dataset</div>',
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader(
    "Upload your memristor dataset",
    type=["xlsx", "xls", "csv"],
    help=(
        "Supported formats: Excel (.xlsx, .xls) "
        "and CSV (.csv)"
    ),
)


# ---------------------------------------------------------------------
# Main workflow
# ---------------------------------------------------------------------

if uploaded_file is None:

    st.info(
        "Upload an Excel or CSV dataset to begin the analysis."
    )

    st.markdown(
        """
        ### Expected Dataset Structure

        The application automatically detects alternating
        Voltage–Current pairs, for example:

        `V1, I1, V2, I2, V3, I3, ...`

        It can also recognize names such as:

        `Voltage1, Current1, Voltage2, Current2, ...`
        """
    )

    st.stop()


# ---------------------------------------------------------------------
# Read uploaded file
# ---------------------------------------------------------------------

try:

    file_extension = Path(uploaded_file.name).suffix.lower()

    if file_extension == ".csv":

        dataframe = pd.read_csv(uploaded_file)

    else:

        dataframe = pd.read_excel(uploaded_file)

except Exception as error:

    st.error(
        f"Unable to read the uploaded dataset: {error}"
    )

    st.stop()


# ---------------------------------------------------------------------
# Dataset information
# ---------------------------------------------------------------------

detected_pairs = detect_voltage_current_pairs(dataframe)

st.markdown(
    '<div class="section-title">2. Dataset Information</div>',
    unsafe_allow_html=True,
)

info_col1, info_col2, info_col3 = st.columns(3)

with info_col1:
    st.metric(
        "Data Points",
        len(dataframe),
    )

with info_col2:
    st.metric(
        "Dataset Columns",
        len(dataframe.columns),
    )

with info_col3:
    st.metric(
        "V-I Pairs",
        len(detected_pairs),
    )


if not detected_pairs:

    st.error(
        "No valid Voltage–Current pairs were detected."
    )

    st.write("Dataset columns:")

    st.dataframe(
        pd.DataFrame(
            {
                "Column": list(dataframe.columns)
            }
        ),
        use_container_width=True,
    )

    st.stop()


# ---------------------------------------------------------------------
# Detected pairs
# ---------------------------------------------------------------------

with st.expander(
    "View detected Voltage–Current pairs"
):

    pair_data = []

    for number, pair in enumerate(
        detected_pairs,
        start=1,
    ):
        pair_data.append(
            {
                "Cycle": number,
                "Voltage": pair[0],
                "Current": pair[1],
            }
        )

    st.dataframe(
        pd.DataFrame(pair_data),
        use_container_width=True,
        hide_index=True,
    )


# ---------------------------------------------------------------------
# Dataset preview
# ---------------------------------------------------------------------

with st.expander("Preview Dataset"):

    st.dataframe(
        dataframe.head(20),
        use_container_width=True,
    )


# ---------------------------------------------------------------------
# Run analysis
# ---------------------------------------------------------------------

st.markdown(
    '<div class="section-title">3. Run Analysis</div>',
    unsafe_allow_html=True,
)

st.write(
    f"**Integration method:** {integration_method}"
)

st.write(
    f"**Cycles detected:** {len(detected_pairs)}"
)

run_analysis = st.button(
    "▶ Run Memristor Analysis",
    type="primary",
    use_container_width=True,
)


if run_analysis:

    with st.spinner(
        "Processing all Voltage–Current cycles..."
    ):

        try:

            (
                cycles_df,
                measure_df,
                mean_df,
                variance_df,
            ) = integration_service.process_data(
                dataframe,
                method=integration_method,
            )

        except Exception as error:

            st.error(
                "Analysis failed."
            )

            st.exception(error)

            st.stop()


    # Store results in session state
    st.session_state["cycles_df"] = cycles_df
    st.session_state["measure_df"] = measure_df
    st.session_state["mean_df"] = mean_df
    st.session_state["variance_df"] = variance_df
    st.session_state["integration_method"] = integration_method

    st.success(
        "Analysis completed successfully."
    )


# ---------------------------------------------------------------------
# Display stored results
# ---------------------------------------------------------------------

if "cycles_df" not in st.session_state:

    st.info(
        "Click **Run Memristor Analysis** to generate results."
    )

    st.stop()


cycles_df = st.session_state["cycles_df"]
measure_df = st.session_state["measure_df"]
mean_df = st.session_state["mean_df"]
variance_df = st.session_state["variance_df"]

current_method = st.session_state[
    "integration_method"
]


# ---------------------------------------------------------------------
# Results summary
# ---------------------------------------------------------------------

st.markdown(
    '<div class="section-title">4. Analysis Summary</div>',
    unsafe_allow_html=True,
)

summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)

with summary_col1:

    st.metric(
        "Cycles Processed",
        len(detected_pairs),
    )

with summary_col2:

    st.metric(
        "Integration",
        current_method,
    )

with summary_col3:

    phl_area = get_measure_value(
        measure_df,
        "PHL Area",
    )

    if phl_area is not None:

        st.metric(
            "Mean PHL Area",
            f"{phl_area:.6g}",
        )

    else:

        st.metric(
            "Mean PHL Area",
            "N/A",
        )

with summary_col4:

    loop_ratio = get_measure_value(
        measure_df,
        "Loop to Rectangle ratio",
    )

    if loop_ratio is not None:

        st.metric(
            "Mean Loop / Rectangle",
            f"{loop_ratio:.6g}",
        )

    else:

        st.metric(
            "Mean Loop / Rectangle",
            "N/A",
        )


# ---------------------------------------------------------------------
# Results tabs
# ---------------------------------------------------------------------

st.markdown(
    '<div class="section-title">5. Results</div>',
    unsafe_allow_html=True,
)

(
    tab_cycles,
    tab_measure,
    tab_mean,
    tab_variance,
    tab_plot,
) = st.tabs(
    [
        "Cycles",
        "Measure",
        "Mean Function",
        "Variance Function",
        "V-I Loops",
    ]
)


# ---------------------------------------------------------------------
# Cycles
# ---------------------------------------------------------------------

with tab_cycles:

    st.subheader("Cycle-wise Measurements")

    display_cycles = cycles_df.copy()

    display_cycles.insert(
        0,
        "Cycle",
        range(
            1,
            len(display_cycles) + 1,
        ),
    )

    st.dataframe(
        display_cycles,
        use_container_width=True,
        height=500,
    )


# ---------------------------------------------------------------------
# Measure
# ---------------------------------------------------------------------

with tab_measure:

    st.subheader(
        "Mean of Cycle-wise Measurements"
    )

    display_measure = measure_df.copy()

    if "Mean" in display_measure.columns:

        display_measure = (
            display_measure[
                ["Mean"]
            ]
            .rename(
                columns={
                    "Mean": "Value"
                }
            )
        )

        display_measure.index.name = "Metric"

    st.dataframe(
        display_measure,
        use_container_width=True,
        height=500,
    )


# ---------------------------------------------------------------------
# Mean Function
# ---------------------------------------------------------------------

with tab_mean:

    st.subheader(
        "Mean Function"
    )

    st.dataframe(
        mean_df,
        use_container_width=True,
        height=500,
    )


# ---------------------------------------------------------------------
# Variance Function
# ---------------------------------------------------------------------

with tab_variance:

    st.subheader(
        "Variance Function"
    )

    st.dataframe(
        variance_df,
        use_container_width=True,
        height=500,
    )


# ---------------------------------------------------------------------
# V-I Plot
# ---------------------------------------------------------------------

with tab_plot:

    st.subheader(
        "Voltage–Current Loops"
    )

    try:

        import plotly.graph_objects as go

        figure = go.Figure()

        for number, (voltage_column, current_column) in enumerate(
            detected_pairs,
            start=1,
        ):

            figure.add_trace(
                go.Scatter(
                    x=dataframe[voltage_column],
                    y=dataframe[current_column],
                    mode="lines",
                    name=f"Cycle {number}",
                )
            )

        figure.update_layout(
            title="Memristor V-I Loops",
            xaxis_title="Voltage",
            yaxis_title="Current",
            template="plotly_white",
            hovermode="closest",
            height=650,
            legend_title="Cycles",
        )

        st.plotly_chart(
            figure,
            use_container_width=True,
        )

    except ImportError:

        st.warning(
            "Plotly is not installed yet. "
            "The numerical results are available, "
            "but the interactive V-I plot requires Plotly."
        )


# ---------------------------------------------------------------------
# Excel export
# ---------------------------------------------------------------------

st.markdown(
    '<div class="section-title">6. Export Results</div>',
    unsafe_allow_html=True,
)

excel_data = dataframe_to_excel(
    cycles_df,
    measure_df,
    mean_df,
    variance_df,
)

st.download_button(
    label="⬇ Download Excel Report",
    data=excel_data,
    file_name="Memristor_Analysis_Report.xlsx",
    mime=(
        "application/vnd.openxmlformats-officedocument."
        "spreadsheetml.sheet"
    ),
    use_container_width=True,
)


# ---------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------

st.divider()

st.caption(
    "Memristor Analysis | Numerical analysis framework "
    "for Voltage–Current memristor data"
)