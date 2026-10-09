from pathlib import Path
import json
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="UPI Transaction Intelligence", page_icon="📊", layout="wide")

# Set this to the folder containing app.py, or provide UPI_PROJECT_DIR as an environment variable.
import os
PROJECT = Path(os.environ.get("UPI_PROJECT_DIR", Path(__file__).resolve().parent))
NPCI_FORECAST_DIR = PROJECT / "outputs" / "npci_forecasting"
NPCI_FINAL_DIR = PROJECT / "deliverables" / "npci_forecasting_final"
PHONEPE_DIR = PROJECT / "data" / "phonepe"
NPCI_DATA_DIR = PROJECT / "data" / "npci"
MDR_DIR = PROJECT / "outputs" / "mdr"

st.title("UPI Transaction Intelligence")
st.caption("Big-data analytics • Independent data pipelines for NPCI and PhonePe Pulse")

def first_existing(paths):
    for p in paths:
        if p.exists() and p.is_file():
            return p
    return None

def load_csv(paths):
    path = first_existing(paths)
    if path is None:
        return None, None
    try:
        return pd.read_csv(path), path
    except Exception as exc:
        st.warning(f"Could not read {path.name}: {exc}")
        return None, path

def load_json(paths):
    path = first_existing(paths)
    if path is None:
        return None, None
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f), path
    except Exception as exc:
        st.warning(f"Could not read {path.name}: {exc}")
        return None, path

page = st.sidebar.radio("Navigate", ["Overview", "NPCI Analytics", "PhonePe Pulse", "MDR Rules Engine"])
st.sidebar.caption("NPCI and PhonePe data are deliberately not merged.")

if page == "Overview":
    st.subheader("Project overview")
    c1, c2, c3 = st.columns(3)
    forecast, _ = load_csv([
        NPCI_FORECAST_DIR / "npci_model_comparison_forecast_6_months.csv",
        NPCI_FINAL_DIR / "final_six_month_forecast.csv",
    ])
    metrics, _ = load_csv([
        NPCI_FORECAST_DIR / "npci_model_comparison_metrics.csv",
        NPCI_FINAL_DIR / "final_model_metrics.csv",
    ])
    phonepe_files = list(PHONEPE_DIR.glob("*.csv")) if PHONEPE_DIR.exists() else []
    mdr_files = list(MDR_DIR.glob("*.csv")) if MDR_DIR.exists() else []
    c1.metric("NPCI forecast rows", int(len(forecast)) if forecast is not None else 0)
    c2.metric("Model metric rows", int(len(metrics)) if metrics is not None else 0)
    c3.metric("PhonePe CSV files", len(phonepe_files))
    st.markdown("### Artifact availability")
    status = pd.DataFrame([
        {"Pipeline": "NPCI forecasting", "Status": "Available" if forecast is not None else "Missing forecast CSV"},
        {"Pipeline": "PhonePe Pulse", "Status": f"{len(phonepe_files)} CSV file(s)" if phonepe_files else "Optional files not found"},
        {"Pipeline": "MDR Rules Engine", "Status": f"{len(mdr_files)} CSV file(s)" if mdr_files else "Optional scenario outputs not found"},
    ])
    st.dataframe(status, use_container_width=True, hide_index=True)
    st.info("If a section reports missing files, copy the corresponding notebook outputs into the documented project folders or update the paths in app.py.")

elif page == "NPCI Analytics":
    st.subheader("NPCI national UPI analytics")
    monthly, monthly_path = load_csv([
        NPCI_DATA_DIR / "npci_monthly_cleaned.csv",
        PROJECT / "npci_monthly_cleaned.csv",
        PROJECT / "data" / "npci_monthly_cleaned.csv",
    ])
    metrics, metrics_path = load_csv([
        NPCI_FORECAST_DIR / "npci_model_comparison_metrics.csv",
        NPCI_FINAL_DIR / "final_model_metrics.csv",
    ])
    forecast, forecast_path = load_csv([
        NPCI_FORECAST_DIR / "npci_model_comparison_forecast_6_months.csv",
        NPCI_FINAL_DIR / "final_six_month_forecast.csv",
    ])
    holdout, holdout_path = load_csv([
        NPCI_FORECAST_DIR / "npci_model_comparison_holdout_predictions.csv",
        NPCI_FINAL_DIR / "final_holdout_predictions.csv",
    ])

    if monthly is not None:
        date_col = next((c for c in ["date", "Date", "month_date", "Month_Date"] if c in monthly.columns), None)
        if date_col:
            monthly[date_col] = pd.to_datetime(monthly[date_col], errors="coerce")
            monthly = monthly.dropna(subset=[date_col]).sort_values(date_col)
            volume_col = next((c for c in ["volume_mn", "Volume (In Mn.)", "volume"] if c in monthly.columns), None)
            value_col = next((c for c in ["value_cr", "Value (In Cr.)", "value"] if c in monthly.columns), None)
            if volume_col:
                st.markdown("#### Historical transaction volume")
                st.plotly_chart(px.line(monthly, x=date_col, y=volume_col, markers=True, title="NPCI monthly transaction volume"), use_container_width=True)
            if value_col:
                st.markdown("#### Historical transaction value")
                st.plotly_chart(px.line(monthly, x=date_col, y=value_col, markers=True, title="NPCI monthly transaction value"), use_container_width=True)
        else:
            st.warning(f"Loaded {monthly_path.name}, but no recognized date column was found.")
            st.dataframe(monthly.head(20), use_container_width=True)
    else:
        st.warning("NPCI historical CSV not found. Add npci_monthly_cleaned.csv to data/npci/.")

    if metrics is not None:
        st.markdown("#### Forecast model comparison")
        st.dataframe(metrics, use_container_width=True, hide_index=True)
        target_col = next((c for c in ["target", "Target", "metric_target"] if c in metrics.columns), None)
        model_col = next((c for c in ["model", "Model", "model_name"] if c in metrics.columns), None)
        rmse_col = next((c for c in ["rmse", "RMSE"] if c in metrics.columns), None)
        if target_col and model_col and rmse_col:
            st.plotly_chart(px.bar(metrics, x=model_col, y=rmse_col, color=target_col, barmode="group", title="RMSE by target and model (lower is better)"), use_container_width=True)

    if forecast is not None:
        st.markdown("#### Six-month forecast")
        st.dataframe(forecast, use_container_width=True, hide_index=True)
        date_col = next((c for c in ["date", "Date", "month", "Month", "forecast_month"] if c in forecast.columns), None)
        if date_col:
            forecast[date_col] = forecast[date_col].astype(str)
            numeric_cols = [c for c in forecast.columns if c != date_col and pd.api.types.is_numeric_dtype(forecast[c])]
            if numeric_cols:
                st.plotly_chart(px.line(forecast, x=date_col, y=numeric_cols, markers=True, title="Forecast horizon"), use_container_width=True)
    else:
        st.warning("Six-month forecast CSV not found. Run Notebooks 03–05 and copy the exported CSV.")

    if holdout is not None:
        with st.expander("Holdout predictions"):
            st.dataframe(holdout, use_container_width=True, hide_index=True)

elif page == "PhonePe Pulse":
    st.subheader("PhonePe Pulse analytics")
    st.caption("This section reads PhonePe files only. It does not join or compare records with NPCI.")
    if PHONEPE_DIR.exists():
        files = sorted(PHONEPE_DIR.glob("*.csv"))
        if files:
            selected = st.selectbox("Choose a PhonePe CSV", files, format_func=lambda p: p.name)
            try:
                data = pd.read_csv(selected)
                st.write(f"Source file: `{selected.name}`")
                st.dataframe(data, use_container_width=True, hide_index=True)
                numeric = data.select_dtypes(include="number").columns.tolist()
                categorical = [c for c in data.columns if c not in numeric]
                if numeric and categorical:
                    x = st.selectbox("Category / dimension", categorical)
                    y = st.selectbox("Numeric measure", numeric)
                    summary = data.groupby(x, dropna=False)[y].sum().reset_index().sort_values(y, ascending=False).head(25)
                    st.plotly_chart(px.bar(summary, x=x, y=y, title=f"{y} by {x} (top 25)"), use_container_width=True)
            except Exception as exc:
                st.error(f"Could not load selected CSV: {exc}")
        else:
            st.info("No CSV files found in data/phonepe/. Export the relevant PhonePe Gold tables from the master notebook to this folder.")
    else:
        st.info("Create data/phonepe/ and place PhonePe Pulse CSV exports there. Example exports: state-quarter, category-quarter, top-pincode. This section remains independent of NPCI.")

elif page == "MDR Rules Engine":
    st.subheader("MDR Rules Engine")
    st.caption("Scenario estimates only. They are not observed UPI transaction-level fees or actual settlement records.")
    if MDR_DIR.exists():
        files = sorted(MDR_DIR.glob("*.csv"))
        if files:
            selected = st.selectbox("Choose an MDR output CSV", files, format_func=lambda p: p.name)
            try:
                mdr = pd.read_csv(selected)
                st.write(f"Source file: `{selected.name}`")
                st.dataframe(mdr, use_container_width=True, hide_index=True)
            except Exception as exc:
                st.error(f"Could not load MDR file: {exc}")
        else:
            st.info("No MDR CSV outputs found in outputs/mdr/. Export the scenario results from the MDR Rules Engine notebook section.")
    else:
        st.info("Create outputs/mdr/ and copy the MDR scenario CSV output there. Keep assumptions explicit.")
