# UPI Transaction Intelligence Dashboard

## Run locally

1. Install Python 3.10+.
2. Copy this dashboard folder into your project directory.
3. Ensure the expected `outputs/`, `deliverables/`, and `data/` folders are next to `app.py`, or set `UPI_PROJECT_DIR` to their parent directory.
4. Install dependencies:

   `pip install -r requirements.txt`

5. Launch:

   `streamlit run app.py`

## Expected data layout

- `outputs/npci_forecasting/npci_model_comparison_metrics.csv`
- `outputs/npci_forecasting/npci_model_comparison_holdout_predictions.csv`
- `outputs/npci_forecasting/npci_model_comparison_forecast_6_months.csv`
- `deliverables/npci_forecasting_final/final_model_metrics.csv`
- `deliverables/npci_forecasting_final/final_six_month_forecast.csv`
- `data/npci/npci_monthly_cleaned.csv`
- `data/phonepe/*.csv` (optional PhonePe Pulse exports only)
- `outputs/mdr/*.csv` (optional MDR scenario outputs)

NPCI and PhonePe Pulse are intentionally separate. The dashboard does not join them.
Missing optional files produce an informational message; add the files or adjust paths in `app.py`.

## Important interpretation notes

- Forecasts are model estimates, not guarantees.
- Historical evaluation metrics apply to the holdout period used in model comparison.
- MDR values are scenario estimates based on assumptions, not observed transaction-level fees.
