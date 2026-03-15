import pandas as pd
from dash import Dash, html, dcc, dash_table, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

# --- 1. DONNÉES ---
df_source = px.data.gapminder()
df_americas = (df_source
    .query("continent == 'Americas'")
    .drop(columns=["continent", "iso_alpha", "iso_num"])
)

# --- 2. LAYOUT ---
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    
    # BLOC 1 : Titre (Bandeau bleu)
    html.Div([
        html.H1("GAPMINDER TABLE APP", 
                style={'color': 'white', 'fontSize': '28px', 'margin': '0', 'fontWeight': 'bold'})
    ], style={
        'backgroundColor': '#007BFF', 'padding': '15px', 'textAlign': 'center', 
        'borderRadius': '5px', 'marginBottom': '20px', 'marginTop': '20px'
    }),

    dbc.Row([
        # BLOC 2 : Colonne GAUCHE (Tableau)
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.P("Select a column from the table to update the line chart", 
                           style={'fontStyle': 'italic', 'fontSize': '14px', 'color': '#666', 'marginBottom': '15px'}),
                    
                    dash_table.DataTable(
                        id='table-interactif',
                        data=df_americas.to_dict('records'),
                        columns=[
                            {"name": i, "id": i, "selectable": (i not in ["country", "year"])} 
                            for i in df_americas.columns
                        ],
                        column_selectable="single",
                        selected_columns=["gdpPercap"],
                        filter_action="native",
                        page_size=12,
                        style_table={'overflowX': 'auto'},
                        style_cell={'textAlign': 'left', 'padding': '8px', 'fontSize': '11px'},
                        style_header={'backgroundColor': '#f2f2f2', 'fontWeight': 'bold'}
                    )
                ])
            ], style={'borderRadius': '5px', 'border': '1px solid #ddd', 'height': '100%'})
        ], width=4),

        # BLOC 3 : Colonne DROITE (Graphique NOIR)
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='line-graph', style={'height': '550px'})
                ])
            ], style={'borderRadius': '5px', 'backgroundColor': '#1E1E1E', 'border': '1px solid #333', 'height': '100%'})
        ], width=8)
    ], className="g-4")

], fluid=True, style={'padding': '20px'})

# --- 3. CALLBACK ---
@app.callback(
    Output('line-graph', 'figure'),
    Input('table-interactif', 'selected_columns')
)
def update_graph(selected_cols):
    y_axis = selected_cols[0] if selected_cols else "gdpPercap"
    
    fig = px.line(
        df_americas, 
        x="year", 
        y=y_axis, 
        color="country",
        title=f"Evolution of {y_axis} in Americas",
        template="plotly_dark" # Fond noir activé ici
    )
    
    # Personnalisation de l'axe X et de la légende
    fig.update_layout(
        margin=dict(l=20, r=20, t=50, b=20),
        legend_title_text='Countries',
        paper_bgcolor='rgba(0,0,0,0)', # Rend le fond du graphique transparent pour voir la Card noire
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    # Réglage précis de l'axe des années comme sur ton image
    fig.update_xaxes(
        tickvals=[1960, 1980, 2000], 
        gridcolor='#333' # Grille discrète
    )
    
    return fig

if __name__ == '__main__':
    app.run(debug=True)