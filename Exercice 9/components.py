from dash import dcc, html
import dash_bootstrap_components as dbc
import styles as s

def create_card_header(title):
    return dbc.CardHeader(title, style=s.HEADER_STYLE)

def stock_segment_card(id_graph, title, badge_text):
    return dbc.Card([
        create_card_header(title),
        dbc.CardBody([dcc.Graph(id=id_graph, style={'height': '300px'})]),
        dbc.CardFooter([dbc.Badge(badge_text, color="dark")])
    ], style={'backgroundColor': s.DARK_BG, 'color': 'white', **s.CARD_STYLE})