import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, callback, dcc, html

# Incorporate data
df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv"
)

# Initialize app with Bootstrap CSS and Viewport Meta Tag for mobile scaling
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0, maximum-scale=1.0",
        }
    ],
)

# App layout with fluid Bootstrap grid
app.layout = dbc.Container(
    [
        html.H2(
            "My First App with Data, Graph, and Controls",
            className="my-3 text-center text-md-start",
        ),
        html.Hr(),
        # Control Section
        dbc.Row([
                dbc.Col(
                    [html.Label(
                            "Select Variable:", className="fw-bold mb-2"
                        ),
                        dcc.RadioItems(
                            options=[
                                {"label": " Population", "value": "pop"},
                                {
                                    "label": " Life Expectancy",
                                    "value": "lifeExp",
                                },
                                {
                                    "label": " GDP Per Capita",
                                    "value": "gdpPercap",
                                },
                            ],
                            value="lifeExp",
                            id="my-final-radio-item-example",
                            inputClassName="me-1",
                            labelClassName="me-3 d-inline-block",),],
                    width=12,), ],
            className="mb-4",
        ),
        # Main Content Grid: Full width on mobile (12), side-by-side on desktop (6 & 6)
        dbc.Row(
            [
                # Data Grid Column
                dbc.Col(
                    [
                        html.H5("Data Table", className="mb-3"),
                        dag.AgGrid(
                            rowData=df.to_dict("records"),
                            columnDefs=[{"field": i} for i in df.columns],
                            defaultColDef={
                                "resizable": True,
                                "sortable": True,
                                "filter": True,
                                "minWidth": 100,
                            },
                            dashGridOptions={
                                "pagination": True,
                                "paginationPageSize": 10,
                                "domLayout": "autoHeight",
                            },
                            style={"width": "100%"},
                        ),
                    ],
                    xs=12,
                    lg=6,
                    className="mb-4 mb-lg-0",
                ),
                # Chart Column
                dbc.Col(
                    [
                        html.H5("Average Metric by Continent", className="mb-3"),
                        dcc.Graph(
                            figure={},
                            id="my-final-graph-example",
                            config={"responsive": True}, ## responsive plotting
                            style={"width": "100%", "minHeight": "350px"},
                        ),
                    ],
                    xs=12,
                    lg=6,
                ),
            ],
            className="g-4",
        ),
    ],
    fluid=True,
    className="px-3 px-md-5 py-3",
)


# Callback for updating graph
@callback(
    Output(
        component_id="my-final-graph-example", component_property="figure"
    ),
    Input(
        component_id="my-final-radio-item-example", component_property="value"
    ),
)
def update_graph(col_chosen):
    fig = px.histogram(df, x="continent", y=col_chosen, histfunc="avg")
    fig.update_layout(
        autosize=True,
        margin=dict(l=20, r=20, t=30, b=30),
        template="plotly_white",
    )
    return fig


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
