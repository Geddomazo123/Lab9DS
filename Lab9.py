import pandas as pd
import numpy as np
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)





app = Dash(__name__)

# -- Import and clean data (importing csv into pandas)
# df = pd.read_csv("intro_bees.csv")
df = pd.read_csv("https://raw.githubusercontent.com/Geddomazo123/Lab9DS/main/DatosFinalesFinales.csv")


# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Análisis de consumo de combustible en Guatemala", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_year",
                 options=[
                     {"label": 'Gasolina Súper', "value": 'Gasolina Súper'},
                     {"label": 'Gasolina Regular', "value": 'Gasolina Regular'},
                     {"label": 'Gasolina Total', "value": 'Gasolina Total'},
                     {"label": 'Diesel', "value": 'Diesel'}],
                 multi=True,
                 value=['Gasolina Total'],
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='timeseries', figure={}),
    html.H1("Crecimiento Interanual de Combustibles en Guatemala", style={'text-align': 'center'}),
    dcc.Graph(id='yoy', figure={}),
    
    html.H1("Predicción de Combustibles en Guatemala", style={'text-align': 'center'}),
    dcc.Graph(id='pred', figure={}),

])



# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='timeseries', component_property='figure'),
     Output(component_id='yoy', component_property='figure'),
     Output(component_id='pred', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The year chosen by user was: {}".format(option_slctd)

    dff = df.copy()
    dfpred=df.copy()
    dff = dff[dff["Combustible"].isin(option_slctd)]
    dfpred = dfpred[dfpred["Categoría"].isin(option_slctd)]


    # Plotly Express
    fig = px.line(dff,
                  x="Fecha",
                  y="Consumo",
                  line_shape="spline",
                  render_mode="svg",
                  hover_name='Combustible',
                  color='Combustible')

    fig2 = px.line(dff,
              x="Fecha",
              y="Crecimiento Interanual",
              line_shape="spline",
              render_mode="svg",
              hover_name='Combustible',
              color='Combustible')

    fig3 = px.line(dfpred,
              x="Fecha",
              y="Consumo",
              line_shape="spline",
              render_mode="svg",
              hover_name='Combustible',
              color='Combustible')

    # Plotly Graph Objects (GO)
    # fig = go.Figure(
    #     data=[go.Choropleth(
    #         locationmode='USA-states',
    #         locations=dff['state_code'],
    #         z=dff["Pct of Colonies Impacted"].astype(float),
    #         colorscale='Reds',
    #     )]
    # )
    #
    # fig.update_layout(
    #     title_text="Bees Affected by Mites in the USA",
    #     title_xanchor="center",
    #     title_font=dict(size=24),
    #     title_x=0.5,
    #     geo=dict(scope='usa'),
    # )

    return container, fig, fig2,fig3


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
