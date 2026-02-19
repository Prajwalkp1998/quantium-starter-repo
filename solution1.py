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

# -----------------------------
# Layout with Styling
# -----------------------------

app.layout = html.Div(

    style={
        "fontFamily": "Arial",
        "backgroundColor": "#f4f6f8",
        "padding": "30px"
    },

    children=[

        html.H1(
            "Soul Foods Pink Morsel Sales Visualiser",
            style={
                "textAlign": "center",
                "color": "#2c3e50"
            }
        ),

        html.H3(
            "Were sales higher before or after the January 15, 2021 price increase?",
            style={"textAlign": "center", "color": "#555"}
        ),

        # -----------------------------
        # Radio Button Filter
        # -----------------------------

        html.Div([

            html.Label(
                "Filter by Region:",
                style={"fontWeight": "bold"}
            ),

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
                labelStyle={"margin-right": "20px"}
            )

        ],
        style={
            "textAlign": "center",
            "marginTop": "20px",
            "marginBottom": "20px"
        }),

        # Chart Container
        html.Div(
            dcc.Graph(id="sales-chart"),
            style={
                "backgroundColor": "white",
                "padding": "20px",
                "borderRadius": "10px",
                "boxShadow": "0px 4px 10px rgba(0,0,0,0.1)"
            }
        )

    ]
)

# -----------------------------
# Callback
# -----------------------------

@app.callback(
    Output("sales-chart", "figure"),
    Input("region-radio", "value")
)
def update_chart(selected_region):

    filtered_df = df.copy()

    if selected_region != "all":
        filtered_df = filtered_df[filtered_df["Region"] == selected_region]

    daily_sales = (
        filtered_df.groupby("Date")["Sales"]
        .sum()
        .reset_index()
        .sort_values("Date")
    )

    fig = px.line(
        daily_sales,
        x="Date",
        y="Sales",
        title="Daily Pink Morsel Sales"
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_title="Date",
        yaxis_title="Total Sales ($)"
    )

    # Price increase marker
    fig.add_vline(
        x=PRICE_CHANGE_DATE,
        line_dash="dash",
        line_color="red"
    )

    return fig

# -----------------------------
# Run App
# -----------------------------

if __name__ == "__main__":
    app.run(debug=True)
