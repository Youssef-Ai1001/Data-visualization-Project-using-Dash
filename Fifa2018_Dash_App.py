# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input, State
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Incorporate data
file_name = "Fifa2018_dataset.csv"
df = pd.read_csv(file_name)

# Convert skill columns to numeric preemptively
skill_columns = [
    "Ball control",
    "Dribbling",
    "Finishing",
    "Acceleration",
    "Aggression",
    "Agility",
    "Balance",
    "Composure",
    "Strength",
    "Stamina",
]

for col in skill_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Convert age, potential, and overall rating to numeric
numeric_columns = ["Age", "Potential", "Overall"]
for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Initialize the app
app = Dash(__name__, suppress_callback_exceptions=True)

# Define color scheme
colors = {
    "background": "#5cadff",
    "text": "#2c3e50",
    "primary": "#3498db",
    "secondary": "#2ecc71",
    "accent": "#e74c3c",
    "light": "#ecf0f1",
}

# App layout
app.layout = html.Div(
    style={
        "backgroundColor": colors["background"],
        "minHeight": "100vh",
        "fontFamily": "'Segoe UI', 'Roboto', sans-serif",
        "padding": "20px",
    },
    children=[
        # Header section
        html.Div(
            style={
                "backgroundColor": colors["primary"],
                "padding": "20px",
                "borderRadius": "10px",
                "marginBottom": "20px",
                "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
            },
            children=[
                html.H1(
                    "FIFA 2018 Interactive Dashboard",
                    style={
                        "textAlign": "center",
                        "color": "white",
                        "marginBottom": "10px",
                    },
                ),
                html.P(
                    "Explore player statistics, skills, and positions by nationality",
                    style={
                        "textAlign": "center",
                        "color": "white",
                        "fontSize": "18px",
                    },
                ),
            ],
        ),
        # Control section
        html.Div(
            style={
                "backgroundColor": "white",
                "padding": "20px",
                "borderRadius": "10px",
                "marginBottom": "20px",
                "boxShadow": "0 2px 4px rgba(0, 0, 0, 0.05)",
                "display": "flex",
                "justifyContent": "space-between",
                "alignItems": "center",
                "flexWrap": "wrap",
            },
            children=[
                # Dropdown to select nationality
                html.Div(
                    [
                        html.Label(
                            "Select Nationality:",
                            style={"fontWeight": "bold", "marginBottom": "8px"},
                        ),
                        dcc.Dropdown(
                            options=[
                                {"label": nat, "value": nat}
                                for nat in sorted(df["Nationality"].unique())
                            ],
                            value="Brazil",
                            id="nationality-dropdown",
                            placeholder="Select a nationality",
                            style={"width": "300px"},
                        ),
                    ],
                    style={"margin": "10px"},
                ),
                # Radio buttons to choose skill
                html.Div(
                    [
                        html.Label(
                            "Choose Skill to Visualize:",
                            style={"fontWeight": "bold", "marginBottom": "8px"},
                        ),
                        dcc.RadioItems(
                            options=[
                                {"label": " Ball Control", "value": "Ball control"},
                                {"label": " Dribbling", "value": "Dribbling"},
                                {"label": " Finishing", "value": "Finishing"},
                                {"label": " Acceleration", "value": "Acceleration"},
                                {"label": " Aggression", "value": "Aggression"},
                            ],
                            value="Dribbling",
                            inline=True,
                            id="skill-radio",
                            labelStyle={
                                "marginRight": "20px",
                                "cursor": "pointer",
                                "padding": "5px 10px",
                            },
                        ),
                    ],
                    style={"margin": "10px"},
                ),
                # Radio buttons for club metric (added for club-performance-chart)
                html.Div(
                    [
                        html.Label(
                            "Choose Club Metric:",
                            style={"fontWeight": "bold", "marginBottom": "8px"},
                        ),
                        dcc.RadioItems(
                            options=[
                                {"label": " Overall Rating", "value": "Overall"},
                                {"label": " Potential", "value": "Potential"},
                                {"label": " Age", "value": "Age"},
                            ],
                            value="Overall",
                            inline=True,
                            id="club-metric-radio",
                            labelStyle={
                                "marginRight": "20px",
                                "cursor": "pointer",
                                "padding": "5px 10px",
                            },
                        ),
                    ],
                    style={"margin": "10px"},
                ),
            ],
        ),
        # Main content section - 2 columns
        html.Div(
            style={
                "display": "flex",
                "flexWrap": "wrap",
                "justifyContent": "space-between",
                "gap": "20px",
            },
            children=[
                # Left column
                html.Div(
                    style={
                        "flex": "1",
                        "minWidth": "400px",
                        "backgroundColor": "white",
                        "padding": "20px",
                        "borderRadius": "10px",
                        "boxShadow": "0 2px 4px rgba(0, 0, 0, 0.05)",
                    },
                    children=[
                        html.H3(
                            "Top Players by Skill Rating",
                            style={"color": colors["text"], "marginBottom": "15px"},
                        ),
                        dcc.Graph(id="top-players-graph"),
                    ],
                ),
                # Right column
                html.Div(
                    style={
                        "flex": "1",
                        "minWidth": "400px",
                        "backgroundColor": "white",
                        "padding": "20px",
                        "borderRadius": "10px",
                        "boxShadow": "0 2px 4px rgba(0, 0, 0, 0.05)",
                    },
                    children=[
                        html.H3(
                            "Position Distribution",
                            style={"color": colors["text"], "marginBottom": "15px"},
                        ),
                        dcc.Graph(id="position-pie-chart"),
                    ],
                ),
            ],
        ),
        # Age Distribution & Potential Section
        html.Div(
            style={
                "display": "flex",
                "flexWrap": "wrap",
                "justifyContent": "space-between",
                "gap": "20px",
                "marginTop": "20px",
            },
            children=[
                # Age Distribution
                html.Div(
                    style={
                        "flex": "1",
                        "minWidth": "400px",
                        "backgroundColor": "white",
                        "padding": "20px",
                        "borderRadius": "10px",
                        "boxShadow": "0 2px 4px rgba(0, 0, 0, 0.05)",
                    },
                    children=[
                        html.H3(
                            "Age Distribution by Nationality",
                            style={"color": colors["text"], "marginBottom": "15px"},
                        ),
                        dcc.Graph(id="age-distribution"),
                    ],
                ),
                # Potential vs Age
                html.Div(
                    style={
                        "flex": "1",
                        "minWidth": "400px",
                        "backgroundColor": "white",
                        "padding": "20px",
                        "borderRadius": "10px",
                        "boxShadow": "0 2px 4px rgba(0, 0, 0, 0.05)",
                    },
                    children=[
                        html.H3(
                            "Potential vs Age Analysis",
                            style={"color": colors["text"], "marginBottom": "15px"},
                        ),
                        dcc.Graph(id="potential-vs-age"),
                    ],
                ),
            ],
        ),
        # Skill Comparison Radar Chart Section
        html.Div(
            style={
                "backgroundColor": "white",
                "padding": "20px",
                "borderRadius": "10px",
                "marginTop": "20px",
                "boxShadow": "0 2px 4px rgba(0, 0, 0, 0.05)",
            },
            children=[
                html.H3(
                    "Player Skill Comparison",
                    style={"color": colors["text"], "marginBottom": "15px"},
                ),
                html.Div(
                    style={
                        "display": "flex",
                        "justifyContent": "space-between",
                        "flexWrap": "wrap",
                        "gap": "20px",
                        "marginBottom": "20px",
                    },
                    children=[
                        html.Div(
                            style={"flex": "1", "minWidth": "300px"},
                            children=[
                                html.Label(
                                    "Select Player 1:",
                                    style={
                                        "fontWeight": "bold",
                                        "marginBottom": "8px",
                                        "display": "block",
                                    },
                                ),
                                dcc.Dropdown(
                                    id="player1-dropdown",
                                    placeholder="Select player",
                                ),
                            ],
                        ),
                        html.Div(
                            style={"flex": "1", "minWidth": "300px"},
                            children=[
                                html.Label(
                                    "Select Player 2:",
                                    style={
                                        "fontWeight": "bold",
                                        "marginBottom": "8px",
                                        "display": "block",
                                    },
                                ),
                                dcc.Dropdown(
                                    id="player2-dropdown",
                                    placeholder="Select player",
                                ),
                            ],
                        ),
                    ],
                ),
                dcc.Graph(id="radar-chart"),
            ],
        ),
        # Players table section
        html.Div(
            style={
                "backgroundColor": "white",
                "padding": "20px",
                "borderRadius": "10px",
                "marginTop": "20px",
                "boxShadow": "0 2px 4px rgba(0, 0, 0, 0.05)",
            },
            children=[
                html.H3(
                    "Players Data",
                    style={"color": colors["text"], "marginBottom": "15px"},
                ),
                dash_table.DataTable(
                    id="players-table",
                    page_size=10,
                    style_table={"overflowX": "auto"},
                    style_cell={
                        "textAlign": "left",
                        "padding": "12px 15px",
                        "fontFamily": "'Segoe UI', 'Roboto', sans-serif",
                    },
                    style_header={
                        "backgroundColor": colors["light"],
                        "fontWeight": "bold",
                        "color": colors["text"],
                        "borderBottom": "2px solid #ddd",
                    },
                    style_data_conditional=[
                        {
                            "if": {"row_index": "odd"},
                            "backgroundColor": "rgb(248, 248, 248)",
                        }
                    ],
                ),
            ],
        ),
        # Skill Correlation Heatmap
        html.Div(
            style={
                "backgroundColor": "white",
                "padding": "20px",
                "borderRadius": "10px",
                "marginTop": "20px",
                "boxShadow": "0 2px 4px rgba(0, 0, 0, 0.05)",
            },
            children=[
                html.H3(
                    "Skill Correlation Analysis",
                    style={"color": colors["text"], "marginBottom": "15px"},
                ),
                html.P(
                    "This heatmap shows correlations between different player skills, helping identify which skills tend to develop together.",
                    style={"marginBottom": "15px"},
                ),
                dcc.Graph(id="correlation-heatmap"),
            ],
        ),
        # Footer
        html.Div(
            style={
                "textAlign": "center",
                "padding": "20px",
                "marginTop": "20px",
                "color": colors["text"],
            },
            children=[
                html.P(
                    "FIFA 2018 Data Analysis Dashboard • Created with Dash and Plotly"
                ),
                html.P("© Youssef Taha Badawi — Made with ❤️ in 2025"),
            ],
        ),
    ],
)


# Callbacks to update table and charts based on nationality and skill
@callback(
    [
        Output("players-table", "data"),
        Output("top-players-graph", "figure"),
        Output("position-pie-chart", "figure"),
        Output("player1-dropdown", "options"),
        Output("player2-dropdown", "options"),
        Output("player1-dropdown", "value"),
        Output("player2-dropdown", "value"),
        Output("age-distribution", "figure"),
        Output("potential-vs-age", "figure"),
        Output("correlation-heatmap", "figure"),
    ],
    [Input("nationality-dropdown", "value"), Input("skill-radio", "value")],
)
def update_main_dashboard(selected_nat, selected_skill):
    # Filter data by nationality
    filtered_df = df[df["Nationality"] == selected_nat].copy()

    # Ensure skill column is numeric
    filtered_df[selected_skill] = pd.to_numeric(
        filtered_df[selected_skill], errors="coerce"
    )

    # Prepare table data
    table_columns = [
        "Name",
        "Club",
        "Overall",
        "Age",
        "Potential",
        "Preferred Positions",
        selected_skill,
    ]
    table_data = (
        filtered_df[table_columns]
        .sort_values(by=selected_skill, ascending=False)
        .to_dict("records")
    )

    # Prepare bar chart for top players
    top_players = filtered_df.sort_values(by=selected_skill, ascending=False).head(10)

    bar_fig = px.bar(
        top_players,
        x="Name",
        y=selected_skill,
        color="Club",
        title=f"Top 10 Players by {selected_skill} in {selected_nat}",
        color_discrete_sequence=px.colors.qualitative.Set3,
    )

    bar_fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=20, r=20, t=60, b=20),
        xaxis=dict(
            title="Player Name",
            tickangle=-45,
            tickfont=dict(size=10),
        ),
        yaxis=dict(title=f"{selected_skill} Rating"),
        legend_title="Club",
        height=450,
    )

    # Prepare pie chart for positions
    positions = []
    for pos in (
        filtered_df["Preferred Positions"].fillna("Unknown").astype(str).str.split(" ")
    ):
        if isinstance(pos, list):
            positions.extend(pos)
        else:
            positions.append(pos)

    position_counts = pd.Series(positions).value_counts().reset_index()
    position_counts.columns = ["Position", "Count"]

    pie_fig = px.pie(
        position_counts,
        names="Position",
        values="Count",
        title=f"Position Distribution - {selected_nat}",
        color_discrete_sequence=px.colors.qualitative.Bold,
        hole=0.3,
    )

    pie_fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=20, r=20, t=60, b=20),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5,
        ),
        height=450,
    )

    pie_fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        insidetextfont=dict(color="white"),
        hoverinfo="label+percent+value",
        marker=dict(line=dict(color="white", width=2)),
    )

    # Player dropdown options
    player_options = [
        {"label": name, "value": name} for name in filtered_df["Name"].sort_values()
    ]

    # Set default values for player dropdowns
    player1_default = filtered_df["Name"].iloc[0] if not filtered_df.empty else None
    player2_default = filtered_df["Name"].iloc[1] if len(filtered_df) > 1 else None

    # Age distribution histogram
    age_fig = px.histogram(
        filtered_df,
        x="Age",
        color="Preferred Positions",
        title=f"Age Distribution - {selected_nat}",
        opacity=0.7,
        marginal="box",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        nbins=25,
    )

    age_fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=20, r=20, t=60, b=20),
        xaxis=dict(title="Age"),
        yaxis=dict(title="Count"),
        legend_title="Position",
        height=450,
    )

    # Potential vs Age scatter plot
    potential_age_fig = px.scatter(
        filtered_df,
        x="Age",
        y="Potential",
        color="Overall",
        size="Overall",
        hover_name="Name",
        hover_data=["Club", "Preferred Positions"],
        title=f"Potential vs Age - {selected_nat}",
        color_continuous_scale="Viridis",
    )

    potential_age_fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=20, r=20, t=60, b=20),
        xaxis=dict(title="Age"),
        yaxis=dict(title="Potential Rating"),
        height=450,
    )

    # Correlation heatmap
    corr_columns = [
        "Overall",
        "Potential",
        "Ball control",
        "Dribbling",
        "Finishing",
        "Acceleration",
        "Aggression",
        "Agility",
        "Balance",
        "Composure",
        "Strength",
    ]

    # Filter out columns not in the dataframe
    available_columns = [col for col in corr_columns if col in filtered_df.columns]

    # Create correlation matrix
    corr_matrix = filtered_df[available_columns].corr()

    # Create heatmap
    heatmap_fig = go.Figure(
        data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale="YlGnBu",
            colorbar=dict(title="Correlation"),
            hovertemplate="%{y} vs %{x}<br>Correlation: %{z:.2f}<extra></extra>",
        )
    )

    heatmap_fig.update_layout(
        title=f"Skill Correlation Heatmap - {selected_nat}",
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=20, r=20, t=60, b=20),
        height=600,
    )

    return (
        table_data,
        bar_fig,
        pie_fig,
        player_options,
        player_options,
        player1_default,
        player2_default,
        age_fig,
        potential_age_fig,
        heatmap_fig,
    )


@callback(
    Output("overall-skill-chart", "figure"),
    Input("overall-skill-radio", "value"),
)
def update_overall_chart(selected_skill):
    # Convert skill column to numeric, forcing errors to NaN
    df[selected_skill] = pd.to_numeric(df[selected_skill], errors="coerce")

    # Group by nationality and calculate average skill
    skill_by_nation = (
        df.groupby("Nationality")[selected_skill]
        .mean()
        .sort_values(ascending=False)
        .head(15)
        .reset_index()
    )

    fig = px.bar(
        skill_by_nation,
        x="Nationality",
        y=selected_skill,
        color=selected_skill,
        color_continuous_scale="Viridis",
        title=f"Top 15 Nations by Average {selected_skill} Rating",
    )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=20, r=20, t=60, b=20),
        xaxis=dict(
            title="Nationality",
            tickangle=-45,
        ),
        yaxis=dict(title=f"Average {selected_skill} Rating"),
        coloraxis_showscale=True,
        height=450,
    )

    return fig


@callback(
    Output("radar-chart", "figure"),
    [
        Input("player1-dropdown", "value"),
        Input("player2-dropdown", "value"),
        Input("nationality-dropdown", "value"),
    ],
)
def update_radar_chart(player1, player2, nationality):
    if not player1 or not player2:
        # Return empty figure if players not selected
        return go.Figure()

    # Filter data for the selected players
    filtered_df = df[df["Nationality"] == nationality]
    player1_data = filtered_df[filtered_df["Name"] == player1]
    player2_data = filtered_df[filtered_df["Name"] == player2]

    if player1_data.empty or player2_data.empty:
        return go.Figure()

    # Skills to compare
    skills = [
        "Ball control",
        "Dribbling",
        "Finishing",
        "Acceleration",
        "Aggression",
        "Agility",
        "Balance",
        "Composure",
        "Strength",
        "Stamina",
    ]

    # Filter skills that exist in the dataframe
    available_skills = [skill for skill in skills if skill in filtered_df.columns]

    # Extract values for each player
    player1_values = player1_data[available_skills].iloc[0].values.tolist()
    player2_values = player2_data[available_skills].iloc[0].values.tolist()

    # Create radar chart
    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=player1_values, theta=available_skills, fill="toself", name=player1
        )
    )

    fig.add_trace(
        go.Scatterpolar(
            r=player2_values, theta=available_skills, fill="toself", name=player2
        )
    )

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        title=f"Skill Comparison: {player1} vs {player2}",
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=40, r=40, t=60, b=40),
        height=500,
    )

    return fig


@callback(
    Output("club-performance-chart", "figure"),
    [Input("club-metric-radio", "value"), Input("nationality-dropdown", "value")],
)
def update_club_chart(selected_metric, nationality):
    # Filter data by nationality
    filtered_df = df[df["Nationality"] == nationality].copy()

    # Group by club and calculate average for the selected metric
    club_stats = (
        filtered_df.groupby("Club")[selected_metric]
        .agg(["mean", "count"])
        .reset_index()
    )

    # Sort by mean value and filter for clubs with at least 2 players
    club_stats = (
        club_stats[club_stats["count"] >= 2]
        .sort_values(by="mean", ascending=False)
        .head(10)
    )

    fig = px.bar(
        club_stats,
        x="Club",
        y="mean",
        color="mean",
        color_continuous_scale="Bluered",
        title=f"Top 10 Clubs by Average {selected_metric} - {nationality} Players",
        text="count",
    )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=20, r=20, t=60, b=20),
        xaxis=dict(
            title="Club",
            tickangle=-45,
        ),
        yaxis=dict(title=f"Average {selected_metric}"),
        coloraxis_showscale=True,
        height=450,
    )

    # Add text about number of players
    fig.update_traces(
        texttemplate="%{text} players",
        textposition="outside",
    )

    return fig


# Run the app
if __name__ == "__main__":
    app.run(debug=True, port=8051)
