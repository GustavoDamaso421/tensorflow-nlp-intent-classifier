
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import sqlite3
import dash_bootstrap_components as dbc


try:
    conexao = sqlite3.connect('meu_banco_de_dados.db')
    query = "SELECT * FROM log_producao;"
    df = pd.read_sql_query(query, conexao)
    conexao.close()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
except Exception as e:
    
    print("ERRO AO LER O BANCO DE DADOS!")
    exit()


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = dbc.Container([

    dbc.Row([
        
        dbc.Col(html.H1("Dashboard de Produção WestRock", className="text-center text-primary mb-4"), width=12)
    ]),


    dbc.Row([

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Label("Selecione um Produto:"),
                    dcc.Dropdown(
                        id='filtro-produto',
                        options=[{'label': i, 'value': i} for i in df['codigo_produto'].unique()],
                        value='PROD-A'
                    ),
                ])
            ])
        ], width=4),

      
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='grafico-temperatura')
                ])
            ])
        ], width=8)
    ])
], fluid=True)



@app.callback(
    Output('grafico-temperatura', 'figure'),
    Input('filtro-produto', 'value')
)
def atualiza_grafico(produto_selecionado):
    df_filtrado = df[df.codigo_produto == produto_selecionado]
    fig = px.line(df_filtrado, x="timestamp", y="temperatura_secador",
                  title=f'Temperatura para o produto {produto_selecionado}')
    
    
    fig.update_layout(template="seaborn")
    
    return fig


if __name__ == '__main__':
    app.run(debug=True)