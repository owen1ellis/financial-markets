import plotly.express as px
import numpy as np
import pandas as pd

# Generate random data
np.random.seed(42)
n_points = 30
sentiment_shift = np.random.uniform(-0.8, 0.8, n_points)
earnings_surprise = np.random.uniform(-1.5, 1.5, n_points)

df = pd.DataFrame({"Sentiment Shift": sentiment_shift, "Earnings Surprise": earnings_surprise})

# Create scatter plot
fig_cor = px.scatter(
    df, x="Sentiment Shift", y="Earnings Surprise",
    title="Sentiment Shift vs Earnings Surprise (Year-Month based)",
    labels={"Sentiment Shift": "Sentiment Shift", "Earnings Surprise": "Earnings Surprise"},
    template="plotly_white"
)
fig_cor.update_layout(height=500, width=700)
fig_cor.add_hline(y=0, line_dash="dot", line_color="black")
fig_cor.add_vline(x=0, line_dash="dot", line_color="black")
# fig_cor.show()