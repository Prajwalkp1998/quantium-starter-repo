import os
import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go

# -----------------------------
# Load Data
# -----------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, "formatted_sales_output.csv")

df = pd.read_csv(data_path)
df["Date"] = pd.to_datetime(df["Date"])

PRICE_CHANGE_DATE = pd.Timestamp("2021-01-15")

# -----------------------------
# Create App
# -----------------------------

app = dash.Dash(__name__)
app.title = "Soul Foods Sales Dashboard"

# -----------------------------
# Layout
# -----------------------------

app.layout = html.Div(style={
    "fontFamily": "Segoe UI",
    "backgroundColor": "#f0f2f5",
    "padding": "40px"
}, children=[

    html.H1(
        "Soul Foods Pink Morsel Performance Dashboard",
        style={"textAlign": "center", "color": "#2c3e50"}
    ),

    html.P(
        "Business Question: Were sales higher before or after the January 15, 2021 price increase?",
        style={"textAlign": "center", "color": "#555"}
    ),

    html.Br(),

    # -----------------------------
    # Region Filter
    # -----------------------------

    html.Div([
        html.Label("Select Region:", style={"fontWeight": "bold"}),
        dcc.RadioItems(
            id="region-radio",
            options=[
                {"label": "All", "value": "all"},
                {"label": "North", "value": "north"},
                {"label": "East", "value": "east"},
                {"label": "South", "value": "south"},
                {"label": "West", "value": "west"},
            ],
            value="all",
            inline=True,
            labelStyle={"marginRight": "20px"}
        )
    ], style={"textAlign": "center"}),

    html.Br(),

    # -----------------------------
    # KPI Cards Container
    # -----------------------------

    html.Div(id="kpi-container", style={
        "display": "flex",
        "justifyContent": "space-around",
        "marginBottom": "40px"
    }),

    # -----------------------------
    # Chart
    # -----------------------------

    html.Div([
        dcc.Graph(id="sales-chart")
    ], style={
        "backgroundColor": "white",
        "padding": "25px",
        "borderRadius": "12px",
        "boxShadow": "0px 6px 18px rgba(0,0,0,0.1)"
    })

])

# -----------------------------
# Callback
# -----------------------------

@app.callback(
    [Output("sales-chart", "figure"),
     Output("kpi-container", "children")],
    Input("region-radio", "value")
)
def update_dashboard(selected_region):

    filtered_df = df.copy()

    if selected_region != "all":
        filtered_df = filtered_df[filtered_df["Region"] == selected_region]

    daily_sales = (
        filtered_df.groupby("Date")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Date")
    )

    # -----------------------------
    # Calculate Business Metrics
    # -----------------------------

    before_sales = filtered_df[filtered_df["Date"] < PRICE_CHANGE_DATE]["Sales"].sum()
    after_sales = filtered_df[filtered_df["Date"] >= PRICE_CHANGE_DATE]["Sales"].sum()

    pct_change = 0
    if before_sales != 0:
        pct_change = ((after_sales - before_sales) / before_sales) * 100

    color = "green" if pct_change >= 0 else "red"

    # -----------------------------
    # Create Chart
    # -----------------------------

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=daily_sales["Date"],
        y=daily_sales["Sales"],
        mode="lines",
        name="Daily Sales",
        line=dict(width=3)
    ))

    # Price change line
    fig.add_vline(
        x=PRICE_CHANGE_DATE,
        line_dash="dash",
        line_color="red"
    )

    # Shaded areas
    fig.add_vrect(
        x0=daily_sales["Date"].min(),
        x1=PRICE_CHANGE_DATE,
        fillcolor="green",
        opacity=0.05,
        layer="below",
        line_width=0,
    )

    fig.add_vrect(
        x0=PRICE_CHANGE_DATE,
        x1=daily_sales["Date"].max(),
        fillcolor="red",
        opacity=0.05,
        layer="below",
        line_width=0,
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_title="Date",
        yaxis_title="Total Sales ($)",
        margin=dict(l=40, r=40, t=40, b=40)
    )

    # -----------------------------
    # KPI Cards
    # -----------------------------

    kpis = [

        html.Div([
            html.H4("Sales Before Price Increase"),
            html.H2(f"${before_sales:,.0f}")
        ], style=card_style()),

        html.Div([
            html.H4("Sales After Price Increase"),
            html.H2(f"${after_sales:,.0f}")
        ], style=card_style()),

        html.Div([
            html.H4("Percentage Change"),
            html.H2(f"{pct_change:.2f}%", style={"color": color})
        ], style=card_style())
    ]

    return fig, kpis


# -----------------------------
# Card Styling Function
# -----------------------------

def card_style():
    return {
        "backgroundColor": "white",
        "padding": "20px",
        "borderRadius": "10px",
        "boxShadow": "0px 4px 12px rgba(0,0,0,0.08)",
        "textAlign": "center",
        "width": "28%"
    }


# -----------------------------
# Run App
# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)
