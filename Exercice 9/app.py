from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import styles as s
import components as c
from callbacks import register_callbacks
from data import get_stocks_data, METRICS_MAP

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
df_stocks = get_stocks_data()

app.layout = dbc.Container([
    html.H2("DASHBOARD ANALYTIQUE", className="text-center my-4", style={'color': s.BLUE_PRIMARY}),
    dbc.Tabs([
        dbc.Tab(label="Séries Temporelles", tab_id="tab-stocks"),
        dbc.Tab(label="Indicateurs mondiaux", tab_id="tab-gapminder"),
    ], id="tabs-navigation", active_tab="tab-stocks", className="mb-4"),
    html.Div(id="tab-display")
], fluid=True, style={'backgroundColor': s.LIGHT_GRAY, 'minHeight': '100vh'})

@app.callback(Output("tab-display", "children"), Input("tabs-navigation", "active_tab"))
def render_content(active_tab):
    if active_tab == "tab-stocks":
        return html.Div([
            dbc.Card([
                c.create_card_header("Configuration de la période"),
                dbc.CardBody([
                    dcc.DatePickerRange(
                        id='stk-date-picker',
                        min_date_allowed=df_stocks['date'].min(),
                        max_date_allowed=df_stocks['date'].max(),
                        start_date='2018-05-01', end_date='2019-02-01', display_format='DD-MMM-YYYY'
                    )
                ]),
                dbc.CardFooter([dbc.Badge(id='stk-badge-start', color="primary", className="me-2"), dbc.Badge(id='stk-badge-end', color="info")])
            ], className="mb-4 shadow"),
            dbc.Row([
                dbc.Col([c.stock_segment_card('stk-graph-before', "Avant début", "Jan - Mai 2018")], width=4),
                dbc.Col([c.stock_segment_card('stk-graph-during', "Dans la Plage", "Mai 2018 - Fév 2019")], width=4),
                dbc.Col([c.stock_segment_card('stk-graph-after', "Après fin", "Fév - Déc 2019")], width=4),
            ], className="g-4")
        ])
    elif active_tab == "tab-gapminder":
        return dbc.Row([
            dbc.Col([
                dbc.Card([
                    c.create_card_header("Filtres"),
                    dbc.CardBody([
                        html.Label("Choisir une mesure :", className="fw-bold mb-2"),
                        dcc.Dropdown(id='gap-dropdown', options=[{'label': k, 'value': k} for k in METRICS_MAP.keys()], value='Population', clearable=False),
                    ])
                ])
            ], width=3),
            dbc.Col([
                dbc.Card([
                    c.create_card_header("Visualisation Gapminder"),
                    dbc.CardBody([dcc.Graph(id='gap-main-graph')], style=s.DARK_CARD_BODY)
                ])
            ], width=9)
        ])

register_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True)