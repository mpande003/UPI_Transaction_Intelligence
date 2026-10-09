# NPCI Monthly UPI Forecasting — Final Report

## Executive summary

The dataset contains 126 monthly observations from April 2016 through September 2026. Models were compared using a chronological holdout of 12 months. The selected model for each target is the model with the lowest holdout RMSE.

## Model evaluation

| Target | Model | MAE | RMSE | MAPE (%) |
|---|---|---:|---:|---:|
| Transaction volume (million transactions) | Holt-Winters (additive trend + seasonality) | 465.22 | 528.48 | 2.08% |
| Transaction value (₹ crore) | Holt-Winters (additive trend + seasonality) | 62,168.07 | 69,439.29 | 2.15% |

## Six-month forecast

| Month | Forecast volume (million transactions) | Forecast value (₹ crore) |
|---|---:|---:|
| Oct 2026 | 25,212.18 | 3,219,261.51 |
| Nov 2026 | 24,821.08 | 3,108,598.51 |
| Dec 2026 | 25,921.64 | 3,260,620.19 |
| Jan 2027 | 26,012.05 | 3,278,296.90 |
| Feb 2027 | 25,040.56 | 3,136,604.15 |
| Mar 2027 | 27,339.29 | 3,394,545.84 |

## Interpretation and limitations

- The model selected for each target is based on one chronological holdout window.
- Lower MAE, RMSE, and MAPE indicate lower holdout error; MAPE is a percentage.
- These are monthly aggregate point forecasts, not transaction-level predictions.
- Prediction intervals are not included.
- Historical associations and forecast changes do not establish causal effects.
- NPCI monthly forecasting is kept separate from PhonePe Pulse analytics.

## Charts

- `final_volume_forecast.png`
- `final_value_forecast.png`
