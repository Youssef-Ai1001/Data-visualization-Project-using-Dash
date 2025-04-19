# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import os


# Incorporate data
# folder_dir = os.path.join("Y:", os.sep, "Machine Learning", "Work Space_ML", "DataSets")
file_name = "Fifa2018_dataset.csv"
# data_path = os.path.join(folder_dir, file_name)
df = pd.read_csv(file_name)


# Initialize the app - incorporate css
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = Dash(external_stylesheets=external_stylesheets)


# App layout
app.layout = html.Div(
    style={"backgroundColor": "#e6f7ff", "minHeight": "100vh"},
    children=[
        # Title
        html.Div(
            children="FIFA 2018 Data Visualization",
            style={
                "textAlign": "center",
                "color": "#003366",
                "fontSize": "32px",
                "fontWeight": "bold",
                "marginTop": "20px",
                "marginBottom": "20px",
            },
        ),
        html.Hr(),


        # Dropdown to select nationality
        html.Div(
            [
                html.Label("Select Nationality:"),
                dcc.Dropdown(
                    options=[
                        {"label": nat, "value": nat}
                        for nat in sorted(df["Nationality"].unique())
                    ],
                    value="Brazil",
                    id="nationality-dropdown",
                    placeholder="Select a nationality",
                ),
            ],
            style={"width": "40%", "display": "inline-block", "padding": "10px"},
        ),


        # Radio buttons to choose skill
        html.Div(
            [
                html.Label("Choose Skill to Visualize:"),
                dcc.RadioItems(
                    options=["Ball control", "Dribbling", "Finishing"],
                    value="Dribbling",
                    inline=True,
                    id="skill-radio",
                ),
            ],
            style={"padding": "10px"},
        ),


        # Graph: Top 10 players in selected skill
        html.Div(
            [dcc.Graph(id="top-players-graph")]),

        # Graph: Pie chart of preferred positions
        html.Div([dcc.Graph(id="position-pie-chart")]),

        # Table: Show players from selected nationality
        html.Div(
            [
                html.H3("Players Table"),
                dash_table.DataTable(
                    id="players-table",
                    page_size=10,
                    style_table={"overflowX": "auto"},
                    style_cell={"textAlign": "left", "padding": "5px"},
                    style_header={"backgroundColor": "lightgrey", "fontWeight": "bold"},
                ),
            ]
        ),


        # Extra chart + DataTable visualization
        html.Div(
            [
                html.Hr(),
                html.Div(
                    [
                        dcc.RadioItems(
                            options=[
                                {"label": "Ball control", "value": "Ball control"},
                                {"label": "Dribbling", "value": "Dribbling"},
                                {"label": "Finishing", "value": "Finishing"},
                            ],
                            value="Dribbling",
                            inline=True,
                            id="my-radio-buttons-final",
                            style={"textAlign": "center", "marginBottom": "30px"},
                        )
                    ]
                ),


                # DataTable and Graph in two columns
                html.Div(
                    style={
                        "display": "flex",
                        "justifyContent": "space-around",
                        "gap": "20px",
                    },
                    children=[
                        html.Div(
                            style={"flex": "1", "maxWidth": "48%"},
                            children=[
                                dash_table.DataTable(
                                    data=df.to_dict("records"),
                                    page_size=11,
                                    style_table={"overflowX": "auto"},
                                    style_cell={"textAlign": "left", "padding": "5px"},
                                    style_header={
                                        "backgroundColor": "#f0f0f0",
                                        "fontWeight": "bold",
                                    },
                                )
                            ],
                        ),


                        # Graph
                        html.Div(
                            style={"flex": "1", "maxWidth": "48%"},
                            children=[dcc.Graph(figure={}, id="histo-chart-final")],
                        ),
                    ],
                ),
            ]
        ),
    ]
)


# Callbacks to update table and charts based on nationality and skill
@app.callback(
    [
        Output("players-table", "data"),
        Output("top-players-graph", "figure"),
        Output("position-pie-chart", "figure"),
    ],
    [Input("nationality-dropdown", "value"), Input("skill-radio", "value")],
)
def update_main_dashboard(selected_nat, selected_skill):
    filtered_df = df[df["Nationality"] == selected_nat]

    table_data = filtered_df[
        ["Name", "Club", "Age", "Potential", "Preferred Positions", selected_skill]
    ].to_dict("records")

    top_players = filtered_df.sort_values(by=selected_skill, ascending=False).head(10)
    bar_fig = px.bar(
        top_players,
        x="Name",
        y=selected_skill,
        color="Club",
        title=f"Top 10 Players by {selected_skill} in {selected_nat}",
    )

    pie_fig = px.pie(
        filtered_df, names="Preferred Positions", title=f"Position Distribution - {selected_nat}"
    )

    return table_data, bar_fig, pie_fig


@app.callback(
    Output("histo-chart-final", "figure"), Input("my-radio-buttons-final", "value")
)
def update_histogram(col_chosen):
    fig = px.histogram(
        df,
        x="Name",
        y=col_chosen,
        histfunc="avg",
        title=f"Average {col_chosen} per Player",
    )
    return fig


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
