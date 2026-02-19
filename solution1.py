import os
import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# -----------------------------
# Load Data
# -----------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, "formatted_sales_output.csv")

df = pd.read_csv(data_path)

df["Date"] = pd.to_datetime(df["Date"])

PRICE_CHANGE_DATE = pd.Timestamp("2021-01-15")

# -----------------------------
# Create Dash App
# -----------------------------

app = dash.Dash(__name__)

# Get region list
regions = ["All"] + sorted(df["Region"].unique())

# -----------------------------
# Layout
# -----------------------------

app.layout = html.Div([

    html.H1(
        "Soul Foods Pink Morsel Sales Dashboard",
        style={"textAlign": "center"}
    ),

    html.H3(
        "Were sales higher before or after the January 15, 2021 price increase?",
        style={"textAlign": "center"}
    ),

    # Dropdown Filter
    html.Div([
        html.Label("Select Region:"),
        dcc.Dropdown(
            id="region-dropdown",
            options=[{"label": r, "value": r} for r in regions],
            value="All",
            clearable=False
        )
    ], style={"width": "30%", "margin": "auto"}),

    html.Br(),

    # KPI Cards
    html.Div(id="kpi-container", style={
        "display": "flex",
        "justifyContent": "center",
        "gap": "50px"
    }),

    # Graph
    dcc.Graph(id="sales-chart")

])

# -----------------------------
# Callback
# -----------------------------

@app.callback(
    [Output("sales-chart", "figure"),
     Output("kpi-container", "children")],
    [Input("region-dropdown", "value")]
)
def update_dashboard(selected_region):

    filtered_df = df.copy()

    if selected_region != "All":
        filtered_df = filtered_df[filtered_df["Region"] == selected_region]

    # Aggregate daily sales
    daily_sales = filtered_df.groupby("Date")["Sales"].sum().reset_index()
    daily_sales = daily_sales.sort_values("Date")

    # Create chart
    fig = px.line(
        daily_sales,
        x="Date",
        y="Sales",
        title="Daily Pink Morsel Sales"
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Total Sales ($)",
        template="plotly_white"
    )

    # Add price change marker
    fig.add_vline(x=PRICE_CHANGE_DATE, line_dash="dash", line_color="red")

    # -----------------------------
    # Business Analysis Calculation
    # -----------------------------

    before_sales = filtered_df[filtered_df["Date"] < PRICE_CHANGE_DATE]["Sales"].sum()
    after_sales = filtered_df[filtered_df["Date"] >= PRICE_CHANGE_DATE]["Sales"].sum()

    if before_sales == 0:
        pct_change = 0
    else:
        pct_change = ((after_sales - before_sales) / before_sales) * 100

    # KPI Cards
    kpis = [

        html.Div([
            html.H4("Sales Before Price Increase"),
            html.H2(f"${before_sales:,.0f}")
        ], style={"textAlign": "center"}),

        html.Div([
            html.H4("Sales After Price Increase"),
            html.H2(f"${after_sales:,.0f}")
        ], style={"textAlign": "center"}),

        html.Div([
            html.H4("Percentage Change"),
            html.H2(f"{pct_change:.2f}%")
        ], style={"textAlign": "center"})

    ]

    return fig, kpis

# -----------------------------
# Run App
# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)
