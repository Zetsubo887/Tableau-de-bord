from dash import Input, Output, ctx
from data import get_stocks_data, get_gapminder_data, METRICS_MAP
from utils import create_dark_line_chart, create_gapminder_bar

df_stocks = get_stocks_data()
df_gap = get_gapminder_data()

def register_callbacks(app):
    @app.callback(
        [Output('stk-graph-before', 'figure'), Output('stk-graph-during', 'figure'), 
         Output('stk-graph-after', 'figure'), Output('stk-badge-start', 'children'), Output('stk-badge-end', 'children')],
        [Input('stk-date-picker', 'start_date'), Input('stk-date-picker', 'end_date')]
    )
    def update_stocks(start, end):
        df_b = df_stocks[(df_stocks['date'] >= '2018-01-01') & (df_stocks['date'] <= '2018-05-01')]
        df_d = df_stocks[(df_stocks['date'] >= start) & (df_stocks['date'] <= end)]
        df_a = df_stocks[(df_stocks['date'] >= '2019-02-01') & (df_stocks['date'] <= '2019-12-30')]
        
        return (create_dark_line_chart(df_b, 'date'), 
                create_dark_line_chart(df_d, 'date'), 
                create_dark_line_chart(df_a, 'date'), 
                f"Début: {start}", f"Fin: {end}")

    @app.callback(
        Output('gap-main-graph', 'figure'),
        Input('gap-dropdown', 'value')
    )
    def update_gap(metric):
        conf = METRICS_MAP[metric]
        return create_gapminder_bar(df_gap, metric, conf['col'], conf['agg'])