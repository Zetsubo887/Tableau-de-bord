import plotly.express as px

def create_dark_line_chart(df, x_col, title=""):
    df_m = df.melt(id_vars=[x_col], var_name='variable', value_name='value')
    fig = px.line(df_m, x=x_col, y='value', color='variable', template="plotly_dark")
    fig.update_layout(
        margin=dict(l=5, r=5, t=10, b=5),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title=x_col,
        yaxis_title="value"
    )
    return fig

def create_gapminder_bar(df, metric_name, col, agg):
    df_g = df.groupby(['year', 'continent'])[col].agg(agg).reset_index()
    fig = px.bar(df_g, x="year", y=col, color="continent", template="plotly_dark", barmode="stack")
    fig.update_layout(
        margin=dict(l=20, r=20, t=30, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title=f"{metric_name} par Continent"
    )
    return fig