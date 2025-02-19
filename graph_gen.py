import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
from math import ceil, floor
import random

# Generate Fake Data
def generate_fake_sentiment_data(num_days=20, num_isins=40, num_rows=1000):
    dates = [datetime.today().date() - timedelta(days=i) for i in range(num_days)]
    isin_prefix = "US"
    isin_numbers = [f"{isin_prefix}{str(i).zfill(10)}" for i in range(num_isins)]
    date_choices = np.random.choice(dates, num_rows)
    isin_choices = np.random.choice(isin_numbers, num_rows)
    sentiment_values = np.clip(np.random.normal(loc=0.5, scale=0.15, size=num_rows), 0, 1)
    df = pd.DataFrame({
        "date": date_choices,
        "isin": isin_choices,
        "sentiment_value": sentiment_values
    })
    return df

df = generate_fake_sentiment_data()

random_isin = np.random.choice(df["isin"].unique())
given_isin="US0000000001"
rows = []
for i, day in enumerate(range(19, -1, -1)):
    num_reports = random.randint(floor(0+i*0.15), ceil(2+i*0.25))
    date = datetime.today().date() - timedelta(days=day)
    for i in range(num_reports):
        sent_score = np.clip(np.random.normal(loc=0.5, scale=0.05), 0, 1) * (1+(i+1)*0.045)
        rows.append(
            {"date": date, "isin": given_isin, "sentiment_value": sent_score}
        )
df_isin = pd.DataFrame(rows)
print(df_isin.head())

# Filter for selected ISIN and all others
# df_isin = df[df["isin"] == random_isin]
df_others = df[df["isin"] != random_isin]

df_aggregated_date_isin = df.groupby(["date", "isin"]).agg(
    max_sentiment=("sentiment_value", "max"),
    min_sentiment=("sentiment_value", "min"),
    avg_sentiment=("sentiment_value", "mean"),
    count=("sentiment_value", "count"),
).reset_index()

others_grouped = df_aggregated_date_isin.groupby("date").agg(
    total_reports=("count", "mean"),
    avg_avg_sentiment=("avg_sentiment", "mean"),
    avg_top_sentiment=("max_sentiment", "max"),
    avg_bottom_sentiment=("min_sentiment", "min")  # Bottom 10% avg
).reset_index()

isin_grouped = df_isin.groupby("date").agg(
    total_reports=("sentiment_value", "count"),
    avg_avg_sentiment=("sentiment_value", "mean"),
    avg_top_sentiment=("sentiment_value", "max"),
    avg_bottom_sentiment=("sentiment_value", "min")  # Bottom 10% avg
).reset_index()

fig = go.Figure()

fig.add_trace(go.Bar(
    x=others_grouped["date"],
    y=others_grouped["total_reports"],
    name="Avg Number Of Reports per SNP500 Company",
    marker_color="blue",
    opacity=0.6
))

fig.add_trace(go.Bar(
    x=others_grouped["date"],
    y=isin_grouped["total_reports"],
    name="Number of Reports for given ISIN",
    marker_color="red",
    opacity=0.6
))

fig.update_layout(
    title="Grouped Bar Chart Example",
    xaxis_title="Date",
    yaxis_title="Total Reports",
    barmode="group",
    template="plotly_white"
)

fig.add_trace(go.Scatter(
    x=isin_grouped["date"], y=isin_grouped["avg_avg_sentiment"],
    mode="lines", name="Avg Sentiment (Selected ISIN)", line=dict(color="red"),
    yaxis="y2"
))
fig.add_trace(go.Scatter(
    x=others_grouped["date"], y=others_grouped["avg_avg_sentiment"],
    mode="lines", name="Avg Sentiment (Others)", line=dict(color="blue"),
    yaxis="y2"
))

fig.update_layout(
    title=f"Sentiment Analysis for {random_isin}",
    xaxis_title="Date",
    yaxis=dict(
        title="Number of Reports",
        side="left",
        showgrid=False
    ),
    yaxis2=dict(
        title="Sentiment Score",
        overlaying="y",
        side="right",
        showgrid=False
    ),
    barmode="group",
    template="plotly_white"
)