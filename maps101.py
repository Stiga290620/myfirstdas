import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
server=app.server

# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df0 = pd.read_csv("2-1.csv")



# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Отношение смертельных случаев COVID-19 к выявленным, %", style={'text-align': 'center'}),


     dcc.Dropdown(id="slct_year",
                  options=[],
                  multi=False,
                  value='Animation',
                  style={'width': "40%"}
                  ),
    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_bee_map', figure={})

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components

@app.callback(
     [Output(component_id='output_container', component_property='children'),
      Output(component_id='my_bee_map', component_property='figure')],
     [Input(component_id='slct_year', component_property='value')]
)
#
def update_graph(option_slctd):
    container = "The data chosen by user was: {}".format(option_slctd)

    # Plotly Express


    fig = px.choropleth(
       #df0[:200],
       data_frame=df0.Data,
        #   locationmode='USA-states',
       locations=df0.Code,
        #    scope="usa",
       color=df0.Data,
        #    hover_data=df,
       color_continuous_scale=px.colors.sequential.YlOrRd,
       labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
       animation_frame=df0.Date, #Data for animation, time-series data
       template='plotly_dark'
    )

    sss='Анимация для периода с '+ df0.Date[0]+' по '+df0.Date[len(df0.Date)-1]
    fig.update_layout(
        title_text=sss,
        geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
        ),
        annotations = [dict(
            x=0.55,
            y=0.1,
            xref='paper',
            yref='paper',
            text='',
            #text='Source: <a href="https://www.cia.gov/library/publications/the-world-factbook/fields/2195.html">\
            #   CIA World Factbook</a>',
            showarrow = False
        )]
        )


    return container, fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
